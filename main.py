import tkinter as tk
from tkinter import Canvas
import pygame


# Sound for my Quiz
pygame.mixer.init()
sound_on = True


def toggle_sound():
   global sound_on
   sound_on = not sound_on


   if sound_on:
       sound_button.config(text="🔊")
       play_sound()
   else:
       sound_button.config(text="🔇")
       pygame.mixer.music.stop()

# Main Menu header and geometry
root = tk.Tk()
root.title("New Zealand Quiz")
root.geometry("1000x600")
root.resizable(False, False)


# Colours are used in my design
NAVY = "#0b0f5c"
RED = "#e21b23"
WHITE = "#ffffff"
GREY = "#d9d9d9"


canvas = Canvas(root, width=1000, height=600, bg=NAVY, highlightthickness=0)
canvas.pack(fill="both", expand=True)


# Diagonal stripe on home page
canvas.create_polygon(
   450, 600,
   1000, 300,
   1000, 340,
   500, 600,
   fill=WHITE,
   outline=""
)


canvas.create_polygon(
   520, 600,
   1000, 360,
   1000, 395,
   580, 600,
   fill=RED,
   outline=""
)


LEFT_MARGIN = 80


# Header of my home screen
canvas.create_text(
   LEFT_MARGIN, 70,
   text="Welcome to the New Zealand Quiz",
   fill=WHITE,
   font=("Times New Roman", 32, "bold"),
   anchor="w"
)


canvas.create_text(
   LEFT_MARGIN, 120,
   text="Test your knowledge on New Zealand’s Birds, Slang, Places and more",
   fill=WHITE,
   font=("Times New Roman", 16),
   anchor="w"
)


# Buttons of my main menu
def create_menu_button(text, y):
   label = tk.Label(
       root,
       text=text,
       bg=GREY,
       fg="black",
       font=("Times New Roman", 18, "italic"),
       width=18,
       anchor="center"
   )


   def on_enter(e):
       label.config(bg=RED, fg=WHITE)


   def on_leave(e):
       label.config(bg=GREY, fg="black")


   label.bind("<Enter>", on_enter)
   label.bind("<Leave>", on_leave)


   canvas.create_window(200, y, window=label)


# Buttons on my main menu
create_menu_button("General Knowledge", 220)
create_menu_button("Native Animals", 270)
create_menu_button("Places", 320)
create_menu_button("Slang", 370)


def create_icon_button(symbol, command):
   btn = tk.Button(
       root,
       text=symbol,
       font=("Segoe UI Emoji", 16),
       bg=NAVY,
       fg=WHITE,
       activebackground=NAVY,
       activeforeground=WHITE,
       bd=1,
       relief="solid",
       width=3,
       height=1,
       command=command
   )
   return btn


# Help button on home page
def show_help():
   print("Help clicked")


# Main menu icon buttons (sound and help button)
help_button = create_icon_button("?", show_help)
sound_button = create_icon_button("🔊", toggle_sound)


# The position of my main menu buttons
RIGHT_MARGIN = 40
BOTTOM_MARGIN = 40
SPACING = 60


canvas.create_window(
   1000 - RIGHT_MARGIN,
   600 - BOTTOM_MARGIN - SPACING,
   window=help_button
)


canvas.create_window(
   1000 - RIGHT_MARGIN,
   600 - BOTTOM_MARGIN,
   window=sound_button
)


root.mainloop()

