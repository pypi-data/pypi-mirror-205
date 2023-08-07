from typing import TYPE_CHECKING, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from fluidsdk.message import BotMessageUnion
from fluidsdk.status_webhook import StatusIntentData
from fluidsdk.templates import AskOpenTemplate, GPTGenerateTemplate

if TYPE_CHECKING:
    from dataclasses import dataclass as _basemodel_decorator
else:
    _basemodel_decorator = lambda x: x


@_basemodel_decorator
class MixTrack(BaseModel):
    event: str = Field(
        "Event Tracked", title="Event", description="Name of the event tracked"
    )
    data: Dict[str, str] = Field(
        {}, title="Data", description="Data to be attached to the mixpanel event."
    )


@_basemodel_decorator
class Intent(BaseModel):
    intent_type: str = Field(
        ..., alias="type", title="Type", description="Type of Intent."
    )
    mixtrack: MixTrack = Field(None)
    status: StatusIntentData = Field(
        None,
        title="Status",
        description="Set the status of the conversation. This will be shown on the dashboard, and pushed to the status webhook of it is present in the flow.",
    )
    next_: str = Field(
        None, alias="next", title="Next", description="Next step to jump to."
    )
    data: Optional[dict] = Field(
        None, title="Data", description="Extra Data for the intent."
    )

    def __add__(self, other):
        if isinstance(other, NextConfig):
            output = self.dict(exclude_unset=True)
            output["next"] = other.next
            return type(self).parse_obj(output)
        elif isinstance(other, StatusIntentData):
            output = self.dict(exclude_unset=True)
            output["status"] = other
            return type(self).parse_obj(output)
        elif isinstance(other, MixTrack):
            output = self.dict(exclude_unset=True)
            output["mixtrack"] = other
            return type(self).parse_obj(output)
        else:
            raise TypeError

    class Config:
        fields = {"mixtrack": {"exclude": True}}
        allow_population_by_field_name = True


@_basemodel_decorator
class NextConfig(BaseModel):
    next: str


@_basemodel_decorator
class AskDefiniteConfig(BaseModel):
    re: str = Field(
        None,
        title="Match Regular Expression",
        description="Regular Expression to run on the answer. If the results is not found, `match_not_found_message` is sent. If it is found, the match is saved in the answer field.",
    )
    match_not_found_message: List[BotMessageUnion] = Field(
        ["Hmmm... Can you send it in the correct format?"],
        title="Match not found message",
        description="A List of messages to send to the user if the answer doesn't have the regex provided in `re`.",
    )
    not_in_list_message: List[BotMessageUnion] = Field(
        ["You must pick from the options above"],
        title="Not in list message",
        description="A List of messages to send to the user if the answer is not in the lists provided.",
    )
    await_for_reply: str = Field(
        "`true`",
        title="Await for reply",
        description="If True, the bot will wait for the user to reply before going to next step.",
    )

    # config for accepting multiple messages

    single: bool = Field(
        True,
        title="Single or wait for multiple messages before moving to next step",
        description="If True, the bot will only accept one answer.",
    )
    done_message: str = Field(
        "When you are done, say, 'done', or click on this button.",
        title="Done Message",
        description="Message to send instructing the user on how to end the step.",
    )
    done_button: str = Field(
        "Done",
        title="Done Button",
        description="Button text to use with the done message. Detection is case insensitive.",
    )
    keep_sending_message: str = Field(
        "Keep sending more, or say 'done'",
        title="Keep Sending Message",
        description="Message sent to the user each time they upload an attachment.",
    )


@_basemodel_decorator
class AskDefiniteIntent(Intent):
    intent_type: Literal["ask-definite"] = "ask-definite"
    question: Union[str, List[BotMessageUnion]] = Field(
        ..., title="Question", description="A List of questions to ask the user."
    )
    answer_field: str = Field(
        ...,
        title="Answer Field",
        description="Field in the user's Conversation_Model.data to store the answer in.",
    )
    list_only: bool = Field(
        False,
        title="List Only",
        description="If True, and InteractiveMessage present in questions, the response must be of the options.",
    )
    mirror: bool = Field(
        False,
        title="Mirror",
        description="Whether to mirror, i.e. acknowledge the user's response.",
    )
    config: AskDefiniteConfig = Field(
        AskDefiniteConfig(), title="Config", description="Ask Definite Config"
    )
    # TODO Add mirror settings field, to add custom prompts

    def __add__(self, other):
        if isinstance(other, AskDefiniteConfig):
            config = self.config.dict(exclude_unset=True)
            config.update(other.dict(exclude_unset=True))
            output = self.dict(exclude_unset=True)
            output["config"] = config
            return AskDefiniteIntent.parse_obj(output)
        elif isinstance(other, SayIntent):
            questions = self.question + other.text
            output = self.dict(exclude_unset=True)
            output["question"] = questions
            return AskDefiniteIntent.parse_obj(output)
        else:
            return super().__add__(other)


