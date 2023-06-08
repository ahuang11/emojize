import panel as pn
import openai

pn.extension(design="bootstrap")

NAV_JS_CODE = """
    var currentDomain = window.location.href;
    var regex = /#\/slide-(\d+)/;
    var match = currentDomain.match(regex);
    if (match) {
        var slideNumber = parseInt(match[1]);
        if (reverse) {
            var newSlideNumber = 0;
        }
        else {
            var newSlideNumber = 1;
        }
        console.log(newSlideNumber);
        var newPage = currentDomain.replace(regex, "#/slide-" + newSlideNumber);
        window.location.href = newPage;
    }
    else {
        currentDomain += "#/slide-1";
        window.location.href = currentDomain;
    }
"""


def emojize(event):
    return_button = pn.widgets.Button(
        name="🔙 Let's go back!",
        align="center",
    )
    return_button.js_on_click(code=NAV_JS_CODE, args={"reverse": True})

    openai_key = openai_key_input.value
    user_text = user_text_input.value
    emoji_count = emoji_count_input.value
    if not openai_key or not user_text:
        return pn.Column(
            "<h3>Please enter your OpenAI Key 🔑 and some text to add emojis to!</h3>",
            return_button,
        )

    openai.api_key = openai_key

    # Define the prompt
    system = f"""
    Infuse and sprinkle exactly {emoji_count} relevant emojis within the user's
    text below. Make sure the placement is logical and try not to place the
    emojis next to each other. No chit-chat.

    User's Text:
    {user_text}
    """.strip()

    # Use the OpenAI API to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system},
        ],
        temperature=0.488,
    )

    # Return the response text
    emojized_content = response.choices[0]["message"]["content"].strip()
    copy_button = pn.widgets.Button(
        name="📋 Copy to Clipboard",
        align="center",
        button_type="primary",
    )
    copy_button.jscallback(
        args={"content": emojized_content},
        value="content",
        callback="""
        navigator.clipboard.writeText(content);
        """,
    )
    return pn.Column(
        f"<h3>{emojized_content}</h3>",
        pn.Row(return_button),
    )


# Define the widgets
openai_key_input = pn.widgets.PasswordInput(
    name="OpenAI Key",
    placeholder="Enter your OpenAI Key",
    sizing_mode="stretch_width",
)
user_text_input = pn.widgets.TextInput(
    name="User Text",
    placeholder="Enter some text to add emojis to!",
    value="I'm excited you're here!",
    sizing_mode="stretch_width",
)
emoji_count_input = pn.widgets.Spinner(
    name="Emojis",
    width=50,
    value=2,
    start=1,
    end=10,
)
submit_button = pn.widgets.Button(
    name="🤩 Let's see the emojis!",
    margin=(20, 10),
    button_type="primary",
    disabled=True,
    align="center",
)
submit_button.js_on_click(code=NAV_JS_CODE, args={"reverse": False})
emojized_text_output = pn.panel(
    pn.bind(
        emojize,
        submit_button,
    ),
    loading_indicator=True,
)

# Create a Panel to display the widgets
main = pn.WidgetBox(
    pn.Column(
        "<h3>🙌 Let AI find the right emojis, for you!</h3>",
        openai_key_input,
        pn.Row(
            user_text_input,
            emoji_count_input,
        ),
        submit_button,
        max_width=500,
    ),
    emojized_text_output,
    max_width=500,
)

slides = pn.template.SlidesTemplate(
    title="emojize",
    main=main,
    reveal_config={
        "center": False,
        "keyboard": False,
        "pause": False,
        "controlsLayout": "edges",
    },
)

# Serve the Panel
slides.servable()
