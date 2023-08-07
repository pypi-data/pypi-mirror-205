import time
import uuid
from typing import Dict, List, Literal, Union

from pydantic import BaseModel, Field

from fluidsdk.message import BotMessageUnion, UserMessageUnion


class Reminder(BaseModel):
    uuid_: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        alias="uuid",
        title="UUID",
        description="UUID for this reminder.",
    )
    flow_id: str = Field(
        ..., title="Flow ID", description="ID of the flow this reminder is from."
    )
    conversation_id: str = Field(
        ...,
        title="Conversation ID",
        description="Conversation ID of the user to trigger the reminder for.",
    )
    source: str = Field(
        ...,
        title="Source",
        description="Source of the conversation. Usually whatsapp, but can be widget, or any other supported third party service.",
    )
    reminder_id: str = Field(
        ...,
        title="Reminder ID",
        description="Reminder ID in the flow's reminder config.",
    )
    trigger_time: int = Field(
        default_factory=lambda: time.time() + 5 * 60,
        title="Trigger Time",
        description="Timestamp to trigger the reminder at.",
    )
    data: Dict = Field({}, title="Data", description="Data for the reminder.")


class ReminderTask(BaseModel):
    type: str


class SetDataReminderTask(ReminderTask):
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


class MessageReminderTask(ReminderTask):
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


class HTTPRequestReminderTask(ReminderTask):
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


class ExpressionReminderTask(ReminderTask):
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


class ProcessMessageReminderTask(ReminderTask):
    type: Literal["process-message"]
    message: Union[str, UserMessageUnion] = Field(None, title="Message")


class ReminderConfig(BaseModel):
    trigger: str = Field(
        "`true`",
        title="Trigger",
        description="A JMESPath expression to be run on the user data. Returns a `bool`. Runs on every turn of the user. If True, the reminder is added to the database.",
    )
    condition: str = Field(
        "`true`",
        title="Trigger",
        description="A JMESPath expression to be run on the user data. Returns a `bool`. Runs when the reminder is run. The pipeline is only run is True.",
    )
    trigger_time: str = Field(
        "sum([time(), `60`])",
        title="trigger_time",
        description="A JMESPath expression to be run on the user data. Returns a `int`. Runs when the reminder is being added. Represents the timestamp at which the reminder is to be processed. Default is 60 second after current time.",
    )
    pipeline: List[
        Union[
            SetDataReminderTask,
            MessageReminderTask,
            HTTPRequestReminderTask,
            ExpressionReminderTask,
            ProcessMessageReminderTask,
        ]
    ]
    data: dict = Field({})
