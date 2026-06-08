import tkinter as tk
from tkinter import Canvas, Toplevel, Listbox, SINGLE
import pygame
import os
import random

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

MUSIC_FOLDER = "songs"

if not os.path.exists(MUSIC_FOLDER):
    os.makedirs(MUSIC_FOLDER)

music_files = [
   file for file in os.listdir(MUSIC_FOLDER)
   if file.endswith(".mp3")
]

current_song = ""

def play_song(song_name):
   global current_song, sound_on


   sound_on = True
   sound_button.config(text="🔊")


   current_song = song_name.replace(".mp3", "")
   song_path = os.path.join(MUSIC_FOLDER, song_name)


   try:
       pygame.mixer.music.load(song_path)
       pygame.mixer.music.set_volume(0.35)
       pygame.mixer.music.play()
       update_now_playing_text()
   except:
       print(f"Could not play {song_name}")




def play_random_music():
   if not music_files or not sound_on:
       return
   song = random.choice(music_files)
   play_song(song)



def check_music():
   if not pygame.mixer.music.get_busy() and sound_on:
       play_random_music()
   root.after(1000, check_music)



def open_song_selector():
   popup = Toplevel(root)
   popup.title("Select a Track")
   popup.geometry("300x400")
   popup.configure(bg=NAVY)
   popup.resizable(False, False)

   tk.Label(
       popup,
       text="Available Tracks",
       font=("Times New Roman", 14, "bold"),
       bg=NAVY,
       fg=WHITE
   ).pack(pady=10)

   listbox = Listbox(popup, bg=GREY, fg="black", font=("Arial", 11), selectmode=SINGLE)
   listbox.pack(fill="both", expand=True, padx=20, pady=10)

   for file in music_files:
       listbox.insert("end", file.replace(".mp3", ""))


   def on_select():
       selection = listbox.curselection()
       if selection:
           index = selection[0]
           chosen_song = music_files[index]
           play_song(chosen_song)
           popup.destroy()

   tk.Button(
       popup,
       text="Play Track",
       font=("Arial", 11, "bold"),
       bg=RED,
       fg=WHITE,
       command=on_select
   ).pack(pady=15)

def flash_sound_instruction():
   canvas.delete("sound_btn_win")

   msg_box = tk.Label(
       root,
       text="To play music,\npress the sound\nbutton and\nchoose a song",
       font=("Arial", 9, "bold"),
       bg=WHITE,
       fg=NAVY,
       bd=2,
       relief="solid",
       padx=5,
       pady=5
   )

   canvas.create_window(
       1000 - 40,
       600 - 40,
       window=msg_box,
       tags="msg_box_win"
   )

   root.after(4000, lambda: restore_sound_button(msg_box))




def restore_sound_button(msg_box_widget):
   msg_box_widget.destroy()
   canvas.delete("msg_box_win")

   canvas.create_window(
       1000 - 40,
       600 - 40,
       window=sound_button,
       tags="sound_btn_win"
   )

def update_now_playing_text():
   if sound_on and current_song:
       canvas.itemconfig("now_playing", text=f"Now Playing: {current_song}")

canvas = Canvas(root, width=1000, height=600, bg=NAVY, highlightthickness=0)
canvas.pack(fill="both", expand=True)

def draw_background():
   canvas.delete("all")
   canvas.create_text(
       20, 575, text="", fill=WHITE, font=("Arial", 10), anchor="w", tags="now_playing"
   )
   canvas.create_polygon(450, 600, 1000, 300, 1000, 340, 500, 600, fill=WHITE, outline="")
   canvas.create_polygon(520, 600, 1000, 360, 1000, 395, 580, 600, fill=RED, outline="")

def create_icon_button(symbol, command):
   return tk.Button(
       root, text=symbol, font=("Segoe UI Emoji", 16), bg=NAVY, fg=WHITE,
       activebackground=NAVY, activeforeground=WHITE, bd=1, relief="solid",
       width=3, height=1, command=command
   )




def show_help():
   print("Help clicked")

def draw_icon_buttons():
   canvas.create_window(1000 - 40, 600 - 40 - 60, window=help_button)

   canvas.create_window(1000 - 40, 600 - 40, window=sound_button, tags="sound_btn_win")




def create_menu_button(text, y):
   label = tk.Label(root, text=text, bg=GREY, fg="black", font=("Times New Roman", 18, "italic"), width=18,
                    anchor="center")
   label.bind("<Enter>", lambda e: label.config(bg=RED, fg=WHITE))
   label.bind("<Leave>", lambda e: label.config(bg=GREY, fg="black"))
   label.bind("<Button-1>", lambda e: open_name_page(text))
   canvas.create_window(200, y, window=label)




def show_main_menu():
   draw_background()
   canvas.create_text(80, 70, text="Welcome to the New Zealand Quiz", fill=WHITE, font=("Times New Roman", 32, "bold"),
                      anchor="w")
   canvas.create_text(80, 120, text="Test your knowledge on New Zealand’s Birds, Slang, Places and more", fill=WHITE,
                      font=("Times New Roman", 16), anchor="w")


   create_menu_button("General Knowledge", 220)
   create_menu_button("Native Animals", 270)
   create_menu_button("Places", 320)
   create_menu_button("Slang", 370)


   if sound_on:
       update_now_playing_text()
   draw_icon_buttons()




def open_name_page(category):
   global selected_category
   selected_category = category
   draw_background()


   canvas.create_text(80, 70, text=f"{category}", fill=WHITE, font=("Times New Roman", 32, "bold"), anchor="w")
   canvas.create_text(80, 120, text="Please enter your name to begin", fill=WHITE, font=("Times New Roman", 16),
                      anchor="w")


   name_entry = tk.Entry(root, font=("Times New Roman", 20), width=25, bd=2, relief="solid")
   canvas.create_window(300, 240, window=name_entry)


   start_button = tk.Label(root, text="Start Quiz", bg=GREY, fg="black", font=("Times New Roman", 18, "italic"),
                           width=15, anchor="center")
   start_button.bind("<Enter>", lambda e: start_button.config(bg=RED, fg=WHITE))
   start_button.bind("<Leave>", lambda e: start_button.config(bg=GREY, fg="black"))
   start_button.bind("<Button-1>", lambda e: print(f"Starting {category} quiz for {name_entry.get()}"))
   canvas.create_window(220, 330, window=start_button)


   back_button = tk.Label(root, text="← Back", bg=GREY, fg="black", font=("Times New Roman", 16), width=10,
                          anchor="center")
   back_button.bind("<Enter>", lambda e: back_button.config(bg=RED, fg=WHITE))
   back_button.bind("<Leave>", lambda e: back_button.config(bg=GREY, fg="black"))
   back_button.bind("<Button-1>", lambda e: show_main_menu())
   canvas.create_window(140, 520, window=back_button)


   if sound_on:
       update_now_playing_text()
   draw_icon_buttons()

help_button = create_icon_button("?", show_help)
sound_button = create_icon_button("🔊", open_song_selector)

check_music()
show_main_menu()

flash_sound_instruction()


root.mainloop()
