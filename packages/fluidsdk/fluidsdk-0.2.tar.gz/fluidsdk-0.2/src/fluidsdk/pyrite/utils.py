import ast
import functools
from inspect import Parameter, Signature
import inspect
from typing import Callable
from fluidsdk.message import Message


class PyriteSyntaxError(SyntaxError):
    ...


class PyriteTypeError(SyntaxError):
    ...


class PyriteTemplateError(SyntaxError):
    ...


def insert(context, idx, intent):
    context.flow_steps[f"{context.prefix}-{idx}"] = intent
    for ctx in context.step_contexts.values():
        ctx.add_step(f"{context.prefix}-{idx}", intent)


def insert_then_increment(context, idx, intent):
    insert(context, idx, intent)
    context.idx += 1


def raise_error(error_class, source_lines, filename, node, error_message):
    error = error_class(error_message)
    error.filename = filename
    error.lineno = node.lineno
    error.end_lineno = node.end_lineno
    error.offset = node.col_offset + 1
    error.end_offset = node.end_col_offset
    error.text = source_lines[node.sourcelineno - 1]
    raise error from None


raise_syntax_error = functools.partial(raise_error, PyriteSyntaxError)
raise_type_error = functools.partial(raise_error, PyriteTypeError)
raise_template_error = functools.partial(raise_error, PyriteTemplateError)


def parse_message(context, node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, str):
            return Message(message=node.value)
        else:
            raise_type_error(
                context.source_lines,
                context.filename,
                node,
                f"{type(node.value)} is not a valid message type. Try using a `str` instead.",
            )
    else:
        raise_type_error(
            context.source_lines,
            context.filename,
            node,
            "Messages can only be constants in pyrite.",
        )


def parse_messages(context, nodes):
    return map(parse_message, nodes)


def get_context_name(context_manager, error_callable):
    if len(context_manager.args) < 1:
        error_callable(
            context_manager,
            'Context name required. Did you mean `with Context("context_name"):`?',
        )
    if len(context_manager.args) > 1:
        error_callable(
            context_manager,
            'Only one context name can be passed. Did you mean `with Context("context_name"):`?',
        )
    context_name_node = context_manager.args[0]
    if not isinstance(context_name_node, ast.Constant) or not isinstance(
        context_name_node.value, str
    ):
        raise_syntax_error(
            context_name_node,
            'Context name must be a of type `str`. Did you mean `with Context("context_name"):`?',
        )
    return context_name_node.value


def make_signature(names):
    return Signature(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names)


def test_signature(signature, args, kwargs, error_callable):
    try:
        bound_args = signature.bind(*args, **{i.arg: i.value for i in kwargs})
        bound_args.apply_defaults()
        return bound_args
    except TypeError as e:
        error_callable(str(e))


def assert_node_type(node, type, error_callable, message=None):
    if not isinstance(node, type):
        error_callable(
            node,
            message or f"This must be a {type}.",
        )


def assert_constant_type(node, type, error_callable, message=None):
    assert_node_type(node, ast.Constant, error_callable, message)
    if not isinstance(node.value, type):
        error_callable(
            node,
            message or f"This must be a {type}.",
        )


def get_builder(f: Callable):
    return f(*([None] * len(inspect.signature(f).parameters)))
