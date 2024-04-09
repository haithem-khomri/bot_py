import discord
from discord import Intents, Message
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import asyncio
import responses 
from googletrans import Translator
import traceback
import requests
import random
from PyDictionary import PyDictionary

translator = Translator()
to_do_list = {}
prefix = "!" 

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
intents.messages = True  # Enable message-related events
intents.guilds = True  # Enable guild-related events
intents.members = True  # Enable member-related events

#initialisations
send_quotes_flag = False
current_timer = None
random_message_timer = None
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)

#ayalns work random word with dcefinition everyday

# Function to fetch a random word
def fetch_random_word():
    try:
        url = "https://random-word-api.herokuapp.com/word"
        response = requests.get(url)
        if response.status_code == 200:
            words = response.json()
            return words[0]  # Return the first word from the list
        else:
            print(f"Failed to fetch random word. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching random word: {e}")
        return None

# Function to get def of the word
def get_definitions(word):
    try:
        dictionary = PyDictionary()
        definitions = dictionary.meaning(word)
        return definitions
    except Exception as e:
        print(f"An error occurred while fetching definitions: {e}")
        return None

@client.event
async def on_ready():
    print(f'{client.user} is ready')


@client.event
async def on_message(message: Message):
    global current_timer
    global send_quotes_flag

    content_lower = message.content.lower()
    #check if the message was send from user or bot
    if message.author == client.user:
        return
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')

    if responses.detect_greeting(user_message):
        await message.channel.send(responses.handle_greeting())
    elif responses.detect_response(user_message):
        await message.channel.send(responses.handle_bot_options())
    elif user_message.startswith( f"{prefix}translate"):
        await translate_message(message)
    elif user_message.startswith( f"{prefix}def"):
        await define_message(message)
    elif user_message.startswith( f"{prefix}timer"):
        await message.channel.send(responses.handle_timers_options())
    elif user_message.startswith( f"{prefix}todo"):
        await message.channel.send(responses.to_do_liste_options())
    elif message.content.startswith(f"{prefix}add"):
        tasks = message.content.split(maxsplit=1)[1].strip()
        added_tasks = 0
        for task in tasks.splitlines():
            if task.lower() != "done":
                to_do_list[task] = False
                added_tasks += 1
        await message.channel.send(f"Added {added_tasks} tasks to your to-do list!")
    elif message.content.startswith(f"{prefix}done"):
        numbers = message.content.split(maxsplit=1)[1].strip().split()
        marked_tasks = 0
        for number in numbers:
            try:
                index = int(number) - 1  # Convert to 0-based index
                task = list(to_do_list.keys())[index]
                if task in to_do_list:
                    to_do_list[task] = True
                    marked_tasks += 1
                    await message.channel.send(f"Marked '{task}' as done!")
                else:
                    await message.channel.send(f"Task number {number} not found in your list.")
            except (ValueError, IndexError):
                await message.channel.send(f"Invalid task number: {number}")
        if marked_tasks > 0:
            await update_progress(to_do_list, message.channel)  # Update progress after marking done
    elif message.content.startswith(f"{prefix}list"):
        await view_list(message.channel)
    elif content_lower.startswith('!quote'):
        await get_quote(message.channel)
    elif content_lower.startswith(('!dquotes')):
        send_quotes_flag = True
        await message.channel.send('Good Luck and Have Fun!')
        await send_quotes.start(message.channel)

    else:
        response = await handle_user_response(user_message, message)
        await message.channel.send(response)




