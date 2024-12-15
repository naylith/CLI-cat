import pickle
import os
import random
import sys
import time
from datetime import datetime

CAT_ASCII = {
    "happy": """
        /\\_/\\  
       ( o.o ) 
        > ^ <
    """,
    "sleeping": """
        |\\      _,,,---,,_
        /,`.-'`'    -.  ;-;;,_ 
       |,4-  ) )-,_. ,\\ (  `'-'
      '---''(_/--'  `-'\\_)
    """,
    "playing": """
        /\\_/\\  
      =( °w° )=  
        )   (  //
       (__ __)// 
    """,
    "hungry": """
        /\\_/\\  
       ( o.o )  
       >  -  <
    """,
    "judgmental": """
        /\\_/\\  
       (-_- )
       > ^ <
    """,
}

class Cat:
    def __init__(self, name):
        self.name = name
        self.hunger = 100
        self.hygiene = 100
        self.care = 100
        self.last_saved_time = datetime.now()

    def display_ascii(self, mood):
        print(CAT_ASCII.get(mood, ""))

    def time_passed(self):
        current_time = datetime.now()
        elapsed = current_time - self.last_saved_time
        minutes_passed = elapsed.total_seconds() // 60  # Calculate minutes passed
        return minutes_passed

    def apply_time_decay(self):
        minutes = self.time_passed()
        # Decrease stats based on time passed (1 unit every 10 minutes)
        decay = max(1, int(minutes // 10))
        self.hunger = max(0, self.hunger - 5 * decay)
        self.hygiene = max(0, self.hygiene - 3 * decay)
        self.care = max(0, self.care - 2 * decay)
        # Update last saved time to now
        self.last_saved_time = datetime.now()

    def display_stats(self):
        print(f"\n{self.name}'s Stats:")
        print(f"Hunger: {self.hunger}")
        print(f"Hygiene: {self.hygiene}")
        print(f"Care: {self.care}\n")
    
    def display_mood(self):
        time.sleep(0.5)
        if self.hunger < 30:
            print(f"{self.name} looks hungry...")
            self.display_ascii("hungry")
        elif self.care < 30:
            print(f"{self.name} is feeling neglected! :(")
            self.display_ascii("judgmental")
        elif self.hygiene < 30:
            print(f"{self.name} looks a bit scruffy...")
            self.display_ascii("sleeping")
        else:
            print(f"{self.name} looks happy!")
            self.display_ascii("happy")


    def decrease_stats(self):
        self.hunger = max(0, self.hunger - 5)
        self.hygiene = max(0, self.hygiene - 3)
        self.care = max(0, self.care - 2)

    def interact(self):
        interactions = [
            (f"{self.name} purrs loudly and rubs against your leg.", "happy"),
            (f"{self.name} paws at your keyboard curiously.", "playing"),
            (f"{self.name} rolls over, exposing its belly.", "happy"),
            (f"{self.name} stares at you judgmentally.", "judgmental"),
            (f"{self.name} meows softly and blinks at you.", "happy"),
            (f"{self.name} jumps up and tries to catch an invisible bug.", "playing"),
            (f"{self.name} curls up into a loaf and ignores you.", "sleeping"),
            (f"{self.name} stretches and yawns loudly.", "sleeping"),
        ]
        action, mood = random.choice(interactions)
        
        slow_print(f"You decide to check on {self.name}\n")
        
        print(f"{self.name}: {action}")
        self.display_ascii(mood)


def save_cat(cat):
    cat.last_saved_time = datetime.now()
    with open("cat_save.pkl", "wb") as f:
        pickle.dump(cat, f)


def load_cat():
    if os.path.exists("cat_save.pkl"):
        try:
            with open("cat_save.pkl", "rb") as f:
                print("Welcome back!")
                cat = pickle.load(f)
                cat.apply_time_decay()  # Apply decay for time passed
                return cat
        except Exception as e:
            print("Uh oh! Your cat found a new home...")
            os.remove("cat_save.pkl")  # Remove the corrupted save file
    else:
        print("Let's adopt a new cat!")
    
    cat_name = input("What will you name your new cat? > ")
    return Cat(cat_name)

def slow_print(message, delay=0.05, dots=3):
    for char in message:
        print(char, end='', flush=True)
        time.sleep(delay)
    for _ in range(dots):  # Add delayed dots
        print('.', end='', flush=True)
        time.sleep(0.5)
    print()  # Move to the next line


def main():
    cat = load_cat()

    while True:
        cat.display_stats()
        cat.display_mood()
        print("Choose an action: feed, brush, play, interact, quit")
        action = input("> ").strip().lower()

        if action == "feed":
            slow_print(f"You decide to feed {cat.name}\n")
            cat.hunger = min(100, cat.hunger + 20)
            print(f"{cat.name} eats.")
            save_cat(cat)
        elif action == "brush":
            slow_print(f"You decide to groom {cat.name}\n")
            cat.hygiene = min(100, cat.hygiene + 15)
            print(f"{cat.name} looks better!")
            save_cat(cat)
        elif action == "play":
            slow_print(f"You decide to play with {cat.name}\n")
            cat.care = min(100, cat.care + 10)
            print(f"{cat.name} is having fun!")
            save_cat(cat)
        elif action == "interact":
            cat.interact()
            save_cat(cat)
        elif action == "quit":
            save_cat(cat)
            print(f"{cat.name} waves!")
            break
        else:
            print(f"{cat.name} doesn't understand. Try again!")

        cat.decrease_stats()

        # Check if all stats are 0
        if cat.hunger == 0 and cat.hygiene == 0 and cat.care == 0:
            print(f"Oh no! {cat.name} ran away...")
            print("Do you want to adopt a new cat? (yes/no)")
            if input("> ").strip().lower() == "yes":
                cat_name = input("What will you name your new cat? > ")
                cat = Cat(cat_name)
            else:
                print("Thanks for playing!")
                break

if __name__ == "__main__":
    main()
