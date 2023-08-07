from functools import partial
from typing import TYPE_CHECKING, Dict, Literal, Union

from pydantic import BaseModel, Field, confloat, conint, conlist

if TYPE_CHECKING:
    from dataclasses import dataclass as _basemodel_decorator
else:
    _basemodel_decorator = lambda x: x


print = partial(print, flush=True)


@_basemodel_decorator
class OpenAIGPTConfig(BaseModel):
    engine: Literal[
        "text-davinci-002",
        "text-davinci-001",
        "text-curie-001",
        "text-babage-001",
        "text-ada-001",
        "code-davinci-002",
        "code-cushman-001",
        "text-davinci-insert-002",
    ] = Field(
        "text-davinci-002",
        title="Engine",
        description="Name of the large language model to use.",
    )
    temperature: confloat(ge=0) = Field(
        0.5,
        title="Temperature",
        description="What sampling temperature to use. Higher values means the model will take more risks. Try 0.9 for more creative applications, and 0 (argmax sampling) for ones with a well-defined answer.",
    )
    max_tokens: conint(gt=0, le=4096) = Field(
        200,
        title="Max Tokens",
        description="The maximum number of tokens to generate in the completion.",
    )
    top_p: float = Field(
        None,
        title="Top P",
        description="An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.",
    )
    frequency_penalty: confloat(ge=-2, le=2) = Field(
        0,
        title="Frequency Penalty",
        description="Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.",
    )
    presence_penalty: confloat(ge=-2, le=2) = Field(
        0,
        title="Presence Penalty",
        description="Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.",
    )
    stop: conlist(str, max_items=4) = Field(
        None,
        title="Stop Sequences",
        description="Up to 4 sequences where the API will stop generating further tokens. The returned text will not contain the stop sequence.",
    )
    logprobs: conint(le=5) = Field(
        0,
        title="Log Probabilities",
        description="Include the log probabilities on the logprobs most likely tokens, as well the chosen tokens. For example, if logprobs is 5, the API will return a list of the 5 most likely tokens. The API will always return the logprob of the sampled token, so there may be up to logprobs+1 elements in the response.",
    )
    suffix: str = Field(
        None,
        title="Suffix",
        description="The suffix that comes after a completion of inserted text. Used with the GP3 Insert Models.",
    )
    logit_bias: Dict[str, confloat(le=100, ge=-100)] = Field(
        {},
        title="Logit Bias",
        description="Modify the likelihood of specified tokens appearing in the completion.",
    )


class AI21PenaltyData(BaseModel):
    scale: confloat(ge=0) = Field(
        0,
        title="Scale",
        description="A positive penalty value implies reducing the probability of repetition. Larger values correspond to a stronger bias against repetition.",
    )

    apply_to_numbers: bool = Field(
        False,
        alias="applyToNumbers",
        title="Apply To Numbers",
        description="Apply the penalty whitespaces and newlines. Determines whether the penalty is applied to the following tokens: '▁', '▁▁', '▁▁▁▁', '<|newline|>'",
    )

    apply_to_punctuations: bool = Field(
        False,
        alias="applyToPunctuations",
        title="Apply To Punctuations",
        description="Apply the penalty to punctuations. Determines whether the penalty is applied to tokens containing punctuation characters and whitespaces, such as ; , !!! or ▁\\[[@.",
    )

    apply_to_stopwords: bool = Field(
        False,
        alias="applyToStopwords",
        title="Apply To Stopwords",
        description="Apply the penalty to numbers. Determines whether the penalty is applied to purely-numeric tokens, such as 2022 or 123. Tokens that contain numbers and letters, such as 20th, are not affected by this parameter.",
    )

    apply_to_whitespaces: bool = Field(
        False,
        alias="applyToWhitespaces",
        title="Apply To Whitespaces",
        description="Apply the penalty to stop words. Determines whether the penalty is applied to tokens that are NLTK English stopwords or multi-word combinations of these words, such as are , nor and ▁We▁have.",
    )

    apply_to_emojis: bool = Field(
        False,
        alias="applyToEmojis",
        title="Apply To Emojis",
        description="Exclude emojis from the penalty. Determines whether the penalty is applied to any of approximately 650 common emojis in the Jurassic-1 vocabulary.",
    )


class AI21GPTConfig(BaseModel):
    engine: Literal["j1-jumbo", "j1-large"] = Field(
        "j1-jumbo",
        title="Engine",
        description="Name of the large language model to use.",
    )

    num_results: conint(gt=0, le=10) = Field(
        1,
        alias="numResults",
        title="Number of results",
        description="Number of completions to sample and return.",
    )
    max_tokens: conint(gt=0, le=4096) = Field(
        200,
        alias="maxTokens",
        title="Max Tokens",
        description="The maximum number of tokens to generate per result.",
    )
    temperature: confloat(ge=0) = Field(
        0.5,
        title="Temperature",
        description="What sampling temperature to use. Higher values means the model will take more risks. Try 0.9 for more creative applications, and 0 (argmax sampling) for ones with a well-defined answer.",
    )
    top_p: float = Field(
        None,
        alias="topP",
        title="Top P",
        description="An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.",
    )
    count_penalty: AI21PenaltyData = Field(
        None,
        alias="countPenalty",
        title="Count Penalty",
        description="Applies a bias against generating tokens that appeared in the prompt or in the completion, proportional to the number of respective appearances",
    )
    frequency_penalty: AI21PenaltyData = Field(
        None,
        alias="frequencyPenalty",
        title="Frequency Penalty",
        description="Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.",
    )
    presence_penalty: AI21PenaltyData = Field(
        None,
        title="Presence Penalty",
        description="Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.",
    )
    stop: conlist(str, max_items=4) = Field(
        None,
        alias="stopSequences",
        title="Stop Sequences",
        description="Up to 4 sequences where the API will stop generating further tokens. The returned text will not contain the stop sequence.",
    )
    logit_bias: Dict[str, confloat(le=100, ge=-100)] = Field(
        {},
        alias="logitBias",
        title="Logit Bias",
        description="Modify the likelihood of specified strings appearing in the completion. more here on format https://studio.ai21.com/docs/api/#logit-bias",
    )
    gpt_logit_bias: Dict[str, confloat(le=100, ge=-100)] = Field(
        {},
        alias="logit_bias",
        title="Logit Bias",
        description="Modify the likelihood of specified strings appearing in the completion. more here on format https://studio.ai21.com/docs/api/#logit-bias",
    )


GPTConfig = Union[OpenAIGPTConfig, AI21GPTConfig]
