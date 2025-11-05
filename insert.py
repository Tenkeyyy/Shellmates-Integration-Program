from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
uri = os.getenv('URI')
client = MongoClient(uri)
def insert_fact_hackers(name , question , fact):
    db = client.facts 
    collection = db.Hackers
    document = {
        "name" : name ,
        "question" : question ,
        "fact" : fact 
    }
    collection.insert_one(document)
def insert_fact_cyberattacks(name , question , fact):
    db = client.facts 
    collection = db.Cybersecurity_attacks
    document = {
        "name" : name ,
        "question" : question ,
        "fact" : fact 
    }
    collection.insert_one(document)
def insert_event(name , year , month , day , details):
    db = client.events_db
    collection = db.events
    document = {
        "name" : name ,
        "year" : year ,
        "month" : month ,
        "day" : day ,
        "details" : details
    }
    collection.insert_one(document)
def inserttip(title , details):
    db = client.tips 
    collection = db.tips
    document = {
        "title" : title ,
        "details" : details 
    }
    collection.insert_one(document)
def insertterm(term , definition):
    db = client.terms 
    collection = db.terms
    document = {
        "term" : term ,
        "definition" : definition 
    }
    collection.insert_one(document)

i = input("What do u wanna do ? 0 for inserting events , 1 for inserting facts ")
if(i == 0):
    while True : 
        name = input("Type the name of the fact : ")
        fact = input("Type the fact : ")
        question = input("Type the question : ")
        insert_fact(name , question , fact )
        print("Success !")
else:
    j = input("Do you want to insert a Hacker fact or a Cyber attack ? 0 for Hacker , 1 for cyber attack")
    if(j == 0):
        while True : 
            name = input("Type the name of the fact : ")
            fact = input("Type the fact : ")
            question = input("Type the question : ")
            insert_fact_hackers(name , question , fact )
            print("Success !")
    else:
        while True : 
            name = input("Type the name of the fact : ")
            fact = input("Type the fact : ")
            question = input("Type the question : ")
            insert_fact_cyberattacks(name , question , fact )
            print("Success !")
