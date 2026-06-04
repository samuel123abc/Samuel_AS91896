import tkinter as tk
from tkinter import Canvas
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
fade_msg_id = None


def play_random_music():
    global current_song

    if not music_files or not sound_on:
        return

    song = random.choice(music_files)
    current_song = song.replace(".mp3", "")
    song_path = os.path.join(MUSIC_FOLDER, song)

    try:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play()
        update_now_playing_text()
    except:
        print("Error Playing Music")


def check_music():
    if not pygame.mixer.music.get_busy() and sound_on:
        play_random_music()
    root.after(1000, check_music)


def play_sound():
    if sound_on:
        try:
            pygame.mixer.music.load("click.mp3")
            pygame.mixer.music.play()
        except:
            print("Missing Sound File")


def toggle_sound():
    global sound_on, fade_msg_id
    sound_on = not sound_on

    if fade_msg_id:
        root.after_cancel(fade_msg_id)
        fade_msg_id = None

    if sound_on:
        sound_button.config(text="🔊")
        play_random_music()
    else:
        sound_button.config(text="🔇")
        pygame.mixer.music.stop()

        canvas.itemconfig(
            "now_playing",
            text="Sound Off... (Press 🔇 to enable music)"
        )

        fade_msg_id = root.after(3000, clear_sound_message)


def clear_sound_message():
    global fade_msg_id
    canvas.itemconfig("now_playing", text="")
    fade_msg_id = None


def update_now_playing_text():
    if sound_on and current_song:
        display_text = f"Now Playing: {current_song} | Press 🔊 button to mute music"
        canvas.itemconfig("now_playing", text=display_text)


canvas = Canvas(
    root,
    width=1000,
    height=600,
    bg=NAVY,
    highlightthickness=0
)
canvas.pack(fill="both", expand=True)


def draw_background():
    canvas.delete("all")

    canvas.create_text(
        20,
        575,
        text="",
        fill=WHITE,
        font=("Arial", 10),
        anchor="w",
        tags="now_playing"
    )

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


def draw_icon_buttons():
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
        LEFT_MARGIN,
        70,
        text="Welcome to the New Zealand Quiz",
        fill=WHITE,
        font=("Times New Roman", 32, "bold"),
        anchor="w"
    )

    canvas.create_text(
        LEFT_MARGIN,
        120,
        text="Test your knowledge on New Zealand’s Birds, Slang, Places and more",
        fill=WHITE,
        font=("Times New Roman", 16),
        anchor="w"
    )

    create_menu_button("General Knowledge", 220)
    create_menu_button("Native Animals", 270)
    create_menu_button("Places", 320)
    create_menu_button("Slang", 370)

    if sound_on:
        update_now_playing_text()
    else:
        if fade_msg_id:
            canvas.itemconfig("now_playing", text="Sound Off... (Press 🔇 to enable music)")

    draw_icon_buttons()


def open_name_page(category):
    global selected_category
    selected_category = category

    draw_background()

    LEFT_MARGIN = 80

    canvas.create_text(
        LEFT_MARGIN,
        70,
        text=f"{category}",
        fill=WHITE,
        font=("Times New Roman", 32, "bold"),
        anchor="w"
    )

    canvas.create_text(
        LEFT_MARGIN,
        120,
        text="Please enter your name to begin",
        fill=WHITE,
        font=("Times New Roman", 16),
        anchor="w"
    )

    name_entry = tk.Entry(
        root,
        font=("Times New Roman", 20),
        width=25,
        bd=2,
        relief="solid"
    )

    canvas.create_window(
        300,
        240,
        window=name_entry
    )

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

    canvas.create_window(
        220,
        330,
        window=start_button
    )

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
    back_button.bind(
        "<Button-1>",
        lambda e: show_main_menu()
    )

    canvas.create_window(
        140,
        520,
        window=back_button
    )

    if sound_on:
        update_now_playing_text()
    else:
        if fade_msg_id:
            canvas.itemconfig("now_playing", text="Sound Off... (Press 🔇 to enable music)")

    draw_icon_buttons()


help_button = create_icon_button("?", show_help)
sound_button = create_icon_button("🔊", toggle_sound)

play_random_music()
check_music()

show_main_menu()

root.mainloop()
