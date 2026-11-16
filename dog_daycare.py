
import json
import random
import sqlite3
import math

connection = sqlite3.connect("daycare.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY,
        dog TEXT,
        incident_type TEXT,
        description TEXT,
        action_taken TEXT
    )
""")

connection.commit()

with open("dogs.json", "r") as file:
    dogs = json.load(file)

def welcome():
    print("Welcome to Ransom's Daycare, where we hold your dog for ransom until you pay. How can I help you?")

welcome()

bank_balance = random.randint(0, 100)

checked_in = []
daycare_fee = 75

while True:
    action = input("> ").lower()

    if action == "all set":
        print("You're all set! Thank you for using Ransom's Daycare.")
        break

    if action == "check in":
        dog = input("Who are you checking in? ").lower()

        if dog in checked_in:
            print("..? He got dropped off already.")

        else:
            cursor.execute(
                "SELECT * FROM dogs WHERE LOWER(name) = ?",
                (dog.lower(),)
            )

            registered_dog = cursor.fetchone()

            if registered_dog:
                checked_in.append(dog)
                print(f"{dog.capitalize()} is checked in!")

            else:
                add_client = input(
                    f"{dog.capitalize()} isn't a registered client. Would you like to add them to our system? "
                ).lower()

                if add_client == "yes":
                    breed = input(f"What breed is {dog.capitalize()}? ")
                    while True:
                        try:
                            age = int(input(f"How old is {dog.capitalize()}? "))
                            if age <= 0:
                                print("Please enter a positive age.")
                            else:
                                break

                        except ValueError:
                            print("Please enter a valid number.")

                    age_unit = input("Months or years? ").lower()
                    behavior = input("How would you describe his temperament? ")

                    dogs[dog] = {
                        "breed": breed,
                        "age": age,
                        "age_unit": age_unit,
                        "behavior": behavior
                    }

                    cursor.execute(
                        "INSERT INTO dogs (name, breed, age, age_unit, behavior) VALUES (?, ?, ?, ?, ?)",
                        (dog, breed, age, age_unit, behavior)
                    )

                    connection.commit()

                    with open("dogs.json", "w") as file:
                        json.dump(dogs, file)

                    print(f"{dog.capitalize()} has been added as a new client!")

                    checked_in.append(dog)
                    print(f"{dog.capitalize()} is checked in!")

    if action == "check out":
        dog = input("Who are you picking up? ").lower()

        if dog in checked_in:
            while True:
                payment_method = input(
                    f"{dog.capitalize()}'s ransom is ${daycare_fee}. Cash or card? "
                ).lower()

                if payment_method == "cash":
                    try:
                        cash_given = float(input("How much cash are you giving me? "))

                        if not math.isfinite(cash_given):
                            print("Please enter a valid cash amount.")
                        elif cash_given < daycare_fee:
                            print(
                                f"You're short ${daycare_fee - cash_given:.2f}. "
                                f"{dog.capitalize()} remains a hostage until the ransom is paid in full."
                            )

                        else:
                            change = cash_given - daycare_fee
                            print(
                                f"Your change is ${change:.2f}. "
                                f"{dog.capitalize()} has been checked out. Have a nice day!"
                            )
                            checked_in.remove(dog)
                            break

                    except ValueError:
                        print("Please enter a valid cash amount.")

                elif payment_method == "card":
                    print("Processing card...")

                    if bank_balance < daycare_fee:
                        print(
                            f"❌ DECLINED. {dog.capitalize()} is remaining with us "
                            "until their ransom is paid in full. "
                            "You better come back with the full amount."
                        )

                    else:
                        card_result = random.choice(
                            ["approved", "approved", "approved", "declined"]
                        )

                        if card_result == "approved":
                            bank_balance = bank_balance - daycare_fee
                            print(
                                f"✅ APPROVED. {dog.capitalize()} is free to go. Have a nice day!"
                            )
                            checked_in.remove(dog)
                            break

                        else:
                            print(
                                f"❌ DECLINED. {dog.capitalize()} is remaining with us "
                                "until their ransom is paid in full. "
                                "You better come back with the full amount."
                            )

                else:
                    print("Invalid payment method. Cash or card only!")

        else:
            print(f"{dog.capitalize()} isn't here!")

    
    if action == "check":
        dog = input("What dog do you want to check? ").lower()

        if dog == "all set":
            break

        if dog in checked_in:
            cursor.execute(
                "SELECT breed, age, age_unit, behavior FROM dogs WHERE LOWER(name) = ?",
                (dog,)
            )

            dog_info = cursor.fetchone()

            if dog_info:
                print(
                    f"{dog.capitalize()} is a "
                    f"{dog_info[1]}-{dog_info[2].rstrip('s')}-old "
                    f"{dog_info[0]}. {dog_info[3]}"
                )
            else:
                print("Dog information not found in the database.")

        else:
            print(f"{dog.capitalize()} isn't here.")

    if action == "incident":
        dog = input("Which dog are we writing an incident report for? ").lower()

        if dog in checked_in:
            print(f"Creating an incident report for {dog.capitalize()}...")

            incident_type = input("What type of incident occurred? ")
            description = input("Describe what happened: ")
            action_taken = input("What action was taken? ")

            cursor.execute(
                """
                INSERT INTO incidents (dog, incident_type, description, action_taken)
                VALUES (?, ?, ?, ?)
                """,
                (dog, incident_type, description, action_taken)
            )

            connection.commit()

            print(f"Incident report for {dog.capitalize()} has been recorded!")

        else:
            print(f"{dog.capitalize()} isn't here right now.")

    if action == "reports":
        dog = input("Whose criminal record would you like to view? ").lower()

        cursor.execute(
            "SELECT incident_type, description, action_taken FROM incidents WHERE LOWER(dog) = ?",
            (dog,)
        )

        reports = cursor.fetchall()

        if reports:
            for report in reports:
                print(report)
        else:
            print(f"No incident reports found for {dog.capitalize()}.")

    if action == "close daycare":
        print("Ransom's Daycare is now closed. All remaining hostages will be held overnight.")
        break

connection.close()
