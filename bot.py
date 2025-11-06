from discord.ext import commands
import discord
import random
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import date
load_dotenv()

uri = os.getenv('XXX')
TOKEN = 'XXX'
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
async def fact(message):
    db = client.facts
    collections = db.list_collection_names()
    collection = db[random.choice(collections)]
    fact = collection.aggregate([{"$sample": {"size": 1}}]).next()
    embed = discord.Embed(
        title=f"💡 {fact['name']}",
        description=fact["fact"],
        color=discord.Color.green()
    )
    await message.send(embed=embed)
@bot.command()
async def quiz(ctx):
    db = client.facts
    collection = db[random.choice(db.list_collection_names())]
    fact1 = collection.aggregate([{"$sample": {"size": 1}}]).next()
    fact2 = collection.aggregate([{"$sample": {"size": 1}}]).next()
    fact3 = collection.aggregate([{"$sample": {"size": 1}}]).next()
    while fact2 == fact1:
        fact2 = collection.aggregate([{"$sample": {"size": 1}}]).next()
    while fact3 == fact2 or fact3 == fact1:
        fact3 = collection.aggregate([{"$sample": {"size": 1}}]).next()
    factss = [fact1["name"], fact2["name"], fact3["name"]]
    facts = [fact1, fact2, fact3]
    i = random.randint(0, 2)
    answer = ["🇦", "🇧", "🇨"][i]
    question = facts[i]["question"]
    description_text = f"**{question}**\n\n" \
                        f"🇦\u00A0\u00A0\u00A0{factss[0]}\n\n" \
                        f"🇧\u00A0\u00A0\u00A0{factss[1]}\n\n" \
                        f"🇨\u00A0\u00A0\u00A0{factss[2]}"

    embed = discord.Embed(
        title="🧠 Quiz Time!",
        description=description_text,
        color=discord.Color.blurple()
    )
    quiz_message = await ctx.send(embed=embed)
    for emoji in ["🇦", "🇧", "🇨"]:
        await quiz_message.add_reaction(emoji)
    def check(reaction, user):
        return user != bot.user and reaction.message.id == quiz_message.id and str(reaction.emoji) in [" 🇦", "🇧", "🇨"]
    reaction, user = await bot.wait_for("reaction_add", check=check)
    result_embed = discord.Embed(
        color=discord.Color.green() if reaction.emoji == answer else discord.Color.red()
    )
    result_embed.title = "✅ Correct!" if reaction.emoji == answer else "❌ Wrong!"
    result_embed.description = f"The correct answer was **{answer} {factss[i]}**\n\nFun fact: {facts[i]['fact']}"

    await ctx.send(embed=result_embed)



@bot.command()
async def update_database(ctx):
    db = client.users
    collection = db.users
    async for member in ctx.guild.fetch_members(limit = None):
        user = collection.find_one({"user_id" : member.id})
        roles = [role.name for role in member.roles]
        if user:
            for role in user["roles"]:
                if role not in roles:
                    collection.update_one({"user_id" : member.id} , {"$pull" : {"roles" : role}})
            for role in roles :
                if role not in user["roles"]:
                    collection.update_one({"user_id" : member.id} , {"$push" : {"roles" : role}})
        else:
            tasks = []
            document = {
                "user_id" : member.id ,
                "name" : member.name ,
                "roles" : roles , 
                "tasks" : tasks
            }
            collection.insert_one(document)
    await ctx.send(f"{ctx.author.mention} The Database has been updated successfully ! ")



@bot.command()
async def assign_task(ctx , role : str , *, task):
    db = client.users
    collection = db.users
    _role = discord.utils.get(ctx.guild.roles , name = role)
    await update_database(ctx)
    async for member in ctx.guild.fetch_members(limit = None):
        roles = [role1.name for role1 in member.roles]
        if role in roles :
            user = collection.find_one({"user_id" : member.id})
            collection.update_one({"user_id" : member.id} , {"$push" : {"tasks" : task}})
            print("assigning was successful")
    await ctx.send(f"{_role.mention} , you have been assigned this task : {task}")



@bot.command()
async def mytasks(ctx):
    db = client.users
    collection = db.users
    user = collection.find_one({"user_id" : ctx.author.id})
    i = 1 
    await ctx.author.send(f"{ctx.author.mention} you have the following tasks : ")
    for task in user["tasks"]:
        await ctx.author.send(f"{i} : {task} ")
        i = i + 1




@bot.command()
async def deletetask(ctx , user : discord.User , *, task ):
    db = client.users
    collection = db.users
    _user = collection.find_one({"user_id" : user.id})
    if task not in _user["tasks"]:
        await ctx.author.send(f"{ctx.author.mention} , The task doesn't exist ! ")
    else:
        collection.update_one({"user_id" : user.id}, {"$pull" : {"tasks" : task}})
        await ctx.author.send("Task deleted successfully !")




@bot.command()
async def tip(ctx):
    db = client.tips 
    collection = db.tips 
    tip = collection.aggregate([{"$sample": {"size": 1}}]).next()
    embed = discord.Embed(
        title=f"💡 {tip['title']}",
        description=tip['details'],
        color=discord.Color.yellow()
    )
    await ctx.send(embed=embed)




@bot.command()
async def cyberterm(ctx):
    db = client.terms 
    collection = db.terms 
    term = collection.aggregate([{"$sample": {"size": 1}}]).next()
    embed = discord.Embed(
        title=f"🕵️‍♂️ {term['term']}",
        description=term['definition'],
        color=discord.Color.dark_grey()
    )
    await ctx.send(embed=embed)



@bot.command()
async def onthisday(ctx):
    db = client.cyber_history 
    collection = db.onthisday 
    day = str(date.today().day)
    month = str(date.today().month)
    fact = collection.find_one({"month": month, "day": day})
    if fact:
        embed = discord.Embed(
            title=f"⏳ On This Day",
            description=fact["info"],
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Nothing happened on this day!")


def insert_task(username, task, status, deadline):
    db = client.users       # Use the 'users' DB
    collection = db.tasks   # Create/use the 'tasks' collection
    document = {
        "username": username,
        "task": task,
        "status": status,
        "deadline": deadline
    }
    collection.insert_one(document)







def get_user_tasks(username):
    db = client.users
    collection = db.tasks
    tasks = collection.find({"username": username})
    result = []
    for task in tasks:
        result.append({
            "task": task["task"],
            "status": task["status"],
            "deadline": task["deadline"]
        })
    return result


@bot.command()
async def tasks(ctx, *, username):
    db = client.users
    collection = db.users
    
    # Look for the user by username
    user = collection.find_one({"name": username})
    if not user or "tasks" not in user or len(user["tasks"]) == 0:
        await ctx.send(f"No tasks found for {username}.")
        return
    
    msg = f"Tasks for {username}:\n"
    for i, t in enumerate(user["tasks"], 1):
        msg += f"{i}. {t}\n"
    
    await ctx.send(msg)


bot.run(TOKEN)