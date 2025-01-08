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

load_dotenv(dotenv_path=".env")
groq_api = "API1"
api_key = os.environ.get(groq_api)
TOKEN = os.environ.get("TOKEN_lora")


# Instructions for the bot's behavior
instructions = ""
file_path = "configs/instructions_lora.txt"
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        instructions = file.read()
else:
    print("Instructions file not found. Please provide instructions in config/instructions.txt")
    exit(1)


# Models and context management
groq_model =  "llama-3.3-70b-versatile"
channel_context = {}  # Stores recent messages for each channel
channel_models = {}  # Stores assigned models for each channel
accepted_channels = []
short_memory = {} # temporary memory 
messages_limit = 20 # After how many message the old messages will start deleting from "short_memory" ?


# Message handling queue
message_queue = deque()
processing = False  # Flag to indicate if the queue is being processed


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
    global short_memory, groq_api
    
    client = Groq(api_key=api_key)
    context= (
      [{"role": "system", "content": instructions,}] + short_memory[message.author.id] + [{"role": "user", "content": message.content,}]
      )
    output = "" # Ai response will be saved in  this variable 
    for i in range(5):
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
        except Exception as e:
          print(f"Saving conversation in short memory error: {e}")
        # break the loop
        break
      except Exception as api_error:
        print(f"Groq API error: {api_error}")
        new_api = switch_API(groq_api)
        groq_api = new_api
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
        await asyncio.sleep(random.uniform(5, 10))
        await handle_message(client, message)
        await asyncio.sleep(random.uniform(1, 2))  # Delay between responses
    processing = False

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
      await asyncio.sleep(random.uniform(3, 8))
      try:
        if isinstance(message.channel, discord.DMChannel):
          await message.channel.send(reply)
        else:
          await message.reply(reply)
      except Exception as e:
          print(f"Error sending reply: {e}")
  except Exception as e:
    print(e)


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_message(self, message):
        global message_queue
        # Check if the message not from the self-bot and check if acceptable channel.
        if message.author == self.user or message.channel.id not in map(int, accepted_channels):
            if message.content.startswith("_ _"):
                accepted_channels.append(str(message.channel.id))
                print("Channel added!")
            return

        # Ensure the bot is mentioned in public channels
        if not isinstance(message.channel, discord.DMChannel) and self.user not in message.mentions:
            return

        # Add message to the queue
        message_queue.append(message)
        await process_message_queue(self)

client = MyClient()
client.run(TOKEN)