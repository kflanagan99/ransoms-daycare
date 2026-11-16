# Ransom's Daycare

A Python-based dog daycare program where your dog is held for ransom until you pay.

## About

I built this project while learning Python. I wanted to make something that was actually fun to work on while practicing what I've learned so far.

The program lets you check dogs in and out of daycare, register new dogs, look up their information, and create incident reports. It also has a payment system where you can pay your dog's ransom with cash or card.

I started with basic Python and JSON, then added SQLite so I could practice working with databases.

## Features

- Check dogs in and out of daycare
- Register new dogs and save their information
- Look up dog profiles
- Simulate cash and card payments
- Create and view incident reports
- Save and retrieve information using JSON and SQLite
- Handle invalid inputs without crashing

## What I Used

- Python
- SQLite
- JSON

## What I Learned

This project gave me more practice with loops, conditionals, functions, dictionaries, lists, and error handling.

I also learned how to connect Python to a SQLite database, write SQL queries, and save information so it doesn't disappear every time the program closes.

There was a lot of debugging involved, especially as I started adding more features, but that was part of the learning process.

## How to Run It

1. Make sure Python 3 is installed.
2. Download the project files.
3. Open the project folder in your terminal.
4. Run `python3 database.py` to set up the dog database.
5. Run `python3 dog_daycare.py` to start the program.

Once it's running, you can type any of these commands:

- `check in` — Check a dog into daycare
- `check out` — Pay the ransom and pick up your dog
- `check` — View a checked-in dog's information
- `incident` — Write an incident report
- `reports` — View a dog's incident history
- `close daycare` — Close the daycare
- `all set` — Exit the program

## Notes

This is a beginner project that I'm using to practice Python and SQL. The payments aren't real, and the list of dogs currently checked in resets when the program closes.

I'm still learning and plan to keep improving it as I learn more.