def detect_greeting(text):
    lowered = text.lower()
    return "!botato" in lowered or "!hi" in lowered or "!hello" in lowered or "!cc" in lowered

def detect_response(text):
    lowered = text.lower()
    return  "!bayna" in lowered
def handle_bot_options():
    return (
        "Here are the commands you can use:\n\n"
        "```"
        "Command           | Description\n"
        "------------------|-----------------------------------------------\n"
        "!timer            | Select a timer depending on what you need.\n"
        "!todo             | Create a to-do list and keep track of your progress.\n"
        "!def [word]       | Find the definitions of a word.\n"
        "!translate [word] | Find the translation of a word in different languages.\n"
        "!dquotes          | Send random quotes while you're working.\n"
        "!quote            | Send one quote.\n"
        "```"
    )

def handle_greeting():
    return "hello bruda i'am ur fav potato with me u can be more focused in studying, soooo ak wajd chikh ? enter '!bayna' to contenu"

def to_do_liste_options():
    return (
        "You can use the following commands:\n\n"
        "```"
        "Command     | Description\n"
        "------------|-----------------------------------------------\n"
        "!add [task] | Add tasks to your to-do list.\n"
        "!done [task]| Mark tasks as completed by their name.\n"
        "!done [num] | Mark tasks as completed by their number.\n"
        "!list       | View your to-do list and progress.\n"
        "```"
    )
def handle_timers_options():
    return (
        "Timer setter:\n\n"
        "```"
        "Mode | Description\n"
        "-----|-----------------------------------------\n"
        "!1   | Get 25 min of studying with 5 min break\n"
        "!2   | Get 50 min of studying with 10 min break\n"
        "!3   | Get 75 min of studying with 15 min break\n"
        "```"
    )

