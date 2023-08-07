from typing import List
from modules.replier_v2.conversational_modules import OpenAIGPTConfig

from modules.replier_v2.intents import *
from modules.replier_v2.message import *
from modules.replier_v2.reminders import ReminderConfig
from modules.replier_v2.status_webhook import StatusIntentData, StatusWebhook


def one_of(*options: str):
    replace_of_backtick = "\`"
    return (
        "[{one_of(["
        + ",".join(
            f"`{option.replace('`', replace_of_backtick)}`" for option in options
        )
        + "])}]"
    )


def ask(*messages, answer_field):
    return AskDefiniteIntent(
        question=messages,
        answer_field=answer_field,
    )


def ask_image(*messages, answer_field):
    return CollectAttachmentsIntent(
        text=[messages], attachment_types=["image"], answer_field=answer_field
    )


def ask_in_options(
    *messages: BotMessageUnion,
    answer_field: str,
    options=["Yes", "No"],
    list_only=True,
    footer="",
    option_type: Literal["button", "list"] = "button",
):
    """Macro for asking questions with button/list options

    :param *messages: Messages to send. Last message must be of type `str`.
    :type *messages: BotMessageUnion

    """
    if len(messages) < 1:
        raise ValueError("Please provide at least one message.")
    if not isinstace(messages[-1], str):
        raise TypeError("Last message must be of type `str`.")
    body = messages[-1]
    messages = messages[:-1]
    return AskDefiniteIntent(
        question=[
            *messages,
            InteractiveMessage(
                type=option_type, body=body, footer=footer, options=options
            ),
        ],
        answer_field=answer_field,
        list_only=list_only,
    )


def say(*messages):
    return SayIntent(text=messages)


def validate_date(*match_not_found_messages):
    if len(match_not_found_messages) < 1:
        match_not_found_messages = [
            one_of(
                [
                    "That's not a real date!",
                    "Hmmm... I don't see a date there. Can you send it again? Make sure its the correct format DD/MM/YY. For example: 15/07/2000",
                ]
            )
        ]
    return AskDefiniteConfig(
        re=r"(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})|(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))|(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})([^\d]|$)",
        match_not_found_message=match_not_found_messages,
    )


def validate_email(*match_not_found_messages):
    if len(match_not_found_messages) < 1:
        match_not_found_messages = [
            one_of(
                [
                    "I think you made a mistake typing your email. Please check and send it again.",
                    "I asked for your email, not this. Please send your email address.",
                    "What is this? I asked for your email ID.",
                    "Hmmm... I don't see an email there. Can you send it again? Make sure its the correct format. For example: person@example.com",
                ]
            )
        ]
    return AskDefiniteConfig(
        re="[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}",
        match_not_found_message=match_not_found_messages,
    )


phone_regex = (
    "(?<!\\d)(\\d{1,2})?[ -]?(\\d{3})[- ]?(\\d{2})[- ]?(\\d{1})[- ]?(\\d{4})(?!\\d)"
)


def validate_phone(*match_not_found_messages):
    if len(match_not_found_messages) < 1:
        match_not_found_message = [
            "Hmmm... I don't see a phone there. Can you send it again?"
        ]
    return AskDefiniteConfig(
        re=phone_regex,
        match_not_found_message=match_not_found_messages,
    )


def validate(re, *match_not_found_messages):
    return AskDefiniteConfig(
        re=re,
        match_not_found_message=match_not_found_messages,
    )


def no_match_messages(*messages):
    return AskDefiniteConfig(not_in_list_message=messages)


def next_step(step):
    return NextConfig(next=step)


