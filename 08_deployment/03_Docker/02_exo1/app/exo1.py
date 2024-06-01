### Find your buddy! 
### Here is one way to create an app that simply create random groups of people
import random 

### Create a list of buddies in your class 
GROUPS_SIZE = 5
buddies = [
    "Alex", 
    "Antoine", 
    "Michel", 
    "Anna", 
    "Célia", 
    "Roseline",
    "Marie",
    "David", 
    "Jocelyne",
    "Joséphine",
    "Julien",
    "Hortense", 
    "Ahmed"
]

random.shuffle(buddies)

#### Match each buddy to a person 
groups = [buddies[x:x+GROUPS_SIZE] for x in range(0, len(buddies), GROUPS_SIZE)]

if len(groups[-1]) == 1:
    alone_person = groups.pop(-1)
    groups[-1] += alone_person

### Print matching buddies
print("Here are your groups")
print("\n")

for i, group in enumerate(groups):
    print(f"group {i}: {group}")