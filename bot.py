import datetime
import discord

from openai import OpenAI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

OPENAI_KEY = "Your OpenAI API key"
DISCORD_TOKEN = "Your Discord bot token"
MONGO_URI = "Your MongoDB URI"
MODEL = "Your model ID"
name = "Your name; should be the same as the one you used in construct_dataset.py"

mongo_client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
client = OpenAI(api_key=OPENAI_KEY)

def add_context(user):
    """
    Add up to 10 previous interactions to the user's message
    """
    conversation = conversations.find_one({"user": user})
    if conversation is None:
        return []
    else:
        context = [{
            "role": "system",         
            "content": f"You are roleplaying as a person named {name} on an online chat app. You must respond as if you are this person and never break character.'"
        }]
        past_interactions = conversation['conversation'][-10:]
        for past_interaction in past_interactions:
            context.append(
                {
                    'role': 'user',
                    'content': interactions.find_one({"_id": past_interaction})['message']
                }
            )
            context.append(
                {
                    'role': 'assistant',
                    'content': interactions.find_one({"_id": past_interaction})['response']
                }
            )
        return context
             
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        # Prevent the bot from responding to itself
        if message.author == discord_client.user:
            return
        
        print(f'Message from {message.author}: {message.content}')

        user_message = {
            'role': 'user',
            'content': message.content
        }

        messages = add_context(message.author.id)

        messages.append(user_message)

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.75,
            presence_penalty=0.25,
            frequency_penalty=0.25
        )
        print(response)
        await message.channel.send(response.choices[0].message.content)

        interaction = {
            "message": message.content,
            "response": response.choices[0].message.content,
            "date": datetime.datetime.now(tz=datetime.timezone.utc),
        }
        interaction = interactions.insert_one(interaction).inserted_id

        # Find conversation or create a new one
        conversation = conversations.find_one({"user": message.author.id})
        if conversation is None:
            conversation = {
                "user": message.author.id,
                "conversation": [interaction]
            }
            conversation = conversations.insert_one(conversation).inserted_id
        else:
            conversation = conversations.update_one(
                {"user": message.author.id},
                {"$push": {"conversation": interaction}}
            )

intents = discord.Intents.default()
intents.message_content = True

try:
    mongo_client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = mongo_client["db1"]
interactions = db["interactions"]
conversations = db["conversations"]

discord_client = MyClient(intents=intents)
discord_client.run(DISCORD_TOKEN)