def ocr_document_flow(
    doctype: Literal["pan", "aadhar"],
    next_step_on_finish: str,
    ocr_failed_messages: List = None,
):
    if doctype == "pan":
        document_name = "PAN Card"
        document_id_name = "PAN"
        sample_image = "https://media.discordapp.net/attachments/975712560114450432/989447953062166579/unknown.png"
    elif doctype == "aadhar":
        document_name = "Aadhar Card"
        document_id_name = "Aadhar Number"
        sample_image = "https://media.discordapp.net/attachments/975712560114450432/989458876317433897/unknown.png"
    else:
        raise NotImplemented
    if ocr_failed_messages is None:
        ocr_failed_messages = [
            f"I'm not able to read your {document_id_name} from this picture. Can you please send a clear picture of the *front part* of *your {document_name} card*. Make sure it is well it and the picture is clear."
        ]

    return {
        f"ask-{doctype}": ask_image(
            f"Please send a picture of your {document_name}.", doctype
        )
        + say(
            RemoteMediaMessage(
                type="image",
                link=sample_image,
                caption="It should look something like this.",
            )
        ),
        f"{doctype}-flatten": ExpressionIntent(
            expression=f"{doctype}[0]",
            answer_field=f"{doctype}_file",
        ),
        f"{doctype}-attempt-add": ExpressionIntent(
            expression=f"jq> .{doctype}attempt + 1", answer_field=f"{doctype}attempt"
        ),
        f"{doctype}-ocr": HTTPRequestIntent(
            url=f"http://127.0.0.1:4000/{doctype}",
            params={"url": "{" + doctype + "_file}"},
            answer_field=f"{doctype}-ocr",
        ),
        f"{doctype}-check-success": {
            "type": "condition",
            "condition": f'"{doctype}-ocr".success && "{doctype}-ocr".response.is_document_valid && "{doctype}-ocr".response.document_details.identification_number != null',
            "if": next_step_on_finish,
            "else": f"document-{doctype}-failed-check-attempt",
        },
        f"document-{doctype}-failed-check-attempt": ConditionIntent(
            condition=f"jq> .{doctype}attempt >= 2",
            if_=f"{doctype}-failed-too-many-times",
        ),
        f"document-{doctype}-failed": say(*ocr_failed_messages)
        + next_step(f"ask-{doctype}"),
        f"{doctype}-failed-too-many-times": say(
            f"Looks like this isn't working. I'll have someone ask for you {document_name} later."
        )
        + next_step(next_step_on_finish),
    }


def classify_yesno(*collect, answer_field):
    return GPTGenerateIntent(
        template="classify-yes-no-maybe-neither",
        collect=collect,
        answer_field=answer_field,
    )


def jq_match_yes(answer_field):
    return f'."{answer_field}" | test("yes|yeah|yep|ok|sure|ya|haa|jaroor|zaroor|theek|why not|i guess|avnu"; "i")'


def jq_all(*answer_fields, equals="true"):
    return " and ".join(
        [f'."{answer_field}" == {equals}' for answer_field in answer_fields]
    )


def jq_any(*answer_fields, equals="true"):
    return " or ".join(
        [f'."{answer_field}" == {equals}' for answer_field in answer_fields]
    )


def jq_match_no(answer_field):
    return f'."{answer_field}" | test("no|na"; "i")'


def jq_match(answer_field, regex, options="i"):
    return f'."{answer_field}" | test("{regex}"; "{options}")'


def status(status, data=None):
    if data is None:
        data = {}
    return StatusIntentData(status=status, data=data)


def classify_yes_no_static(answer_field):
    return {
        f"{answer_field}-check-yes": ConditionIntent(
            condition="jq> " + jq_match_yes(answer_field), if_=f"{answer_field}-yes"
        ),
        f"{answer_field}-check-no": ConditionIntent(
            condition="jq> " + jq_match_no(answer_field),
            if_=f"{answer_field}-no",
            else_=f"{answer_field}-yes-no-done",
        ),
        f"{answer_field}-yes": ExpressionIntent(
            expression="`Yes`", answer_field=answer_field
        )
        + next_step(f"{answer_field}-yes-no-done"),
        f"{answer_field}-no": ExpressionIntent(
            expression="`No`", answer_field=answer_field
        )
        + next_step(f"{answer_field}-yes-no-done"),
        f"{answer_field}-yes-no-done": say(),
    }


