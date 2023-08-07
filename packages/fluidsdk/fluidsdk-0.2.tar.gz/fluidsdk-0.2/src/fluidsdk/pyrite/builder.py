import ast
import inspect
import logging
import sys
from copy import deepcopy
from functools import partial
from typing import Callable, Dict, List, Union

import astor
import requests

from fluidsdk.flow import Flow
from fluidsdk.intents import (
    AskDefiniteIntent,
    AskOpenIntent,
    ExpressionIntent,
    GPTGenerateIntent,
    SayIntent,
)
from fluidsdk.message import Message
from fluidsdk.pyrite import library, utils
from fluidsdk.pyrite.consts import ENGINE_GLOBALS, PYTHON_BUILTINS
from fluidsdk.templates import Template

sys.tracebacklimit = 0
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

BASE_URL = "https://engine.workhack.io"


statement_library = {ctx.__name__: ctx for ctx in library._exports["statement_library"]}
assignment_library = {
    ctx.__name__: ctx for ctx in library._exports["assignment_library"]
}
context_library = {ctx.__name__: ctx for ctx in library._exports["context_library"]}


class FlowBuilder:
    """
    Pyrite flow builder.

    :param flow_id: ID used to indentify the flow in the engine.
    :param flow_description: Purpose of the flow.
    :param data: Global data to be shared by all conversations. Can be accessed in the `flow_data` variable.
    :param invitation_messages: Messages sent when the bot messages the user first.
    :param referred_conversation_messages: Messages sent when the user messages the bot first.
    :param end_conversation_messages: Messages sent right before closing the conversation.
    :param token: Access Token to log into the engine. If not passed, the Builder will be in offline mode..
    """

    def __init__(
        self,
        flow_id: str,
        flow_description: str,
        *,
        data: Dict = None,
        invitation_messages: List[Message] = None,
        referred_conversation_messages: List[Message] = None,
        end_conversation_messages: List[Message] = None,
        token: str = None,
    ):
        self.flow = Flow(
            flow_id=flow_id,
            flow_description=flow_description,
            data=data or {},
            # Do not include reminders yet. The dashboard sets reminders which should
            # not be overwritten by the pyrite.
            # reminders={},
            filters={},
            step={},
            invitation_messages=invitation_messages or [],
            end_conversation_messages=end_conversation_messages or [],
            referred_conversation_messages=referred_conversation_messages or [],
        )

        self.token = token
        if token is not None:
            response = requests.get(
                f"{BASE_URL}/orgs", headers={"Authorization": f"Bearer {token}"}
            )
            if not response.ok:
                raise RuntimeError(
                    "Failed to Authenticate to the engine. Is the provided token valid?"
                )
            logging.info(f"Logged in as {response.json()['name']}")
        else:
            print(f"Builder for {flow_id} is in Offline Mode.")

        self.subroutines = {}
        self.templates = {}

    class Context:
        def __init__(
            self,
            prefix,
            idx,
            flow_steps,
            source_lines,
            filename,
            *,
            global_names=None,
            local_names=None,
            builder=None,
        ):
            self.prefix = prefix
            self.idx = idx
            self.flow_steps = flow_steps
            self.source_lines = source_lines
            self.filename = filename
            self.global_names = global_names or set()
            self.local_names = local_names or set()
            self.step_contexts = {}
            self.builder = builder

    def subroutine(self, f: Callable) -> Callable:
        """
        Include a subroutine to be used in a flow.
        Used as a decorator like this:

        .. code-block:: python

            @flow.subroutine
            def start():
                ...

        :return: Returns the same function

        """
        self.subroutines[f.__name__] = f
        return f

    def include_template(self, t: Union[str, Template]):
        """
        Include a template to be used in a flow.
        Template is not pushed until :py:mod:`Flow.push_templates` or :py:mod:`Flow.build_and_push` is called.
        """
        if isinstance(t, str):
            self.templates[t] = None
        elif isinstance(t, Template):
            self.templates[t.template_id] = t
        else:
            raise TypeError("This is not a Fluid Template.")

    def build_expression(self, expression_node, prefix, old_context) -> str:
        context = deepcopy(old_context)
        context.builder = old_context.builder
        context.step_contexts = old_context.step_contexts
        context.flow_steps = {}
        context.idx = 0
        context.prefix = f"{prefix}-expression-{context.idx}"
        raise_syntax_error = partial(
            utils.raise_syntax_error, context.source_lines, context.filename
        )

        class RewriteName(ast.NodeTransformer):
            def visit_Name(self, node):
                # If name is a global variable, use as is.
                if node.id in context.global_names:
                    return node
                # Else If, name is a local, index into data_stack
                elif node.id in context.local_names:
                    return ast.copy_location(
                        ast.Subscript(
                            value=ast.Subscript(
                                value=ast.Name(id="data_stack", ctx=ast.Load()),
                                slice=ast.UnaryOp(
                                    op=ast.USub(), operand=ast.Constant(value=1)
                                ),
                                ctx=ast.Load(),
                            ),
                            slice=ast.Constant(value=node.id),
                            ctx=node.ctx,
                        ),
                        node,
                    )
                # Else If, its a python built in. Return as is. (Example "int")
                elif node.id in PYTHON_BUILTINS:
                    return node
                # Else name error
                else:
                    raise_syntax_error(node, f"Undefined variable `{node.id}`")

        transformed_node = RewriteName().visit(expression_node)
        return astor.to_source(transformed_node)[:-1]

    def build_body(self, body, prefix, old_context) -> dict:
        context = deepcopy(old_context)
        context.step_contexts = old_context.step_contexts
        context.builder = old_context.builder
        context.flow_steps = {}
        context.prefix = prefix

        raise_syntax_error = partial(
            utils.raise_syntax_error, context.source_lines, context.filename
        )
        raise_type_error = partial(
            utils.raise_type_error, context.source_lines, context.filename
        )

        for node in body:
            # Line is an expression
            if isinstance(node, ast.Expr):
                if isinstance(node.value, ast.Call):
                    call_node = node.value
                    if call_node.func.id in statement_library:
                        utils.get_builder(statement_library[call_node.func.id])(
                            context, call_node
                        )
                    elif call_node.func.id in self.subroutines:
                        utils.insert_then_increment(
                            context,
                            context.idx,
                            ExpressionIntent(
                                expression=f"[call_stack, '{context.prefix}-{context.idx+1}'] | []",
                                answer_field="call_stack",
                                next_=f"{call_node.func.id}",
                            ),
                        )
                        utils.insert_then_increment(
                            context,
                            context.idx,
                            ExpressionIntent(
                                expression="`null`", answer_field="return_value"
                            ),
                        )
                    else:
                        raise_syntax_error(node, "Undefined subroutine.")
                else:
                    raise_syntax_error(
                        node.value,
                        "Unexpected Python Syntax. Pyrite does not support "
                        + str(type(node.value))
                        + " yet.",
                    )
            elif isinstance(node, ast.Assign):
                if len(node.targets) > 1:
                    raise_syntax_error(
                        node.targets[1],
                        "You can't assign to more than one target at a time yet.",
                    )
                if isinstance(node.targets[0], ast.Name):
                    target = node.targets[0].id
                    if target in context.global_names:
                        target_field = target
                    else:
                        target_field = "data_stack.[{py>len(data_stack)-1}]." + target
                    if isinstance(node.value, ast.Call):
                        call_node = node.value
                        # If the call node is a simple name. Like `subr(arg)` or `int(arg)`
                        if isinstance(call_node.func, ast.Name):
                            if call_node.func.id in self.subroutines:
                                raise_syntax_error(
                                    node,
                                    "Cannot assign returns values from subroutines yet.",
                                )
                            elif call_node.func.id in assignment_library:
                                # If this is a library function, call handler
                                utils.get_builder(
                                    assignment_library[call_node.func.id]
                                )(context, call_node, target_field)
                            elif call_node.func.id in PYTHON_BUILTINS:
                                # If node is a whitelisted python builtin, treat it as an expression
                                expression = self.build_expression(
                                    call_node, context.prefix, context
                                )
                                utils.insert_then_increment(
                                    context,
                                    context.idx,
                                    ExpressionIntent(
                                        expression=f"py>{expression}",
                                        answer_field=target_field,
                                    ),
                                )
                            else:
                                raise_syntax_error(call_node, "Undefined subroutine.")
                        # Else if the call node is an Attribute or Subscript. Like `re.test(arg)` or `xyz["func"](arg)`
                        else:
                            # Treat it as an expression
                            expression = self.build_expression(
                                call_node, context.prefix, context
                            )
                            utils.insert_then_increment(
                                context,
                                context.idx,
                                ExpressionIntent(
                                    expression=f"py>{expression}",
                                    answer_field=target_field,
                                ),
                            )
                    else:
                        expression = self.build_expression(
                            node.value, context.prefix, context
                        )
                        utils.insert_then_increment(
                            context,
                            context.idx,
                            ExpressionIntent(
                                expression=f"py>{expression}", answer_field=target_field
                            ),
                        )
                    context.local_names.add(target)
                elif isinstance(node.targets[0], ast.Tuple):
                    raise_syntax_error(
                        node.targets[0], "Assigning to tuples not supported yet"
                    )
                else:
                    raise_syntax_error(
                        node.targets[0],
                        f"Assigning to {str(node.targets[0])} not supported yet",
                    )
            elif isinstance(node, ast.Nonlocal):
                raise_syntax_error(
                    node, "Invalid keyword `nonlocal`. Did you mean `global`?"
                )
            elif isinstance(node, ast.Global):
                context.global_names.update(node.names)
            elif isinstance(node, ast.With):
                if len(node.items) < 1:
                    raise_syntax_error(
                        node,
                        "You cannot use the `with` statement without a context manager. Did you mean `with Context() as context_name:`?",
                    )
                if len(node.items) > 1:
                    raise_syntax_error(
                        node,
                        "You cannot use the `with` statement multiple context managers. Did you mean `with Context() as context_name:`?",
                    )
                context_manager_item = node.items[0]
                if isinstance(context_manager_item.context_expr, ast.Call):
                    if context_manager_item.optional_vars is None:
                        raise_syntax_error(
                            node,
                            "You must give this context a name. Did you mean `with Context() as context_name:`?",
                        )
                    if not isinstance(context_manager_item.optional_vars, ast.Name):
                        raise_syntax_error(
                            context_manager_item.optional_vars,
                            "Context name can only be a simple variable name. Did you mean `with Context() as context_name:`?",
                        )
                    context_name = context_manager_item.optional_vars.id
                    if isinstance(
                        context_manager_item.context_expr.func, ast.Attribute
                    ):
                        raise_syntax_error(
                            context_manager_item.context_expr.func,
                            'This is not a context manager. Did you mean `with Context("context_name"):`?',
                        )
                    context_function = context_library.get(
                        context_manager_item.context_expr.func.id
                    )
                    if context_function is None:
                        raise_syntax_error(
                            context_manager_item.context_expr.func,
                            'Undefined context manager. Did you mean `with Context("context_name"):`?',
                        )
                    ctx = utils.get_builder(context_function)

                    with ctx(
                        context_manager_item.context_expr,
                        node.body,
                        context,
                        context_name,
                    ):
                        ctx.body_context = self.build_body(
                            node.body,
                            f"{context.prefix}-{context.idx}-context-{context_name}",
                            ctx.body_context,
                        )
                elif isinstance(context_manager_item.context_expr, ast.Name):
                    context_name = context_manager_item.context_expr.id
                    if context_name not in context.step_contexts:
                        raise_syntax_error(
                            context_manager_item.context_expr,
                            f"Undefined context {context_name}.",
                        )
                    with context.step_contexts[context_name].with_body(
                        node.body, context
                    ):
                        ctx.body_context = self.build_body(
                            node.body,
                            f"{context.prefix}-{context.idx}-context-{context_name}",
                            ctx.body_context,
                        )
                else:
                    raise_syntax_error(
                        context_manager_item.context_expr,
                        'This is not a context manager. Did you mean `with Context("context_name"):`?',
                    )
            else:
                raise_syntax_error(
                    node,
                    "Unexpected Python Syntax. Pyrite does not support "
                    + str(type(node))
                    + " yet.",
                )
            # print(ast.dump(node, indent=4))
        return context

    def build_function(self, f) -> dict:
        filename = inspect.getmodule(f).__file__
        source_lines, line_count = inspect.getsourcelines(f)
        f_ast_body = ast.parse(inspect.getsource(f)).body
        if len(f_ast_body) != 1:
            print(
                "Subroutine invalid. Only pass functions to FlowBuilder.subroutine.",
                file=sys.stderr,
            )

        func_def: ast.FunctionDef = f_ast_body[0]
        line_offset = f.__code__.co_firstlineno - 1

        class FixLineNos(ast.NodeTransformer):
            parent = None

            def visit(self, node):
                if hasattr(node, "lineno") and hasattr(node, "end_lineno"):
                    node.sourcelineno = node.lineno
                    node.lineno += line_offset
                    node.end_lineno += line_offset
                self.generic_visit(node)
                return node

        func_def = FixLineNos().visit(func_def)

        raise_syntax_error = partial(utils.raise_syntax_error, source_lines, filename)
        raise_type_error = partial(utils.raise_type_error, source_lines, filename)

        # Check if the subroutine takes any arguments. If so, raise error.
        if func_def.args.posonlyargs:
            raise_syntax_error(
                func_def.args.posonlyargs[0],
                "Pyrite subroutines do not take any positional only arguments.",
            )
        if func_def.args.kwonlyargs:
            raise_syntax_error(
                func_def.args.kwonlyargs[0],
                "Pyrite subroutines do not take any keyword only arguments.",
            )
        if func_def.args.args:
            raise_syntax_error(
                func_def.args.args[0],
                "Pyrite subroutines do not take any arguments.",
            )
        if func_def.args.vararg:
            raise_syntax_error(
                func_def.args.vararg,
                "Pyrite subroutines do not take any variable arguments.",
            )
        if func_def.args.kwarg:
            raise_syntax_error(
                func_def.args.kwarg,
                "Pyrite subroutines do not take any variable keyword arguments.",
            )

        context = self.Context(
            prefix=func_def.name,
            idx=1,
            flow_steps={
                func_def.name: ExpressionIntent(
                    expression="`true`", answer_field="init"
                )
            },
            source_lines=source_lines,
            filename=filename,
            builder=self,
            global_names=set(ENGINE_GLOBALS),
        )

        # Push empty dict to the data stack
        utils.insert_then_increment(
            context,
            context.idx,
            ExpressionIntent(
                expression="[data_stack, `{}`] | []",
                answer_field="data_stack",
            ),
        )

        func_context = self.build_body(func_def.body, func_def.name, context)
        context.idx = func_context.idx
        context.flow_steps.update(func_context.flow_steps)

        # Pop the top of the data stack
        utils.insert_then_increment(
            context,
            context.idx,
            ExpressionIntent(
                expression="data_stack[:-1]",
                answer_field="data_stack",
            ),
        )
        # Get the return step from the call_stack
        utils.insert_then_increment(
            context,
            context.idx,
            ExpressionIntent(
                expression="call_stack[-1]",
                answer_field="return_step",
            ),
        )
        # Pop the top value from the call_stack and go to return_step
        utils.insert_then_increment(
            context,
            context.idx,
            ExpressionIntent(
                expression="call_stack[:-1]",
                answer_field="call_stack",
                next_="[{return_step || `END`}]",
            ),
        )

        return context.flow_steps

    def build(
        self,
    ) -> Dict[
        str, Union[SayIntent, AskDefiniteIntent, AskOpenIntent, GPTGenerateIntent]
    ]:
        """
        Build the flow by calling build_function on each subroutine.

        :return: A dictionary of steps that can be fed to the engine
        """

        flow_dict = {}
        # Update flow dictionary for each subroutines.
        for k, v in self.subroutines.items():
            flow_dict.update(self.build_function(v))
        self.flow.steps = flow_dict
        return self.flow

    def push_templates(self):
        """
        Push templates to engine. Access token is required.
        """
        assert self.token is not None, "Flow builder is in offline mode"
        for template_id, template in self.templates.items():
            if isinstance(template, str):
                continue
            logging.info(f"Updating template {template_id}")
            response = requests.patch(
                f"{BASE_URL}/engine/templates/{template_id}",
                headers={"Authorization": f"Bearer {self.token}"},
                json=template.dict(),
            )
            if not response.ok:
                raise RuntimeError(f"Failed to update template {template_id}")

    def push_flow(self):
        """
        Push flow to engine. Access token is required.
        """
        assert self.token is not None, "Flow builder is in offline mode"
        logging.info(f"Updating flow {self.flow.flow_id}")
        response = requests.patch(
            f"{BASE_URL}/engine/flows/{self.flow.flow_id}",
            headers={"Authorization": f"Bearer {self.token}"},
            json=self.flow.dict(exclude_unset=True),
        )
        if not response.ok:
            raise RuntimeError(f"Failed to update flow {self.flow.flow_id}")
        logging.info(
            f"Updated flow {self.flow.flow_id} to version {response.json()['version']}"
        )

    def build_and_push(self):
        """
        Build and push the flow, and templates to engine. Access token is required.
        """

        assert self.token is not None, "Flow builder is in offline mode"
        self.build()
        self.push_templates()
        self.push_flow()
