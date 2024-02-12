# Import pyinputplus for choice inputs and os to clear the console.
import pyinputplus
import os
import json

# setting up some variables
currentKey = '0'
currentKeys = []
itemAlreadyAdded = False

# Get the Story Prompts
# A dictionary is used because we dont want to allow
# duplicate keys
with open('story.json', 'r') as f:
    storyPrompts = json.load(f)

inventory = []
instructions = """

Portobella
You are a 10-year old boy named Porto.  That's the only thing you remember from
before you woke up.  Unbeknownst to you, one fateful night, you lost your family
and were displaced.  Your parents, sister, and you were sitting around the dinner
table when unspeakable abominations came in crashing through the doors and windows.
Everyone was scattered, your house destroyed, and you blacked out.  You are pretty
certain you lost your parents, but a feeling in your gut tells you your sister,
Bella, is still out there.  You've got to go save her, but how?  As you wake up,
your injuries seem to have healed, albeit leaving scars, and you are doused in
sweat.  Your surroundings are strange and a wave of terror immediately overtakes
you.  This seems to be an exotic rainforest.  The weather is sweltering and it
feels like your skin is peeling off your bones.  Your clothes are like a dirty
towel covering your whole body, but you ignore them.  You gotta man up now,
because your sister is out there.  Dead or alive, you are determined to find her.
This is the fastest that you've grown up in a long time.  Speaking of which, it's
of the essence.  If Bella is out there crying for help, it won't be for long.
After gaining your strength, you embark on the journey of a lifetime.  You'll
only know where you'll end up when you see the only family you're gonna see.

This help file will only show once.  You are given two options every prompt of
the game to decide what action you want Porto to take.  At times, you will gain
items.  Don't ignore these, since they will give you clues on what to do next.
You must use logic in solving puzzles, particularly how the items are utilized.
There are two paths you can go, and the only time you can turn back is right at the
beginning, while you are still uncertain which path to take.  Either one will
take you on a completely different adventure, with multiple ways to end it.
Porto's fate is in your hands.  It may be a good idea to write down what action
leads to what prompt at every turn.  That way, if you must abandon your game,
you will know how to get back to where you were.  This game is rather lengthy
either path you take, and you may want to discover all possible endings.

At every prompt, type in the number of the action you want Porto to take,
-1 to exit the game, or -i to view your inventory ... good luck.

"""

# Check if the prompts are valid
for prompt in storyPrompts:
    promptText, keys, *_ = storyPrompts[prompt]

    # Add ":" at the end of the prompt Text
    if not promptText.endswith(':'):
        storyPrompts[prompt][0] = promptText + ': '

    # Check if the keys are strings, if not transform them
    storyPrompts[prompt][1] = [str(i) for i in keys]

# Giving the user some instructions.
print(instructions)
input('Press Enter to continue ... if you dare ...')

# Prompt Loop
while True:
    # Clearing the Console on all platforms
    os.system('cls' if os.name == 'nt' else 'clear')

    # Get the current prompt all its associated data
    currentPrompt, currentKeys, _, action = storyPrompts[currentKey]

    # Finish the Adventure when the next keys list contains the string 'end'
    if 'end' in currentKeys:
        break

    # Look for inventory Changes
    if not itemAlreadyAdded:
        if 'minus' in action:
            inventory.remove(action.split('-')[1])
        if 'plus' in action:
            inventory.append(action.split('-')[1])

    # Add Option Descriptions to the current Prompt with their number
    for o in currentKeys:
        invalidOption = False
        thisaction = storyPrompts[o][3]
        if 'minus' in thisaction:
            item = storyPrompts[o][3].split('-')[1]
            if item not in inventory:
                print(storyPrompts[o][3].split('-')[1])
                invalidOption = True

        if not invalidOption:
            currentPrompt += f'\n{o}. {storyPrompts[o][2]}'

    currentPrompt += '\n\nWhat do you do? '

    # Get the input from the user, only give them the keys as a choice so they dont
    # type in something invalid.
    userInput = pyinputplus.inputChoice(choices=(currentKeys + ['-i'] + ['-1']), prompt=currentPrompt)

    # Printing out the inventory if the user types in -i
    if '-i' in userInput:
        print(f'\nCurrent Inventory: ')
        for i in inventory:
            print(i)
        print('\n')
        input('Press Enter to continue ... ')
        itemAlreadyAdded = True
        continue
    elif '-1' in userInput:
        break
    else:
        itemAlreadyAdded = False
    currentKey = userInput

# Printing out the last prompt so the user knows what happened to him.
if '-1' in userInput:
    print('You black out again.')
else:
    print(storyPrompts[currentKey][0])
print('\nStory Finished ...')

