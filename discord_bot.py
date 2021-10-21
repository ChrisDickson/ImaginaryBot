import discord
from discord import Embed
import requests
import os
import asyncpraw
from random import randint
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot_tag = "!!"


reddit = asyncpraw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('SECRET_TOKEN'),
    username = os.getenv('USERNAME'),
    password = os.getenv('PASSWORD'),
    user_agent="testscript by me to learn more about async python"
)
client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith(bot_tag):
        sub_request = message.content[2:]
        out_message = ""
        if " " in sub_request:
            out_message = f"I'm sorry {message.author.display_name}, I can only handle one request per message."
            await message.channel.send(out_message)
        else:
            sub_name = "imaginary"+sub_request
            try:
                subreddit = await reddit.subreddit(sub_name, fetch=True)
                submission_list = [submission async for submission in subreddit.top(limit=100) if not submission.stickied]
                selector = randint(0, len(submission_list)-1)
                post = submission_list[selector]
                embed = Embed(title=post.title)
                embed.set_image(url=post.url)

                await message.channel.send(embed=embed)
            except Exception:
                out_message = f"Could not find the subreddit /r/{sub_name}, please check again!"
                await message.channel.send(out_message)


client.run(DISCORD_TOKEN)