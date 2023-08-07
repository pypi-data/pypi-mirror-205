from fluidsdk.pyrite import FlowBuilder
from fluidsdk.pyrite.library import Context, ask, say, GPTGenerate
from fluidsdk.templates import GPTGenerateTemplate
import json

flow = FlowBuilder("test_flow", "Test Flow", token="SUPER_SECRET_ACCESS_TOKEN")

# The GPTGenerate intent makes a request using a template. Below, we make the required changes based on our needs.
flow.include_template(
    GPTGenerateTemplate(
        template_id="version-test",
        re="(.*)",
        results=["poem"],
        pre_prompt="",
        user_prefix="{.name}",
        bot_prefix="Mom:",
        post_prompt="\nWrite a poem about what {.name} had for lunch and where they live:",
    )
)


# Context stores the results of the ask intents and repurposes them for the GPTGenerate intent.
@flow.subroutine
def poem():
    global poem
    with Context() as test_context:
        place = ask("Where do you live?")
        had_for_lunch = ask("What did you have for lunch?")

    poem = GPTGenerate(template="version-test", context=test_context)
    say(
        "Here's a poem for you!", "{poem.poem}}"
    )  # Uses the result of GPTGenerate to share the poem with the user.


@flow.subroutine
def start():
    say("Hello")
    poem()  # Includes the poem subroutine in the flow.
    say("Bye!")


print(flow.build())
