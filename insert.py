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
def insert_onthisday( day , month , info):
    db = client.cyber_history
    collection = db.onthisday
    document = {
        "month" : month ,
        "day" : day ,
        "info" : info
    }
    collection.insert_one(document)  

while True:
    print("\nChoose an option:")
    print("0 = Insert a Hacker fact")
    print("1 = Insert a Cybersecurity fact")
    print("2 = Insert an Event")
    print("3 = Insert a Term")
    print("4 = Insert a Tip")
    print("5 = Insert an 'On this day' fact")
    print("q = Quit")

    choice = input("Your choice: ")

    if choice == "0":
        while True:
            name = input("Name of the fact: ")
            question = input("Question: ")
            fact = input("Fact: ")
            insert_fact_hackers(name, question, fact)
            print("Success!")
            cont = input("Add another Hacker fact? (y/n): ")
            if cont.lower() != "y":
                break

    elif choice == "1":
        while True:
            name = input("Name of the fact: ")
            question = input("Question: ")
            fact = input("Fact: ")
            insert_fact_cyberattacks(name, question, fact)
            print("Success!")
            cont = input("Add another Cybersecurity fact? (y/n): ")
            if cont.lower() != "y":
                break

    elif choice == "2":
        while True:
            name = input("Event name: ")
            year = input("Year: ")
            month = input("Month: ")
            day = input("Day: ")
            details = input("Details: ")
            insert_event(name, year, month, day, details)
            print("Success!")
            cont = input("Add another Event? (y/n): ")
            if cont.lower() != "y":
                break

    elif choice == "3":
        while True:
            term = input("Term: ")
            definition = input("Definition: ")
            insertterm(term, definition)
            print("Success!")
            cont = input("Add another Term? (y/n): ")
            if cont.lower() != "y":
                break

    elif choice == "4":
        while True:
            title = input("Tip title: ")
            details = input("Details: ")
            inserttip(title, details)
            print("Success!")
            cont = input("Add another Tip? (y/n): ")
            if cont.lower() != "y":
                break

    elif choice == "5":
        while True:
            day = input("Day: ")
            month = input("Month: ")
            info = input("Info/Event: ")
            insert_onthisday(day, month, info)
            print("Success!")
            cont = input("Add another 'On this day' fact? (y/n): ")
            if cont.lower() != "y":
                break

    elif choice.lower() == "q":
        print("Exiting program.")
        break

    else:
        print("Invalid choice, try again.")