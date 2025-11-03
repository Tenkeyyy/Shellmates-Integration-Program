from discord.ext import commands
import discord
import random
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
uri = os.getenv('URI')
TOKEN = os.getenv('DISCORD_TOKEN')
client = MongoClient(uri)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
@bot.command()
async def hello(message):
    await message.channel.send(f"Hello {message.author.mention} !")
@bot.command()
async def dbs(message):
    dbs = client.list_database_names()
    await message.channel.send(f"Here is the names of your database : {dbs}")
@bot.command()
async def fact(message):
    db = client.facts
    collections = db.list_collection_names()
    collection = db[random.choice(collections)]
    fact = collection.aggregate([{"$sample": {"size": 1}}]).next()
    await message.channel.send(f"Here is your fun fact {message.author.mention} : {fact["name"]} : {fact["fact"]} ")
@bot.command()
async def quiz(message):
    db = client.facts
    collection = db[random.choice(db.list_collection_names())]
    fact1 = collection.aggregate([{"$sample": {"size": 1}}]).next()
    fact2 = collection.aggregate([{"$sample": {"size": 1}}]).next()
    fact3 = collection.aggregate([{"$sample": {"size": 1}}]).next()
    while(fact2 == fact1):
        fact2 = collection.aggregate([{"$sample": {"size": 1}}]).next()
    while(fact3 == fact2 or fact3 == fact1):
        fact3 = collection.aggregate([{"$sample": {"size": 1}}]).next()
    factss = [fact1["name"] , fact2["name"] , fact3["name"]]
    facts = [fact1 , fact2 , fact3]
    i = random.randint(0,2)
    question = facts[i]["question"]
    if i == 0:
        answer = "🇦"
    elif i == 1 :
        answer = "🇧"
    else :
        answer = "🇨"
    messages = await message.send(f"🧠 **{question}**\n" + "\n".join(factss))
    for emoji in ["🇦", "🇧", "🇨"] :
        await messages.add_reaction(emoji)
    def check(reaction , user):
        return user != bot.user and reaction.message.id == messages.id and str(reaction.emoji) in ["🇦" , "🇧" , "🇨"]
    reaction , user = await bot.wait_for("reaction_add" , check = check)
    if reaction.emoji == answer:
        await message.send(f"✅ Well done {message.author.mention} ! You got it right !!")
        await message.send(f"Here is the fun fact about it : {facts[i]["fact"]} ")
    else:
        await message.send(f"❌ You got the wrong answer {message.author.mention} ! ")
        await message.send(f"Here is the fun fact about it : {facts[i]["fact"]} ")

bot.run(TOKEN)