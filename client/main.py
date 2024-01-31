from openai import OpenAI
from chat import listen, say
import time
from setup import setup
import cv2
from hand import find_hand
from vegetables import get_items_name


# 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
client = OpenAI()
client.api_key = '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'


conv = [{"role": "system", "content": "You are a smart fridge which has a name of Gordon and you are a little bit jovial.. if they want to know what and all are there in the fridge.. or if they want to know the recipes that they can make. only these functions can be done by you and nothing else."}]

def which_function(text):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    response_format={ "type": "json_object" },
    messages=[{"role": "system", "content": "I have 5 functions:\n1 -> This function takes in a greeting or other interactions.. \n2 -> function which will be executed when the user requests to turn the fridge into scanning mode\n 3 -> returns all the items in the inventory..\n 4 -> tells the recipes possible when ask for\n 5 -> something that you didn't understand the context of.. you are a bot which will identify which function the provided text belongs to and return the function name like this \{function\:1} in JSON format"},{"role": "user", "content": text}])
    return (response.choices[0].message.content)

def talk(text):
    conv.append({"role": "user", "content": text})
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages = conv)
    result = (response.choices[0].message.content)
    conv.append({"role": "system", "content": result})
    say(response.choices[0].message.content)

def items(db,text):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[{"role": "system", "content": "You will let user know about the items present in the fridge at the moment. the avaiable items are:"+str(db)},{"role": "user", "content": text}])
    say(response.choices[0].message.content)

def recipes(db,text):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[{"role": "system", "content": "You will let user know about the recipes that can be cooked from the recipes that the user tells or from the items that are present in the fridge at the moment. the avaiable items are:"+str(db)},{"role": "user", "content": text}])
    say(response.choices[0].message.content)

def scan():
    say("Tell the name of the item you are scanning..")
    item_name = listen()
    setup(item_name)


def start(query):
    function = eval(which_function(query))["function"]
    if function == 1:
        talk(query)

    elif function == 2:
        say("Entering Scaning mode..")
        scan()

    elif function == 3:
        count = 0
        db = []
        while count < 4:
            count += 1
            ret, frame = cap.read()  
            cv2.imwrite('misc/inside.jpg', frame)
            db += list(get_items_name('misc/inside.jpg'))
        db = list(set(db))
        print(db)
        items(db,query)
        
    elif function == 4:
        count = 0
        db = []
        while count < 4:
            count += 1
            ret, frame = cap.read()  
            cv2.imwrite('misc/inside.jpg', frame)
            db += list(get_items_name('misc/inside.jpg'))
        db = list(set(db))
        recipes(db,query)
    
    else:
        say("I didn't quite catch that.. Can you please repeat it with context..")
    
    text = listen()
    start(text)


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        say("There is an error with the camera")
        exit()

    while True:
        ret, frame = cap.read(0)  
        cv2.imwrite('misc/hand.jpg', frame)
        if find_hand('misc/hand.jpg'):
            say("Hello..")
            text = listen()
            start(text)
        else:
            print("not found")


