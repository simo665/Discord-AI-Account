import discord
from groq import Groq
from dotenv import load_dotenv
import os
import asyncio
import random
from discord.ext import commands
import time
from collections import deque
from utilities.ChangeAPI import switch_API
from utilities.help import help_message
import json


prefix = os.environ.get("PRE-FIX", ".")
bot = commands.Bot(command_prefix=prefix, help_command=None)

file_path = "configs/instructions.txt"
def load_instructions():
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            instructions = file.read()
            return instructions if instructions else ""
    else:
        print("Instructions file not found. Please provide instructions in config/instructions.txt")
        return ""

# Load the accepted channels from a file
def load_accepted_channels():
    try:
        with open("configs/accepted_channels.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exists
        
# Load the blocklist user from a file
def load_blocked_users():
    try:
        with open("configs/blocked_users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exists
        

def load_conversation_history():
    file_path = "user/conversations.json"
    try:
        if os.path.exists(file_path):
            # load file 
            with open(file_path, "r") as f:
                data = json.load(f)
                return data
        else:
            return {}
    except Exception as e:
        print(f"Error loading contact: {e}")
        
def save_conversation_history():
    file = "user/conversations.json"
    os.makedirs("user", exist_ok=True)
    try:
        with open(file, "w") as f:
            json.dump(short_memory, f, indent=2)
    except Exception as e:
        print(f"Error saving contact: {e}")
        
# Requirements 
load_dotenv()
groq_api = "API1"
api_key = os.environ.get(groq_api)
TOKEN = os.environ.get("TOKEN")
owner_id = os.environ.get("OWNER_ID", 0)  # without owner id you can't execute some commands that can only be used by the owner.


# Instructions for the bot's behavior
instructions = load_instructions()


# Models and context management
groq_model =  "llama-3.3-70b-versatile"
channel_context = {}  # Stores recent messages for each channel
channel_models = {}  # Stores assigned models for each channel
accepted_channels = load_accepted_channels() # The only channels where the AI self-bot will respond 
blocked_users = load_blocked_users() # Blocked user will be ignored by the ai. 
short_memory = load_conversation_history() # temporary memory 
messages_limit = 20 # After how many message the old messages will start deleting from "short_memory" ?
# words that the bot will respond to even if it not being mentioned 
engage_keywords = os.environ.get("ENGAGE_KEYWORDS", "").split(",")
# Message handling queue
message_queue = deque()
processing = False  # Flag to indicate if the queue is being processed


def save_accepted_channels():
    with open("configs/accepted_channels.json", "w") as file:
        json.dump(accepted_channels, file)
        
def save_blocked_users():
    with open("configs/blocked_users.json", "w") as file:
        json.dump(blocked_users, file)




async def load_context(message_obj, bot_name, limit=15):
  """Fetches recent messages from the channel to build context."""
  try: 
    temp_messages = []  # Temporary list to collect messages
    async for message in message_obj.channel.history(limit=limit):  # Collect messages normally
      if message.author.name == bot_name:
        temp_messages.append({"role": "assistant", "content": message.content})
      else:
        temp_messages.append({"role": "user", "content": message.content})
    temp_messages.reverse()
    messages_history = temp_messages
    short_memory[message_obj.author.id] = messages_history
    print("history memory done!")
  except Exception as e:
    print(f"error loafing the context: {e}")

def short_memory_limit(user_id):
  """Delete old messages if the short memory length hits the limit"""
  global short_memory
  if len(short_memory[user_id]) >= messages_limit:
    short_memory[user_id].pop(0)

def generate_reply(message, bot):
    """Generates a reply using the model and context."""
    global short_memory, api_key
    
    client = Groq(api_key=api_key)
    context= (
      [{"role": "system", "content": instructions,}] + short_memory[message.author.id] + [{"role": "user", "content": message.content,}]
      )
    output = "" # Ai response will be saved in  this variable 
    for i in range(3):
      try:     # handle api errors 
        chat_completion = client.chat.completions.create(
            messages=context,
            model=groq_model,
            stream=False,
        )
        output = chat_completion.choices[0].message.content
        if output == "none" or output == "none0":
          return ""
        try: # handle saving errors temporary 
          short_memory_limit(message.author.id)
          short_memory[message.author.id].append({"role": "user", "content": message.content})
          short_memory[message.author.id].append({"role": "assistant", "content": output})
          save_conversation_history()
        except Exception as e:
          print(f"Saving conversation in short memory error: {e}")
        # break the loop
        break
      except Exception as api_error:
        print(f"Groq API error: {api_error}")
        new_api = switch_API(groq_api)
        api_value = os.environ.get(new_api)
      
    # Return response 
    return output
    

async def process_message_queue(client):
    """Processes the message queue sequentially with delays."""
    global processing
    if processing:
        return  # Avoid multiple workers processing the queue

    processing = True
    while message_queue:
        message = message_queue.popleft()
        await asyncio.sleep(random.uniform(5, 15))
        await handle_message(client, message)
    processing = False


def process_selfbot_commands(message):
    if message.content == ".a":
        accepted_channels = load_accepted_channels()
        # if a channel id provided 
        channel_id = message.channel.id
        if channel_id:
             # Check if it's already in the list
            if str(channel_id) in accepted_channels:
                print(" • Channel id is already in the accepted channels list")
                return 
            # Append channel id
            accepted_channels.append(str(channel_id))
            save_accepted_channels()
            print(" • Channel id is added successfully!")
            return
    if message.content == ".r":
        accepted_channels = load_accepted_channels()
        # if a channel id provided 
        channel_id = message.channel.id
        if channel_id:
             # Check if it's already in the list
            if not str(channel_id) in accepted_channels:
                print(" • Channel id is not in the accepted channels list to be removed.")
                return 
            # Append channel id
            accepted_channels.remove(str(channel_id))
            save_accepted_channels()
            print(" • Channel was removed successfully!")
            return

async def handle_message(client, message):
  """Handles an individual message."""
  try:
    async with message.channel.typing():
      # Fetch recent context
      if message.author.id not in short_memory:
        short_memory[message.author.id] = []
        if isinstance(message.channel, discord.DMChannel):
          await load_context(message, client.user.name)
 
      # Generate a reply
      reply = generate_reply(message=message, bot=client)
      if not reply:
        return 
      await asyncio.sleep(random.uniform(5, 15))
      try:
        if isinstance(message.channel, discord.DMChannel):
          await message.channel.send(reply)
        else:
          await message.reply(reply)
      except Exception as e:
          print(f"Error sending reply: {e}")
  except Exception as e:
    print(e)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    

@bot.event
async def on_message(message):
    global message_queue, accepted_channels
    # Check if it's a blocked user
    blocked_users = load_blocked_users()
    if str(message.author.id) in blocked_users:
        return 
    
    # Check if it's a command 
    if message.content.startswith(prefix):
        try:
            if message.author == bot.user:
                process_selfbot_commands(message)
                return 
            await bot.process_commands(message)
            print("command detected")
            return 
        except Exception as e:
            print(e)
    
    # Check if the message not from the self-bot and check if acceptable channel.
    if message.author == bot.user:
        return 
    
    accepted_channels = load_accepted_channels()
    if str(message.channel.id) not in accepted_channels:
        return 
   
    # Ensure the bot is mentioned in public channels
    if not isinstance(message.channel, discord.DMChannel) and bot.user not in message.mentions:
        for keyword in engage_keywords:
            if keyword.lower() in message.content.lower():
                break 
            else:
                return

    # Add message to the queue
    message_queue.append(message)
    await process_message_queue(bot)

async def load_cogs():
    # Load all cogs in the "cogs" directory
    try: 
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")
    except Exception as e:
        print("Error loading extensions: ", e)
    
if __name__ == "__main__":
    asyncio.run(load_cogs())
    asyncio.run(bot.run(token=TOKEN))