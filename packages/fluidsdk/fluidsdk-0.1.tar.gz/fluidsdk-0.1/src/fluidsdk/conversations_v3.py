from typing import Literal

from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel, Field

from fluidsdk.message import *


class ObjId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        try:
            return cls(v)
        except InvalidId:
            raise ValueError("Not a valid ObjectId")


class Conversations_Model_v3(BaseModel):
    id: ObjId = Field(default_factory=ObjectId, title="BSON Object ID", alias="_id")
    flow_id: str = Field(
        ..., title="Flow ID", description="Name of the current flow the user is in."
    )
    conversation_id: str = Field(
        ...,
        title="Conversation ID",
        description="Unique ID for the user. For Whatsapp this is the wa_id of the user.",
    )
    name: str = Field(..., title="Name", description="Name of the user")
    current_state: str = Field(
        "CONVERSATION_NOT_STARTED",
        title="Current State",
        description="Current State of the conversation in a particular flow step.",
    )

    current_flow_step: str = Field(
        "start", title="Current Flow Step", description="Name of the current flow step."
    )

    data: dict = Field(
        {"flow_states": {"stack": []}},
        title="Data",
        description="Arbitrary data about the user. Stores the user's answers, flow states, and other information.",
    )

    source: str = Field(
        "whatsapp",
        title="Source",
        description="Source of the conversation. Usually whatsapp, but can be widget, or any other supported third party service.",
    )
    status: Literal["live", "archived"] = Field(
        "live",
        title="Status",
        description="Whether the conversation is live or archived.",
    )

    last_user_message: Optional[float] = Field(
        None,
        title="Last User Message",
        description="Timestamp of the last user message.",
    )

    class Config:
        json_encoders = {
            ObjId: lambda v: str(v),
        }