def classify_yes_no(collect, answer_field):
    return {
        f"{answer_field}-check-yes": ConditionIntent(
            condition="jq> " + jq_match_yes(answer_field), if_=f"{answer_field}-yes"
        ),
        f"{answer_field}-check-no": ConditionIntent(
            condition="jq> " + jq_match_no(answer_field),
            if_=f"{answer_field}-no",
            else_=f"{answer_field}-yes-no-classify",
        ),
        f"{answer_field}-yes": ExpressionIntent(
            expression="`Yes`", answer_field=f"{answer_field}-yes-no-classify"
        )
        + next_step(f"{answer_field}-yes-no-done"),
        f"{answer_field}-no": ExpressionIntent(
            expression="`No`", answer_field=f"{answer_field}-yes-no-classify"
        )
        + next_step(f"{answer_field}-yes-no-done"),
        f"{answer_field}-yes-no-classify": classify_yesno(
            collect, answer_field=answer_field + "-yesno-gpt"
        ),
        f"{answer_field}-yes-no-classify-save": ExpressionIntent(
            expression=f'jq> if (."{answer_field}-yesno-gpt".classification // "unsure" | ascii_downcase) == "yes" then "Yes" else "No" end',
            answer_field=f"{answer_field}-yes-no-classify",
        ),
        f"{answer_field}-yes-no-done": say(),
    }


def ask_if_not_there(body, answer_field, acknowledgement="", next_step=None):
    """_summary_: Ask if not there

    Args:
        body (string): The body of the message
        answer_field (str): The answer field
        next_step (str): The next intent


    Returns:
        Dict[Intents]: The intents you can overwrite the {answer_field}_done_asking to condition or expression or anything else
    """
    return {
        f"check_if_{answer_field}_is_there": ConditionIntent(
            **{
                "condition": 'jq> ."answer_field"//false'.replace(
                    "answer_field", answer_field
                ),
                "if": f"{answer_field}_done_asking",
                "else": f"ask_{answer_field}",
            }
        ),
        f"ask_{answer_field}": AskDefiniteIntent(
            question=[body],
            answer_field=answer_field,
        ),
        f"{answer_field}_done_asking": SayIntent(
            text=[acknowledgement], next_=next_step
        ),
    }


def if_not_there(*intents, answer_field, acknowledgement, next_step=None):
    """_summary_: Ask if not there

    Args:
        intents (List[Intent]): Intents to run if answer_field is falsy
        answer_field (str): The answer field
        acknowledgement (Intent): Answer to

    Returns:
        Dict[Intent]: The intents you can overwrite the {answer_field}_done_asking to condition or expression or anything else
    """
    return {
        f"check_if_{answer_field}_is_there": ConditionIntent(
            **{
                "condition": 'jq> ."answer_field"//false'.replace(
                    "answer_field", answer_field
                ),
                "if": f"{answer_field}_done_asking",
                "else": f"intent_{answer_field}_0",
            }
        ),
        **{f"intent_{answer_field}_{i}": intent for i, intent in enumerate(intents)},
        f"{answer_field}_ack": acknowledgement,
        f"{answer_field}_done_asking": say(""),
    }


def generate_skip_table(steps, first_step="check-all"):
    check_if = re.compile("check_if_(.*)_is_there")
    done_asking = re.compile("(.*)_done_asking")
    storing = False
    step_queue = []
    skip_table = {}
    for step in steps:
        matches = check_if.match(step)
        if matches is not None:
            skip_table.update({skip_from: step for skip_from in step_queue})
            step_queue = []
            storing = True
        matches = done_asking.match(step)
        if matches is not None:
            storing = False
        if storing:
            step_queue.append(step)
    skip_table.update({skip_from: first_step for skip_from in step_queue})
    return skip_table


def initialize_variables(**variables):
    """
    Expression macro to initialize variables based on types in values
    """
    defaults = {
        "str": "",
        "int": "0",
        "bool": "false",
        "array": "[]",
        "object": "{}",
    }
    return {
        f"init_{answer_field}": ExpressionIntent(
            answer_field=answer_field,
            expression=f'"{answer_field}"//{defaults.get(variable_type, "")}',
        )
        for answer_field, variable_type in variables.items()
    }


def discordhook(url, content, answer_field="webhook"):
    return HTTPRequestIntent(
        url=url,
        method="POST",
        body=HTTPBody(
            body_type="json",
            data={"content": content},
        ),
        answer_field=answer_field,
    )