@_basemodel_decorator
class AskOpenIntent(Intent):
    intent_type: Literal["ask-open"] = "ask-open"
    template: Union[str, AskOpenTemplate] = Field(
        ...,
        title="Template",
        description="Template to use from intentsdb, or template object.",
    )
    question: BotMessageUnion = Field(
        None,
        title="Question",
        description="Question to ask the user, instead of the one in template. This does not get added to the prompt to generate the followup.",
    )
    answer_field: str = Field(
        ...,
        title="Answer Field",
        description="Field in the user's Conversation_Model.data to store the answer in.",
    )
    followups: int = Field(
        ...,
        title="Followups",
        description="Number of followups.",
    )


@_basemodel_decorator
class SayIntent(Intent):
    intent_type: Literal["say"] = "say"
    text: Union[str, List[BotMessageUnion]] = Field(
        ..., title="Question", description="A list of messages to send to the user."
    )

    def __add__(self, other):
        if isinstance(other, AskDefiniteIntent):
            questions = self.text + other.question
            output = other.dict(exclude_unset=True)
            output["question"] = questions
            return AskDefiniteIntent.parse_obj(output)
        elif isinstance(other, SayIntent):
            text = self.text + other.text
            output = other.dict(exclude_unset=True)
            output["text"] = text
            return SayIntent.parse_obj(output)
        else:
            return super().__add__(other)


@_basemodel_decorator
class ConditionIntent(Intent):
    intent_type: Literal["condition"] = "condition"
    condition: str = Field(
        ...,
        title="Condition",
        description="A JMESPath expression to be run on the user data. Returns a `bool`.",
    )
    if_: str = Field(
        ...,
        alias="if",
        title="If",
        description="Step to go to if condition is True",
    )

    else_: str = Field(
        None,
        alias="else",
        title="Else",
        description="Step to go to if condition is False",
    )


@_basemodel_decorator
class GPTGenerateIntent(Intent):
    intent_type: Literal["gpt-generate"] = "gpt-generate"
    template: Union[str, GPTGenerateTemplate] = Field(
        ...,
        title="Template",
        description="Template to use from intentsdb, or template object.",
    )
    args: Dict[str, str] = Field(
        {},
        title="Arguments",
        description="Key value pair of arguments to feed to the template.",
    )
    collect: List[str] = Field(
        [],
        title="Collect",
        description="An array of step names to collect answers from to feed to the template.",
    )
    answer_field: str = Field(
        ...,
        title="Answer Field",
        description="Field in the user's Conversation_Model.data to store the answer in.",
    )


@_basemodel_decorator
class GPTSearchIntent(Intent):
    intent_type: Literal["gpt-search"] = "gpt-search"
    engine: Literal["davinci", "curie", "babbage", "ada",] = Field(
        "davinci",
        title="Engine",
        description="Name of the large language model to use.",
    )
    query: str = Field(
        ...,
        title="Query",
        description="Query to run the search on.",
    )
    documents: Union[str, List[str]] = Field(
        ...,
        title="Documents",
        description="Documents or The ID of an uploaded file that contains documents to search over.",
    )
    purpose: str = Field(
        ..., title="Purpose", description="Purpose to use for mixpanel tracking."
    )
    max_rerank: int = Field(
        200,
        title="Max Rerank",
        description="The maximum number of documents to be re-ranked and returned by search.",
    )
    return_metadata: bool = Field(
        True,
        title="Return Metadata",
        description="A special boolean flag for showing metadata. If set to true, each document entry in the returned JSON will contain a 'metadata' field.",
    )
    answer_field: str = Field(
        ...,
        title="Answer Field",
        description="Field in the user's Conversation_Model.data to store the answer in.",
    )


@_basemodel_decorator
class CollectAttachmentsConfig(BaseModel):
    done_message: str = Field(
        "When you are done, say, 'done', or click on this button.",
        title="Done Message",
        description="Message to send instructing the user on how to end the step.",
    )
    done_button: str = Field(
        "Done",
        title="Done Button",
        description="Button text to use with the done message. Detection is case insensitive.",
    )
    non_file_error_message: str = Field(
        "Please upload a file.",
        title="Not File Error Message",
        description="Message sent to the user when they don't upload a file.",
    )
    wrong_file_type_error_message: str = Field(
        "Please upload only a {file_types} file.",
        title="Wrong File Type Error Message",
        description="Message sent to the user when they upload a file of the wrong type. `{file_types}` is replaced with the list of valid file types.",
    )
    keep_sending_message: str = Field(
        "Keep sending more, or say 'done'",
        title="Keep Sending Message",
        description="Message sent to the user each time they upload an attachment.",
    )


