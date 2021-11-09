import tkinter
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data\\words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data\\portuguese_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    print(current_card["Portuguese"].title())
    canvas.itemconfig(card_title, text="Portuguese", fill="black")
    canvas.itemconfig(card_word, text=current_card["Portuguese"].lower(), fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"].lower(), fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    to_learn.remove(current_card)
    new_data = pandas.DataFrame(to_learn)
    new_data.to_csv("data\\words_to_learn.csv", index=False)
    next_card()


window = tkinter.Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

card_front_img = tkinter.PhotoImage(file="images\\card_front.png")
card_back_img = tkinter.PhotoImage(file="images\\card_back.png")
wrong_img = tkinter.PhotoImage(file="images\\wrong.png")
right_img = tkinter.PhotoImage(file="images\\right.png")

canvas = tkinter.Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_background = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(row=0, column=0, columnspan=2)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

unknown_button = tkinter.Button(image=wrong_img, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)
known_button = tkinter.Button(image=right_img, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()

window.mainloop()
