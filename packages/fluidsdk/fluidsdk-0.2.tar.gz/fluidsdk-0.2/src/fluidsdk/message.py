import random
import string
import time
from typing import TYPE_CHECKING, ForwardRef, List, Literal, Optional, Union
from uuid import uuid4

from bson import ObjectId
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from dataclasses import dataclass as _basemodel_decorator
else:
    _basemodel_decorator = lambda x: x


MessageInDb = ForwardRef("MessageInDb")


class ObjId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        try:
            print("validating", type(cls(v)))
            return cls(v)
        except InvalidId:
            raise ValueError("Not a valid ObjectId")

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


@_basemodel_decorator
class UserMessageContext(BaseModel):
    forwarded: Optional[bool] = Field(
        False, title="Forwarded", description="Whether or not this message is forwarded"
    )
    frequently_forwarded: Optional[bool] = Field(
        False,
        title="Frequently Forwarded",
        description="Whether or not this message is frequently forwarded",
    )
    sent_by: Optional[str] = Field(
        None,
        title="Author of the message if forwarded, or if this is a message/button reply.",
    )
    reply_to: Optional[str] = Field(
        None,
        title="Reply To",
        description="ID of the message this message is a reply to.",
    )
    reply_to_message: Optional[MessageInDb] = Field(
        None,
        title="Reply To Message",
        description="The message object from the database this message is a reply to.",
    )


@_basemodel_decorator
class UserMessage(BaseModel):
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        title="ID",
        description="Message ID from the source.",
    )
    context: UserMessageContext = Field(UserMessageContext())
    timestamp: float = Field(
        default_factory=time.time,
        title="Timestamp",
        description="Timestamp from the source.",
    )
    name: str = Field(
        "Candidate", title="Name", description="Name of the sender of the message."
    )
    conversation_id: Optional[str] = Field(None, title="Conversation ID")
    type: Literal["text", "voice", "document", "video", "image", "sticker"]
    message: str = Field(..., title="Message", description="Message as text.")


@_basemodel_decorator
class UserTextMessage(UserMessage):
    type: Literal["text"] = "text"


@_basemodel_decorator
class UserLocationMessage(UserMessage):
    type: Literal["location"] = "location"
    address: str = Field(None, title="Address")
    latitude: float = Field(None, title="Latitude")
    longitude: float = Field(None, title="Longitude")
    location_name: str = Field(None, title="Location Name", description="Location Name")
    url: str = Field(None, title="URL")


@_basemodel_decorator
class UserMediaMessage(UserMessage):
    type: Literal["voice", "document", "video", "image", "audio", "sticker"]
    bucket: str = Field(..., title="Bucket", description="S3 Bucket")
    key: str = Field(..., title="Key", description="S3 Key")
    url: str = Field(None, title="URL", description="Presigned S3 URL")
    filename: str = Field(None, title="Filename", description="Local filename.")
    hash: str = Field(
        None, title="Hash", description="Hash of the media. SHA256 for whatsapp."
    )
    caption: Optional[str] = Field("", title="Caption")


@_basemodel_decorator
class UserButtonMessage(UserMessage):
    type: Literal["button"]
    button_id: str = Field(..., title="Button ID")
    payload: Optional[str] = Field(None, title="Payload")
    title: str
    description: Optional[str]


@_basemodel_decorator
class UserContactAddress(BaseModel):
    city: str
    country: str
    country_code: str
    state: str
    street: str
    type: str
    zip: str


@_basemodel_decorator
class UserContactEmail(BaseModel):
    email: str
    type: str


@_basemodel_decorator
class UserContactIM(BaseModel):
    service: str
    user_id: str