async def handle_user_response(user_input, message):
    global current_timer, random_message_timer

    # Reset the current mode and cancel existing timers
    current_mode = None
    if current_timer:
        current_timer.cancel()

    if "!1" in user_input:
        await message.channel.send("You've chosen mode 1: 25 min of studying with 5 min break.")
        current_timer = asyncio.create_task(timer(25*60, message))
        await current_timer
        await message.channel.send("You did it! Take a 5-minute break.")
        current_timer = asyncio.create_task(timer(5*60, message))
        await current_timer
        await message.channel.send("Back to studying!")
        current_timer = asyncio.create_task(timer(25*60, message))
        await current_timer
        await message.channel.send("You did it! Take a 5-minute break.")
        current_timer = asyncio.create_task(timer(5*60, message))
        await current_timer
        await message.channel.send("Back to studying!")
        current_timer = asyncio.create_task(timer(25*60, message))
        await current_timer
        await message.channel.send("You did it! Take a 5-minute break.")
        current_timer = asyncio.create_task(timer(5*60, message))
        await current_timer
        return "select which mode again!"
    elif "!2" in user_input:
        await message.channel.send("You've chosen mode 2: 50 min of studying with 10 min break.")
        current_timer = asyncio.create_task(timer(50 * 60, message))
        await current_timer
        await message.channel.send("You did it! Take a 10-minute break.")
        current_timer = asyncio.create_task(timer(10 * 60, message))
        await current_timer
        await message.channel.send("Back to studying!")
        current_timer = asyncio.create_task(timer(50 * 60, message))
        await current_timer
        await message.channel.send("You did it! Take a 10-minute break.")
        current_timer = asyncio.create_task(timer(10 * 60, message))
        await current_timer
        await message.channel.send("Back to studying!")
        current_timer = asyncio.create_task(timer(50 * 60, message))
        await current_timer
        await message.channel.send("You did it! Take a 10-minute break.")
        current_timer = asyncio.create_task(timer(10 * 60, message))
        await current_timer
        return "select which mode again!"
    elif "!3" in user_input:
        await message.channel.send("You've chosen mode 2: 50 min of studying with 10 min break.")
        current_timer = asyncio.create_task(timer(75 * 60, message))
        await current_timer
        await message.channel.send("You did it! Take a 10-minute break.")
        current_timer = asyncio.create_task(timer(15 * 60, message))
        await current_timer
        await message.channel.send("Back to studying!")
        current_timer = asyncio.create_task(timer(75 * 60, message))
        await current_timer
        await message.channel.send("You did it! Take a 10-minute break.")
        current_timer = asyncio.create_task(timer(15 * 60, message))
        await current_timer
        await message.channel.send("Back to studying!")
        current_timer = asyncio.create_task(timer(75 * 60, message))
        await current_timer
        await message.channel.send("You did it! Take a 10-minute break.")
        current_timer = asyncio.create_task(timer(15 * 60, message))
        await current_timer
        return "select which mode again!"
    else:
        return "didn't get u tap [!bayna] to get your commands list again"
    
async def timer(duration, message):
    await asyncio.sleep(duration)
    await message.channel.send("Time's up!")
#minen
async def translate_message(message):
    user_message = str(message.content)
    content = user_message[len('!translate'):].strip()  # Correct command prefix
    print("Received message:", content)
    await message.channel.send("Please send the language code of the desired language "
                               "(e.g., en for English, es for Spanish, fr for French, de for German). "
                               "Send 'stop' to stop translating.")

    def check(m):
        return m.author == message.author and m.channel == message.channel and m.content.lower() in ['stop', 'en', 'es', 'fr', 'de']  # Check for valid language codes or 'stop'

    try:
        msg = await client.wait_for('message', check=check, timeout=30)  # Wait for user's response

        if msg.content.lower() == 'stop':
            await message.channel.send("Translation stopped.")
            return

        dest_lang = msg.content.lower()

        translation = translator.translate(content, dest=dest_lang)
        translated_text = translation.text if translation else None

        if translated_text:
            print(f"Translated message ({dest_lang}): {translated_text}")
            await message.channel.send(f"Translated message ({dest_lang}): {translated_text}")
        else:
            await message.channel.send("Translation failed. Please try again.")

    except asyncio.TimeoutError:
        await message.channel.send("Translation request timed out. Please try again.")

    except Exception as e:
        traceback.print_exc()
        print("Translation Error:", e)
        await message.channel.send("An error occurred during translation. Please try again later.")
