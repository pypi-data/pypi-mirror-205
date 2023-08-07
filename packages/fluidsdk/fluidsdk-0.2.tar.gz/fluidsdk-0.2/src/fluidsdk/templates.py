import time
from typing import TYPE_CHECKING, List

from pydantic import BaseModel, Field, PrivateAttr

from fluidsdk.conversational_modules import GPTConfig, OpenAIGPTConfig

template_cache = {}

if TYPE_CHECKING:
    from dataclasses import dataclass as _basemodel_decorator
else:
    _basemodel_decorator = lambda x: x


@_basemodel_decorator
class Template(BaseModel):
    template_id: str = Field(
        ..., title="Template ID", description="Template ID to lookup"
    )
    template_type: str = Field(
        ..., title="Template Type", description="The type of template this is."
    )

    _valid_until: int = PrivateAttr(default_factory=lambda: time.time() + 60)


@_basemodel_decorator
class AskOpenTemplate(Template):
    template_type = "ask-open"
    followup_prompt: str = Field(
        ...,
        title="Follow up Template",
        description="Prompt to use for the followup generation.",
    )
    question: str = Field(
        ...,
        title="Question",
        description="Question to be sent to the user and the prompt.",
    )
    user_prefix: str = Field(
        None,
        title="User Prefix",
        description="Prefix to use for user messages when adding the context to the prompt. User messages are not added if set to None, Use empty string if no prefix is to be added.",
    )
    bot_prefix: str = Field(
        None,
        title="Bot Prefix",
        description="Prefix to use for bot messages when adding the context to the prompt. Bot messages are not added if set to None, Use empty string if no prefix is to be added.",
    )
    bot_thought_prefix: str = Field(
        None,
        title="Bot Thought Prefix",
        description="Allows for inner monologue in the prompt.",
    )
    keep_bot_thoughts_in_all_turns: bool = Field(
        False,
        title="Keep inner monologue to every turn",
        description="If set to True, the prompt will keep the previously generated inner monologue for future turns. ",
    )
    exchange_separator: str = Field(
        None,
        title="Exchange Separator",
        description="String to add between exchanges when adding context to the prompt.",
    )
    gpt_config: GPTConfig = Field(
        OpenAIGPTConfig(),
        title="GPT Config",
        description="GPT Settings to use.",
    )


@_basemodel_decorator
class GPTGenerateTemplate(Template):
    template_type = "gpt-generate"
    re: str = Field(
        ...,
        title="Result Regular Expression",
        description="Regular Expression to run on the generation. The groups in the regular expression will be stored in the answers.",
    )
    results: List[str] = Field(
        [],
        title="Results",
        description="Keys for the matched groups obtained by running the regular expression. Length must be equal to the number of groups in the regular expression.",
    )
    pre_prompt: str = Field(
        ...,
        title="Pre-Prompt",
        description="Prompt to add before the context.",
    )
    post_prompt: str = Field(
        ..., title="Post-Prompt", description="Prompt to add after the context."
    )
    user_prefix: str = Field(
        None,
        title="User Prefix",
        description="Prefix to use for user messages when adding the context to the prompt. User messages are not added if set to None, Use empty string if no prefix is to be added.",
    )
    bot_prefix: str = Field(
        None,
        title="Bot Prefix",
        description="Prefix to use for bot messages when adding the context to the prompt. Bot messages are not added if set to None, Use empty string if no prefix is to be added.",
    )
    gpt_config: GPTConfig = Field(
        OpenAIGPTConfig(),
        title="GPT Config",
        description="GPT Settings to use.",
    )
    default_on_failure: dict = Field(
        {},
        title="Default on Failure",
        description="Default answer to set if the gpt didn't generate or regular expression fails to match.",
    )