@_basemodel_decorator
class UserContactName(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    formatted_name: Optional[str]


@_basemodel_decorator
class UserContactOrg(BaseModel):
    company: Optional[str]


@_basemodel_decorator
class UserContactPhone(BaseModel):
    phone: str
    type: str
    wa_id: Optional[str]


@_basemodel_decorator
class UserContactUrl(BaseModel):
    url: str
    type: str


@_basemodel_decorator
class UserContact(BaseModel):
    addresses: List[UserContactAddress]
    birthday: Optional[str]
    emails: List[UserContactEmail]
    ims: List[UserContactIM]
    name: Optional[UserContactName]
    org: Optional[UserContactOrg]
    phones: List[UserContactPhone]
    urls: List[UserContactUrl]


@_basemodel_decorator
class UserContactsMessage(UserMessage):
    type: Literal["contacts"]
    contacts: List[UserContact]


@_basemodel_decorator
class UserWhatsappStickerMessage(UserMessage):
    type: Literal["sticker"]


UserMessageUnion = Union[
    UserButtonMessage,
    UserContactsMessage,
    UserWhatsappStickerMessage,
    UserLocationMessage,
    UserTextMessage,
    UserMediaMessage,
]


@_basemodel_decorator
class BotMessageContext(BaseModel):
    current_step: Optional[str] = Field(
        None,
        title="Flow Step",
        description="Name of the flow step, reminder id or filter id this message was generated on. None if Manual Message.",
    )
    steps: List[str] = Field(
        [],
        title="Steps",
        description="List of steps the flow went through as the message was processing.",
    )
    state: Literal[
        "TEMPLATE_INVITED",
        "CONVERSATION_NOT_STARTED",
        "INTENT_NOT_STARTED",
        "INTENT_AWAITING_RESPONSE",
        "CONVERSATION_ENDED",
    ] = Field(
        None,
        title="Flow State",
        description="The flow state of the user when this message was generated.",
    )
    followup: Optional[int] = Field(
        None,
        title="Followup number",
        description="The followup number of this message if this message was generated as part of the a AskOpen Intent.",
    )

    def __add__(self, other):
        d = self.dict(exclude_unset=True)
        d.update(other.dict(exclude_unset=True))
        return type(self)(**d)


@_basemodel_decorator
class BotMessage(BaseModel):
    type: str = Field(..., title="Type", description="Message type.")
    condition: str = Field(
        "`true`", title="Condition", description="Whether or not to send this message"
    )
    conversation_id: Optional[str] = Field(
        None,
        title="Conversation ID",
        description="Conversation ID to send this message to instead of the current conversation.",
    )
    source_id: Optional[str] = Field(
        None,
        title="Source ID",
        description="Override the Source to send this message from.",
    )
    context: BotMessageContext = Field(BotMessageContext())


@_basemodel_decorator
class Message(BotMessage):
    type: Literal["text"] = "text"
    message: str


@_basemodel_decorator
class InteractiveMessageOption(BaseModel):
    id: str = Field(
        default_factory=lambda: "".join(random.choices(string.ascii_letters, k=8))
    )
    title: str = Field(..., title="Title")
    description: Optional[str] = Field("", title="Description")

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == other
        elif isinstance(other, dict):
            return self.dict(by_alias=True) == other
        else:
            return

    def __str__(self):
        if self.description not in [None, ""]:
            return f"{self.title} {self.description}"
        else:
            return self.title


@_basemodel_decorator
class InteractiveMessage(BotMessage):
    type: Literal["button", "list"] = Field("list", title="Type")
    body: str = Field(
        ...,
        title="Body",
        description="Message to send in the body of the interactive message.",
    )
    footer: str = Field(
        "",
        title="Footer",
        description="Message to send in the footer of the interactive message.",
    )

    # TODO: separate validation for button and list.
    options: Union[List[Union[InteractiveMessageOption, str]], str] = Field(
        [],
        title="Options",
        description="List or Button options, or an expression that evaluates to a list of button options.",
    )


@_basemodel_decorator
class WhatsappTemplateHeader(BaseModel):
    type: Literal["image", "video", "document"] = Field(
        ..., title="Type", description="Type of header."
    )
    link: str = Field(..., title="Link", description="URL to the media.")


@_basemodel_decorator
class Dialog360WhatsappTemplateMessage(BotMessage):
    type: Literal["template"] = "template"
    template_type: Literal["dialog360"] = Field("dialog360")
    template_id: Optional[str] = Field(
        ...,
        title="Template ID",
        description="Whatsapp approved message template ID.",
    )
    header: WhatsappTemplateHeader = Field(
        None,
        title="Header",
        description="Header details if present in the template.",
    )
    params: List[str] = Field(
        [],
        title="Parameters",
        description="List of strings to pass as body parameters for the Whatsapp Template.",
    )
    text: str = Field("", title="Text", description="Text to send in the message.")
    url: Union[str, List[str]] = Field(
        None,
        title="URL",
        description="Text to pass to the URL if a CTA button exists in the template.",
    )


@_basemodel_decorator
class GupshupWhatsappTemplateMessage(BotMessage):
    type: Literal["template"]
    template_type: Literal["gupshup"]
    template_id: Optional[str] = Field(
        None,
        title="Template ID for reference",
        description="Whatsapp approved message template ID.",
    )
    header: Optional[WhatsappTemplateHeader] = Field(
        None,
        title="Header",
        description="Header details if present in the template.",
    )
    interactive: Optional[bool] = Field(
        False,
        title="Is Interactive?",
        description="Whether or not this message is interactive (aka. has buttons)",
    )
    text: str = Field("", title="Text", description="Text to send in the message.")


class BasicEmailMessage(BotMessage):
    type: Literal["email"] = "email"
    from_address: Optional[str] = Field(
        None, title="From", description="Email address to send from."
    )
    to_address: Optional[str] = Field(
        None, title="To", description="Email address to send to."
    )
    subject: str = Field(..., title="Subject", description="Subject of the email.")
    body_html: str = Field(..., title="Body", description="HTML body of the email.")
    body_text: str = Field(
        ...,
        title="Text body of the email.",
        description="Body of the mail when html is not supported",
    )


@_basemodel_decorator
class RemoteAudioMessage(BotMessage):
    type: Literal["audio"] = "audio"
    link: str = Field(
        ...,
        title="Link",
        description="URL to the audio.",
    )


@_basemodel_decorator
class S3AudioMessage(BotMessage):
    type: Literal["audio"] = "audio"
    bucket: str = Field(
        ...,
        title="Bucket",
        description="S3 Bucket of the media.",
    )
    key: str = Field(
        ...,
        title="Key",
        description="S3 Key of the media.",
    )


@_basemodel_decorator
class RemoteMediaMessage(BotMessage):
    type: Literal["image", "video", "document"]
    link: str = Field(
        ...,
        title="Link",
        description="URL to the media.",
    )
    caption: str = Field(
        ..., title="Caption", description="Message to be sent with the media."
    )


@_basemodel_decorator
class S3MediaMessage(BotMessage):
    type: Literal["image", "video", "document"]
    bucket: str = Field(
        ...,
        title="Bucket",
        description="S3 Bucket of the media.",
    )
    key: str = Field(
        ...,
        title="Key",
        description="S3 Key of the media.",
    )
    caption: str = Field(
        ..., title="Caption", description="Message to be sent with the media."
    )


@_basemodel_decorator
class LocalAudioMessage(BotMessage):
    type: Literal["audio"]
    path: str = Field(
        ...,
        title="Path",
        description="Local Path to the audio.",
    )


@_basemodel_decorator
class LocalMediaMessage(BotMessage):
    type: Literal["image", "video", "document"]
    path: str = Field(
        ...,
        title="Path",
        description="Local Path to the media.",
    )
    caption: str = Field(
        ..., title="Caption", description="Message to be sent with the media."
    )


@_basemodel_decorator
class EmbedMessage(BotMessage):
    type: Literal["embed"]
    url: str = Field(..., title="URL", description="URL of the page to embed.")


BotMessageUnion = Union[
    str,
    InteractiveMessage,
    RemoteMediaMessage,
    S3MediaMessage,
    S3AudioMessage,
    LocalMediaMessage,
    LocalAudioMessage,
    RemoteAudioMessage,
    Dialog360WhatsappTemplateMessage,
    GupshupWhatsappTemplateMessage,
    EmbedMessage,
    BasicEmailMessage,
    Message,
]


@_basemodel_decorator
class MessageInDb(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid4()), title="Message Id")
    type: Literal["invitation", "flow", "reminder", "filter", "manual"] = Field(
        "flow",
        title="Message type",
        description="Type of message this is. `flow` type is messages sent during a conversation. `reminders` is messages sent through the reminder engine. `manual` is messages sent manually.",
    )
    conversation_oid: Optional[ObjId] = Field(None, title="Conversation BSON Object ID")
    conversation_id: str = Field(..., title="User ID")
    flow_id: str = Field(..., title="Flow ID")
    source: str = Field(
        ..., title="Source", description="Source this message was sent/received from"
    )
    message: Union[
        UserMessageUnion,
        Message,
        InteractiveMessage,
        RemoteMediaMessage,
        S3MediaMessage,
        S3AudioMessage,
        LocalMediaMessage,
        LocalAudioMessage,
        RemoteAudioMessage,
        Dialog360WhatsappTemplateMessage,
        GupshupWhatsappTemplateMessage,
        BasicEmailMessage,
        RemoteAudioMessage,
        EmbedMessage,
    ] = Field(..., title="Message", description="The object representing the message.")
    sender: Literal["user", "bot"] = Field(..., title="Sender")
    timestamp: int = Field(default_factory=time.time, title="Timestamp")
    status: Literal[
        "sending", "failed", "sent", "delivered", "read", "deleted", "received"
    ] = Field(
        "sending", title="Status", description="Status of the message being sent."
    )
    data: dict = Field({}, title="Data", description="Arbitrary data.")

    class Config:
        arbitrary_types_allowed = True


UserMessageContext.update_forward_refs()