#aya
async def update_progress(todo_list, channel):
    """Calculates and sends a message with the current progress."""
    completed = sum(value for value in todo_list.values())
    total = len(todo_list)
    progress = (completed / total) * 100
    await channel.send(f"Progress: {progress:.2f}% ({completed}/{total} tasks completed)")
async def view_list(channel):
    """Displays the to-do list and progress in the channel."""
    if not to_do_list:
        await channel.send("Your to-do list is empty.")
        return
    completed_tasks = sum(1 for task in to_do_list.values() if task)
    total_tasks = len(to_do_list)
    progress = (completed_tasks / total_tasks) * 100
    message_content = "**To-Do List:**\n"
    for i, (task, done) in enumerate(to_do_list.items(), start=1):
        status = "✅" if done else "❌"
        message_content += f"{status} {task}\n"
    message_content += f"\nProgress: {progress:.2f}% ({completed_tasks}/{total_tasks})"
    await channel.send(message_content)

#doua
@tasks.loop(minutes=1)  # Adjust the interval as needed
async def send_quotes(channel):
    print("Sending quotes...") 
    quote_file_paths = [
        "C:\\Users\\haith\\Desktop\\discord-bot\\quotes.txt",
        "C:\\Users\\haith\\Desktop\\discord-bot\\algerianProverbs.txt",
    ]
    for file_path in quote_file_paths:
        quote = get_random_quote(file_path)
        msg = await channel.send(quote)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await asyncio.sleep(1)  

def get_random_quote(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        quotes = file.readlines()
        return random.choice(quotes).strip()
async def get_quote(channel):
    quote_file_paths = [
        "C:\\Users\\haith\\Desktop\\discord-bot\\quotes.txt",
        "C:\\Users\\haith\\Desktop\\discord-bot\\algerianProverbs.txt",
    ]
    for file_path in quote_file_paths:
        quote = get_random_quote(file_path)
        await channel.send(quote)
@bot.command()
async def stop(ctx):
    global send_quotes_flag
    send_quotes_flag = False
    await ctx.send("Quotes stopped.")
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I don't recognize that command.")

#ayals
async def define_message(message):
    user_message = str(message.content)
    word = user_message[len('!def'):].strip().lower() # Correct command prefix
    

    definitions = get_definitions(word)

    if definitions:
        response = f"Definitions of '{word}':\n"
        for part_of_speech, meanings in definitions.items():
            response += f"{part_of_speech.capitalize()}:\n"
            response += "\n".join(meanings) + "\n"
        await message.channel.send(response)
    else:
        await message.channel.send(f"No definitions found for '{word}'")

    await client.process_commands(message)
@tasks.loop(hours=24)
async def word_of_the_day():
    word_of_the_day = fetch_random_word()
    if word_of_the_day:
        definition = get_definitions(word_of_the_day)
        if definition:
            channel_id = 1219786513605460030 
            channel = client.get_channel(channel_id)
            if channel:
                try:
                    await channel.send(f"Word of the Day: {word_of_the_day}\nDefinition: {definition}")
                except Exception as e:
                    print(f"Failed to send word of the day message: {e}")
            else:
                print("Failed to find channel.")
        else:
            print(f"No definition found for '{word_of_the_day}'")
    else:
        print("Failed to fetch word of the day.")


#haithem
async def background_tasks():
    await client.wait_until_ready()  # Wait until the bot is fully ready
    while True:
        if current_timer:
            await current_timer
        await asyncio.sleep(1)  # Sleep briefly to prevent CPU usage


@client.event
async def on_disconnect():
    send_quotes.stop()

@word_of_the_day.before_loop
async def before_word_of_the_day():
    await client.wait_until_ready()  # Wait until the bot is fully ready before starting the task

async def main():
    await client.start(TOKEN)
    await word_of_the_day()
    word_of_the_day.start()  # Start the background task to send random word
    client.loop.create_task(background_tasks())  # Start the background tasks
    await client.connect()

if __name__ == "__main__":
    asyncio.run(main())