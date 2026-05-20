import tkinter as tk
from tkinter import Canvas
import pygame

pygame.mixer.init()
sound_on = True


root = tk.Tk()
root.title("New Zealand Quiz")
root.geometry("1000x600")
root.resizable(False, False)

NAVY = "#0b0f5c"
RED = "#e21b23"
WHITE = "#ffffff"
GREY = "#d9d9d9"


selected_category = ""

def play_sound():
   if sound_on:
       try:
           pygame.mixer.music.load("click.mp3")
           pygame.mixer.music.play()
       except:
           print("Missing sound file")




def toggle_sound():
   global sound_on
   sound_on = not sound_on


   if sound_on:
       sound_button.config(text="🔊")
       play_sound()
   else:
       sound_button.config(text="🔇")
       pygame.mixer.music.stop()




canvas = Canvas(root, width=1000, height=600, bg=NAVY, highlightthickness=0)
canvas.pack(fill="both", expand=True)





def draw_background():
   canvas.delete("all")


   # Diagonal white stripe
   canvas.create_polygon(
       450, 600,
       1000, 300,
       1000, 340,
       500, 600,
       fill=WHITE,
       outline=""
   )


   # Diagonal red stripe
   canvas.create_polygon(
       520, 600,
       1000, 360,
       1000, 395,
       580, 600,
       fill=RED,
       outline=""
   )


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


def show_help():
   print("Help clicked")


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


   def on_click(e):
       open_name_page(text)


   label.bind("<Enter>", on_enter)
   label.bind("<Leave>", on_leave)
   label.bind("<Button-1>", on_click)

   canvas.create_window(200, y, window=label)


def show_main_menu():
   draw_background()


   LEFT_MARGIN = 80


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

   create_menu_button("General Knowledge", 220)
   create_menu_button("Native Animals", 270)
   create_menu_button("Places", 320)
   create_menu_button("Slang", 370)

def open_name_page(category):
   global selected_category
   selected_category = category


   draw_background()


   LEFT_MARGIN = 80


   canvas.create_text(
       LEFT_MARGIN, 70,
       text=f"{category} Quiz",
       fill=WHITE,
       font=("Times New Roman", 32, "bold"),
       anchor="w"
   )


   canvas.create_text(
       LEFT_MARGIN, 120,
       text="Please enter your name to begin",
       fill=WHITE,
       font=("Times New Roman", 16),
       anchor="w"
   )


   # Name Entry Box
   name_entry = tk.Entry(
       root,
       font=("Times New Roman", 20),
       width=25,
       bd=2,
       relief="solid"
   )


   canvas.create_window(300, 240, window=name_entry)


   # Start Button
   start_button = tk.Label(
       root,
       text="Start Quiz",
       bg=GREY,
       fg="black",
       font=("Times New Roman", 18, "italic"),
       width=15,
       anchor="center"
   )


   def start_hover(e):
       start_button.config(bg=RED, fg=WHITE)


   def start_leave(e):
       start_button.config(bg=GREY, fg="black")


   def start_quiz(e):
       username = name_entry.get()
       print(f"Starting {category} quiz for {username}")


   start_button.bind("<Enter>", start_hover)
   start_button.bind("<Leave>", start_leave)
   start_button.bind("<Button-1>", start_quiz)


   canvas.create_window(220, 330, window=start_button)


   # Back Button
   back_button = tk.Label(
       root,
       text="← Back",
       bg=GREY,
       fg="black",
       font=("Times New Roman", 16),
       width=10,
       anchor="center"
   )


   def back_hover(e):
       back_button.config(bg=RED, fg=WHITE)


   def back_leave(e):
       back_button.config(bg=GREY, fg="black")


   back_button.bind("<Enter>", back_hover)
   back_button.bind("<Leave>", back_leave)
   back_button.bind("<Button-1>", lambda e: show_main_menu())

   canvas.create_window(140, 520, window=back_button)

help_button = create_icon_button("?", show_help)
sound_button = create_icon_button("🔊", toggle_sound)


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

show_main_menu()


root.mainloop()