@_basemodel_decorator
class CollectAttachmentsIntent(Intent):
    intent_type: Literal["collect-attachments"] = "collect-attachments"
    attachment_types: List[
        Literal["image", "video", "document", "voice", "audio"]
    ] = Field(
        [],
        min_items=1,
        title="Attachment Types",
        description="List of allowed attachments.",
    )
    text: List[BotMessageUnion] = Field(
        ..., title="Text", description="A list of messages to send to the user."
    )
    answer_field: str = Field(
        ...,
        title="Answer Field",
        description="Field in the user's Conversation_Model.data to store the answer in.",
    )
    optional: bool = Field(
        False, title="Optional", description="Whether this step is optional."
    )
    single: bool = Field(
        True,
        title="Single",
        description="Whether this step takes only one attachment, or multiple.",
    )
    config: CollectAttachmentsConfig = Field(
        CollectAttachmentsConfig(), title="Config", description="Message Configuration."
    )

    def __add__(self, other):
        if isinstance(other, SayIntent):
            text = self.text + other.text
            output = self.dict(exclude_unset=True)
            output["text"] = text
            return CollectAttachmentsIntent.parse_obj(output)
        else:
            return super().__add__(other)


@_basemodel_decorator
class ExpressionIntent(Intent):
    intent_type: Literal["expression"] = "expression"
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


@_basemodel_decorator
class HTTPBody(BaseModel):
    body_type: Literal["text", "json", "form"] = Field(
        "text",
        alias="type",
        title="Body Type",
        description="Type of request body. Changes how `data` is parsed and adds relevant `Content-Type` Header.",
    )
    data: Union[str, dict, list, int, float] = Field(
        None, title="Data", description="HTTP Body Data."
    )

    class Config:
        allow_population_by_field_name = True


http_request_cache = {}


@_basemodel_decorator
class HTTPRequestConfig(BaseModel):
    cache: bool = Field(
        False, title="Cache", description="Whether or not to cache the responses"
    )
    cache_size: int = Field(
        180, title="Cache Size", description="Number of items to store in the cache"
    )
    cache_ttl: int = Field(
        3600, title="Cache TTL", description="Time to Live to use for the cache"
    )
    cache_type: Literal["TTLCache", "FIFOCache", "LFUCache", "LRUCache"] = Field(
        "LRUCache", title="Cache Type", description="Type of cache to use"
    )
    cache_save: str = Field(
        "`true`",
        title="Cache Save",
        description="Whether or not to add the result to cache.",
    )
    cache_skip: str = Field(
        "`false`",
        title="Cache Skip",
        description="Whether or not to skip checking the cache for the response.",
    )


@_basemodel_decorator
class HTTPRequestIntent(Intent):
    intent_type: Literal["http"] = "http"
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
    config: HTTPRequestConfig = Field(
        HTTPRequestConfig(),
        title="HTTP Request Config",
        description="Config options for HTTP Request Intent",
    )


@_basemodel_decorator
class QuizOption(BaseModel):
    correct: bool = Field(
        False,
        title="Correct",
        description="Whether this option is correct.",
    )
    response: List[BotMessageUnion] = Field(
        [],
        title="Response",
        description="Response to send if this option is selected.",
    )


@_basemodel_decorator
class SingleAnswerQuizIntent(Intent):
    intent_type: Literal["ask-single-answer-quiz"] = "ask-single-answer-quiz"
    instruction: BotMessageUnion = Field(
        None,
        title="situation instruction",
        description="The instruction related to the question to be sent to the user.",
    )
    question: BotMessageUnion = Field(
        ...,
        title="Actual question",
        description="Question that will be sent again if answered wrong",
    )
    options: Dict[str, QuizOption] = Field(
        {},
        title="Options and their correctness and responses",
    )
    answer_field: str = Field(
        ...,
        title="Answer Field",
        description="Field in the user's Conversation_Model.data to store the answer in.",
    )
    hint_to_choose_only_from_options: str = Field(
        "You have to choose from below options only",
        title="Hint to choose from options",
        description="Hint to choose from options",
    )


@_basemodel_decorator
class TextOnImageConfig(BaseModel):
    text: str = Field(
        ...,
        title="Text to be added on the image",
        description="Text to be displayed on the image",
    )
    font_size: int = Field(
        14,
        title="Font size",
        description="Font size of the text to be displayed on the image",
    )
    font_color: Union[str, tuple] = Field(
        "#000000",
        title="Font color in hex #rrggbb or #rrggbbaa, or color name",
        description="Example: #ffffff, red, etc.",
    )
    font_family: str = Field(
        "static/Advent_Pro/AdventPro-Regular.ttf",
        title="Font family ttf file path",
        description="Example: static/Advent_Pro/AdventPro-Regular.ttf",
    )
    position: List[float] = Field(
        [
            0.5,
            0.5,
        ],  # http://griddrawingtool.com/ in step 5 use at least 10x10 grid lines with Keep boxes square checked off
        title="Fractional position similar to viewport width and height in css. ex. [5/16, 6/15]",
        description="Example: [0.5, 0.5] will put the text right on center of image",
    )


class DynamicImage(Intent):
    intent_type: Literal["generate-image"] = "generate-image"
    template_path: str = Field(  # local file path, TODO: add expression/remote urls
        ...,
        title="Image path",
        description="Local Path to the image.",
    )
    text_config: List[TextOnImageConfig] = Field(
        [], title="Text on image and its style and position config"
    )
    caption: str = Field(
        "",
        title="Caption",
        description="Caption to be displayed along with the image",
    )
