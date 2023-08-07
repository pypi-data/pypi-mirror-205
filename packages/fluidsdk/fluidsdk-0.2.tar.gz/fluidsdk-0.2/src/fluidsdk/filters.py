from typing import TYPE_CHECKING, Dict, List, Literal, Union

from pydantic import BaseModel, Field, PrivateAttr

from fluidsdk.conversations_v3 import Conversations_Model_v3
from fluidsdk.message import *

if TYPE_CHECKING:
    from dataclasses import dataclass as _basemodel_decorator
else:
    _basemodel_decorator = lambda x: x


class FilterTask(BaseModel):
    type: str
    _filter_id: str = PrivateAttr("")


class SetDataFilterTask(FilterTask):
    type: Literal["set-data"]
    data: dict = Field(
        None, title="Data", description="Data to set to the user's answer field."
    )
    state: Literal[
        "INTENT_NOT_STARTED",
        "INTENT_AWAITING_RESPONSE",
        "TEMPLATE_INVITED",
        "CONVERSATION_ENDED",
        "CONVERSATION_NOT_STARTED",
    ] = Field(None, title="state", description="What state to set the user to")
    step: str = Field(None, title="step", description="What step to send the user to")

    async def process(self, flow, conversation: Conversations_Model_v3):
        if self.step is None:
            self.step = conversation.current_flow_step
        if self.state is None:
            self.state = conversation.current_state
        conversation.set_next_step(
            flow,
            self.state,
            conversation.replace_answer_keys(self.step),
            conversation.replace_answer_keys(self.data),
        )


class MessageFilterTask(FilterTask):
    type: Literal["message"]
    text: List[Union[str, BotMessageUnion]] = Field(
        ..., title="Text", description="A list of messages to send to the user."
    )


class HTTPBody(BaseModel):
    body_type: Literal[None, "text", "json", "form"] = Field(
        None,
        title="Body Type",
        description="Type of request body. Changes how `data` is parsed and adds relevant `Content-Type` Header.",
    )
    data: Union[str, Dict] = Field(None, title="Data", description="HTTP Body Data.")


class HTTPRequestFilterTask(FilterTask):
    type: Literal["http"]
    url: str = Field(
        ...,
        title="URL",
        description="URL to send the request to.",
    )
    method: Literal["GET", "POST"] = Field(
        "GET", title="Method", description="HTTP Method to use for making the request."
    )
    headers: Dict[str, str] = Field(
        {}, title="Headers", description="HTTP headers to include in the request"
    )
    params: Dict[str, str] = Field(
        {},
        title="Parameters",
        description="URL Encoded Parameters to be included in the requested.",
    )
    body: HTTPBody = Field(
        None, title="Body", description="HTTP Body to be included in the request."
    )
    response_type: Literal["text", "json"] = Field(
        "json",
        title="Response Type",
        description="Type to interpret the response body as.",
    )
    answer_field: str = Field(
        ...,
        title="Answer Field",
        description="Field in the user's Conversation_Model.data to store the answer in.",
    )


class ExpressionFilterTask(FilterTask):
    type: Literal["expression"]
    expression: str = Field(
        ...,
        title="Expression",
        description="A JMESPath expression to be run on the user data.",
    )
    answer_field: str = Field(
        ...,
        title="Answer Field",
        description="Field in the user's Conversation_Model.data to store the answer in.",
    )


class TerminalFilterTask(FilterTask):
    """
    # Terminal Task

    Returns the result of the expression to the pipeline.
    If `None` is returned, pipeline continues as normal.
    If `True` or a truthy value is returned the Pipeline stops, along with processing more filters, or the flow.
    If `False` or a non-None falsy value is returned the Pipeline stops, but the next filter, or the flow processing continues.
    """

    type: Literal["terminal"]
    condition: str = Field(
        ...,
        title="Expression",
        description="A JMESPath expression to be run on the user data.",
    )

    async def process(self, flow, conversation: Conversations_Model_v3):
        try:
            return process_expression(self.condition, conversation.data)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return False


class ProcessMessageFilterTask(FilterTask):
    """
    Process Message Task

    Processes a message in the flow, and stops further processing.
    """

    type: Literal["process-message"]
    message: Union[str, UserMessageUnion] = Field(None, title="Message")


class Filter(BaseModel):
    """
    # Filter

    Filters are processed before the message is processed by the flow.
    The pipeline is run if the trigger returns `True`.
    Their return value determines whether or not further filters and the flow is processed.

    Basic usage involves, catching a value, sending a message, and returning `False`, and maybe setting the data to move the user to a particular step.
    For more complicated usage, you can chain together multiple filters, or use the `ProcessMessageTask` to do work in the flow itself.

    Example, to check if the current message is a swear word using GPT, you can have a filter that triggers for all messages.
    The pipeline would contain a `SetDataTask` to save the current step, state, and message to a temporary variable and to move to a part of the flow with
    the `GPTGenerateIntent` which contains the GPT call to check if the word is a swear word, and a `ConditionIntent` to move to a different part of the flow
    or return a scolding if that is true, or to return back to the flow and continue if not true,
    then a `ProcessMessageTask` to actually start the processing. Use the `next` and `next-state` fields to return to normal flow.

    Need to add a GPTGenerateTask, so this isn't required for most cases.
    The pipeline can look like
    GPTGenerate -> Message (with conditionals) -> Terminal/ProcessMessage

    """

    trigger: str = Field(
        "`false`",
        title="Trigger",
        description="A jq/JMESPath expression to be run on the user data. Returns a `bool`. The pipeline is only run is True.",
    )
    pipeline: List[
        Union[
            SetDataFilterTask,
            MessageFilterTask,
            HTTPRequestFilterTask,
            ExpressionFilterTask,
            ProcessMessageFilterTask,
            TerminalFilterTask,
        ]
    ]
    _filter_id: str = PrivateAttr("")
