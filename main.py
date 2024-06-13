### --- IMPORTS --- ### 

#get tkinter
from tkinter import *
import tkinter.messagebox
#pandas
import pandas
#random
import random

### --- VARS/CONSTANTS --- ###

#create variables for var path, and each item
var_path ="." 

card_back = "/images/card_back.png"
card_front = "/images/card_front.png"
right = "/images/right.png"
wrong = "/images/wrong.png"

#get loc of french words and FOLDER where to learn is stored
french_words = "/data/french_words.csv"
to_learn_folder = "/data/"

#BG color
BG_COLOR = "#B1DDC6"
#current card dict to hold our card
current_card = {}
#to learn for try except, if word is not correct add to this then to words to learn csv.
to_learn = {}

### --- LOAD FILE --- ###

try:
    #we try and open words to learn (load stuff we need to learn)
    french_words = pandas.read_csv(var_path+to_learn_folder+"/words_to_learn.csv")
except FileNotFoundError:
    #if no file open original words list
    original_word_list = pandas.read_csv(var_path+french_words)
    #orient records so we can format to dict
    to_learn = original_word_list.to_dict(orient="records")
else:
    #else just open the list
    to_learn = french_words.to_dict(orient="records")

### --- FUNCS --- ###

def new_word():
    """Gets random french word for the card and adds it to flash card. On button press moves to next card
    """
    #global current card and flip so it will update the var and we don't need to add more
    global current_card, flip_timer
    #get a random card from to learn list (either to learn or french words files)
    current_card = random.choice(to_learn)
    #add word to card 
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    #will change card back to french side if flipped
    canvas.itemconfig(card_background, image=front)
    #we want the card to flip after 5 seconds, so user can see what the word is
    flip_timer = window.after(5000, func=flip_card)


def flip_card():
    """Flips the currrent card to the english version after a set period in case the user did not guess it"""
    #updates card to french side
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=current_card["English"], fill="black")
    canvas.itemconfig(card_background, image=back)

def is_known():
    """Gets random french word for the card and adds it to flash card. On button press moves to next card and removes the learnt word from to_learn
    """
    #remove current card
    to_learn.remove(current_card)
    #we also want to create a csv of words to learn for next time we open the app
    data = pandas.DataFrame(to_learn)
    data.to_csv(var_path+to_learn_folder+"/words_to_learn.csv", index=False)
    #then call the next card
    new_word()

### --- WIN SETUP --- ###   

#setup our window
window = Tk()
window.title("Flash Card Study For Serious Gamers")
window.config(padx=50, pady=50, bg=BG_COLOR)

#setup canvas
canvas = Canvas(width=800, height=526)

#now we want our card images, photoimage can't find full path so we store paths in 2 vars
front = PhotoImage(file=var_path+card_front)
back = PhotoImage(file=var_path+card_back)
card_background = canvas.create_image(400, 263, image=front)
#next we want two blank text pieces that will be filled later on witht hese fonts
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
#we want the background color to be filled 
canvas.config(bg=BG_COLOR, highlightthickness=0)
#finally we grid it
canvas.grid(row=0, column=0, columnspan=2)

### --- BUTTONS --- ###

#now we create our buttons for the check and cross, when pressed trigger functions
cross_image = PhotoImage(file=var_path+wrong)
unknown_button = Button(image=cross_image, highlightthickness=0, command=new_word)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file=var_path+right)
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

### --- RUN --- ###

new_word()

window.mainloop()