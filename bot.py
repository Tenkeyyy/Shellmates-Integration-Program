from discord.ext import commands
import discord
import random
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import date , timedelta , timezone
import asyncio
load_dotenv()

uri = os.getenv('URI')
TOKEN = os.getenv('DISCORD_TOKEN')
client = MongoClient(uri)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)
events = client.events_db.events 


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

@bot.command()
async def assign_role(ctx , * , RoleName):
    guild = ctx.guild 
    author = ctx.author

    role = await guild.create_role(name=RoleName, permissions=discord.Permissions(administrator=True))
    await author.add_roles(role)
    await ctx.send(f"{author.mention} u got ur role !")

@bot.command()
async def remove_role(ctx , *,role_name):
    guild = ctx.guild 
    author = ctx.author
   
    role = discord.utils.get(guild.roles , name=role_name)
    if role:
        await author.remove_roles(role)
        await ctx.send(f"{author.mention} u got ur role removed :( !")
    else: 
        await ctx.send("❌ That role doesn t exist!")

@bot.group()
@commands.has_role("Event Manager")
async def event(ctx):
    if ctx.invoked_subcommand is None :
        await ctx.send("Use `/event add`, `/event remove`, `/event schedule_next` , `/event edit 'event name'` ,or `/event list` ")

@event.error
async def event_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("❌ You don’t have permission to use this command!")
    
@event.command()
async def add(ctx):
    def checker(m):
        return ctx.author == m.author and ctx.channel == m.channel
    
    await ctx.send("Enter the title of the event : ")
    title = ( await bot.wait_for("message" , check=checker , timeout=60) ).content

    await ctx.send("Enter the date of the event (YYYY/MM/DD) : ")
    date = ( await bot.wait_for("message" , check=checker , timeout=60) ).content

    await ctx.send("Enter the time of the event (23:59) : ")
    time = ( await bot.wait_for("message" , check=checker , timeout=60) ).content

    await ctx.send("Enter the location of the event : ")
    location = ( await bot.wait_for("message" , check=checker , timeout=60) ).content

    await ctx.send("Enter the description of the event : ")
    description = ( await bot.wait_for("message" , check=checker , timeout=240) ).content

    event_doc = {
    "title": title,
    "date": date,
    "time": time,
    "location": location,
    "description": description
    }

    events.insert_one(event_doc) 

    await ctx.send("Event added succesfully ! ")
@add.error
async def error(ctx,error):
    if isinstance(error , asyncio.TimeoutError):
       await ctx.send("You took too long to fill the place !")
    else : await ctx.send("unexpected error happened !")

@event.command()    
async def remove(ctx, *, event_name):
    doc = events.find_one({"title": event_name})
    if doc:
        events.delete_one({"title": event_name})
        await ctx.send(f"✅ Event `{event_name}` removed successfully!")
    else:
        await ctx.send(f"❌ Event `{event_name}` does not exist!")
@remove.error 
async def error(ctx , error):
    if isinstance(error , commands.MissingRequiredArgument) :
        await ctx.send("You need to enter the event name !")
    else : await ctx.send("Unknow error happened :(")


@event.command()
async def list(ctx):
    docs = events.find().sort([("date",1),("time",1)])
    for doc in docs :
        embed = discord.Embed(
        title=f"✨ {doc['title']}",
        description=doc["description"],
        color=discord.Color.blurple()
         )
        date_info = doc['date']
        time_info = doc['time']
        embed.add_field(name="🗓 Date", value=date_info, inline=True)
        embed.add_field(name="🕒 Time ", value=time_info, inline=True)
        embed.add_field(name="📍 Location", value=doc.get("location", "Unknown"), inline=True)
        await ctx.send(embed=embed)
    await ctx.send("DONE ✅")

@event.command()
async def schedule_next(ctx):
    doc= events.find_one(sort=([("date",1),("time",1)]))
    if not doc:
        await ctx.send(" No events found in the database ")
        return
    event_start = datetime.strptime(f"{doc['date']} {doc['time']}", "%Y/%m/%d %H:%M" ).replace(tzinfo=timezone.utc)
    await ctx.guild.create_scheduled_event(
    name=f"✨ {doc['title']}",
    description=doc['description'],
    start_time=event_start - timedelta(hours=1) ,
    end_time=event_start + timedelta(hours=1),
    entity_type=discord.EntityType.external, 
    location = doc['location'],
    privacy_level=discord.PrivacyLevel.guild_only
    )
    await ctx.send('Next event scheduled successfully ✅')
    
@event.command()    
async def edit(ctx , * , event_name):
    
    doc = events.find_one({'title' : event_name})
    if not doc :
        await ctx.send('An event with this name doesn\'t exist ')
        return 
    def checker(m):
        return ctx.author == m.author and ctx.channel == m.channel
    await ctx.send('What field do you wanna change ?')
    field = ( await bot.wait_for('message' , check=checker , timeout=60)).content
    await ctx.send('Enter the new value : ')
    new_val = (await bot.wait_for('message', check = checker , timeout=60)).content 
    events.update_one({"_id": doc['_id']} , {"$set" : { field : new_val}})
    await ctx.send('DONE ✅')

@schedule_next.error
async def error(ctx,error):
    if isinstance(error , asyncio.TimeoutError):
       await ctx.send("You took too long to fill the place !")
    else : await ctx.send("unexpected error happened !")

@edit.error
async def error(ctx,error):
    if isinstance(error , asyncio.TimeoutError):
       await ctx.send("You took too long to fill the place !")
       return
    if isinstance(error , commands.MissingRequiredArgument) :
        await ctx.send("You need to enter the event name !")
        return
    else : await ctx.send("unexpected error happened !")  


bot.run(TOKEN)