import tkinter as tk
from tkinter import Canvas
import pygame
import os
import random

pygame.mixer.init()
sound_on = True
is_paused = False

root = tk.Tk()
root.title("New Zealand Quiz")
root.geometry("1000x600")
root.resizable(False, False)

NAVY = "#0b0f5c"
RED = "#e21b23"
WHITE = "#ffffff"
GREY = "#d9d9d9"
DARK_NAVY = "#060a3d"

selected_category = ""

player_name = ""
current_q_index = 0
score = 0
quiz_questions = []


GENERAL_KNOWLEDGE_QUESTIONS = [
   {
       "question": "What year was television first broadcast\nin New Zealand?",
       "choices": ["1960", "1961", "1962", "1963"],
       "answer": "1960"
   },
   {
       "question": "What is the name of the famous New Zealander\non the $100 note?",
       "choices": ["James Fisher", "Glen O’Conner", "Edmund Hillary", "Ernest Rutherford"],
       "answer": "Ernest Rutherford"
   },
   {
       "question": "What is the capital of New Zealand?",
       "choices": ["Auckland", "Christchurch", "Dunedin", "Wellington"],
       "answer": "Wellington"
   }
]


MUSIC_FOLDER = "songs"

if not os.path.exists(MUSIC_FOLDER):
   os.makedirs(MUSIC_FOLDER)

music_files = [
   file for file in os.listdir(MUSIC_FOLDER)
   if file.endswith(".mp3")
]

current_song = ""

def play_song(song_name):
   global current_song, sound_on, is_paused


   sound_on = True
   is_paused = False
   sound_button.config(text="🔊")
   pause_button.config(text="⏸")


   current_song = song_name.replace(".mp3", "")
   song_path = os.path.join(MUSIC_FOLDER, song_name)


   try:
       pygame.mixer.music.load(song_path)
       pygame.mixer.music.set_volume(float(volume_slider.get()))
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
   if not pygame.mixer.music.get_busy() and sound_on and not is_paused:
       play_random_music()
   root.after(1000, check_music)



def set_volume(val):
   pygame.mixer.music.set_volume(float(val))




def toggle_pause():
   global is_paused
   if not pygame.mixer.music.get_busy() and not is_paused:
       return


   if is_paused:
       pygame.mixer.music.unpause()
       pause_button.config(text="⏸")
       is_paused = False
   else:
       pygame.mixer.music.pause()
       pause_button.config(text="▶")
       is_paused = True




hover_job = None




def show_audio_controls(e):
   global hover_job
   if hover_job:
       root.after_cancel(hover_job)
       hover_job = None


   if canvas.find_withtag("pause_win"):
       return


   canvas.create_window(915, 560, window=pause_button, tags="pause_win", anchor="center")
   canvas.create_window(845, 560, window=volume_slider, tags="slider_win", anchor="center")




def hide_audio_controls(e):
   global hover_job
   if hover_job:
       root.after_cancel(hover_job)
   hover_job = root.after(300, perform_hide)




def keep_controls_alive(e):
   global hover_job
   if hover_job:
       root.after_cancel(hover_job)
       hover_job = None




def perform_hide():
   canvas.delete("pause_win")
   canvas.delete("slider_win")




def open_custom_track_selector():
   if canvas.find_withtag("custom_popup_win"):
       return


   popup_frame = tk.Frame(root, bg=DARK_NAVY, bd=3, relief="solid", highlightbackground=RED, highlightcolor=RED)


   tk.Label(
       popup_frame,
       text="Select a Track",
       font=("Times New Roman", 14, "bold"),
       bg=DARK_NAVY,
       fg=WHITE
   ).pack(pady=10)


   list_frame = tk.Frame(popup_frame, bg=DARK_NAVY)
   list_frame.pack(fill="both", expand=True, padx=15)


   scrollbar = tk.Scrollbar(list_frame)
   scrollbar.pack(side="right", fill="y")


   listbox = tk.Listbox(
       list_frame, bg=GREY, fg="black", font=("Arial", 10),
       selectmode="single", yscrollcommand=scrollbar.set, relief="flat", highlightthickness=0
   )
   listbox.pack(side="left", fill="both", expand=True)
   scrollbar.config(command=listbox.yview)


   for file in music_files:
       listbox.insert("end", file.replace(".mp3", ""))


   def select_and_close():
       selection = listbox.curselection()
       if selection:
           play_song(music_files[selection[0]])
       close_popup()


   def close_popup():
       popup_frame.destroy()
       canvas.delete("custom_popup_win")


   btn_frame = tk.Frame(popup_frame, bg=DARK_NAVY)
   btn_frame.pack(pady=15)


   tk.Button(btn_frame, text="Play", font=("Arial", 10, "bold"), bg=RED, fg=WHITE, width=8,
             command=select_and_close).pack(side="left", padx=5)
   tk.Button(btn_frame, text="Cancel", font=("Arial", 10), bg=GREY, fg="black", width=8, command=close_popup).pack(
       side="left", padx=5)


   canvas.create_window(500, 300, window=popup_frame, width=320, height=380, tags="custom_popup_win")




def flash_sound_instruction():
   canvas.delete("sound_btn_win")


   msg_box = tk.Label(
       root, text="To play music,\npress the sound\nbutton and\nchoose a song",
       font=("Arial", 9, "bold"), bg=WHITE, fg=NAVY, bd=2, relief="solid", padx=5, pady=5
   )


   canvas.create_window(1000 - 40, 600 - 40, window=msg_box, tags="msg_box_win")
   root.after(4000, lambda: restore_sound_button(msg_box))




def restore_sound_button(msg_box_widget):
   msg_box_widget.destroy()
   canvas.delete("msg_box_win")
   canvas.create_window(1000 - 40, 600 - 40, window=sound_button, tags="sound_btn_win")



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


   start_button.bind("<Button-1>", lambda e: start_quiz(category, name_entry.get()))
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

def start_quiz(category, name):
   global player_name, quiz_questions, current_q_index, score
   player_name = name.strip()
   current_q_index = 0
   score = 0
   quiz_questions = GENERAL_KNOWLEDGE_QUESTIONS
   show_question_page()




def show_question_page():
   draw_background()
   global current_q_index, score
   current_q = quiz_questions[current_q_index]


   canvas.create_text(60, 45, text=current_q["question"], fill=WHITE, font=("Times New Roman", 24, "bold"),
                      anchor="nw")
   canvas.create_rectangle(680, 40, 960, 90, fill=RED, outline="")
   canvas.create_text(690, 65, text=f"Points: {score}", fill=WHITE, font=("Times New Roman", 22, "bold"), anchor="w")
   canvas.create_rectangle(500, 150, 920, 430, fill="#050738", outline=GREY, width=1)


   start_y = 195


   for idx, choice in enumerate(current_q["choices"]):
       y_pos = start_y + (idx * 65)


       bar_id = canvas.create_rectangle(80, y_pos, 420, y_pos + 45, fill=WHITE, outline="")


       text_id = canvas.create_text(250, y_pos + 22, text=choice, fill="black", font=("Times New Roman", 18, "italic"),
                                    anchor="center")


       def on_click(e, c=choice): handle_answer(c)


       canvas.tag_bind(bar_id, "<Button-1>", on_click)
       canvas.tag_bind(text_id, "<Button-1>", on_click)


   if sound_on: update_now_playing_text()
   draw_icon_buttons()




def handle_answer(selected_choice):
   global current_q_index, score
   if selected_choice == quiz_questions[current_q_index]["answer"]:
       score += 10
   current_q_index += 1
   if current_q_index < len(quiz_questions):
       show_question_page()
   else:
       show_main_menu()




help_button = create_icon_button("?", show_help)
sound_button = create_icon_button("🔊", open_custom_track_selector)


pause_button = tk.Button(
   root, text="⏸", font=("Segoe UI Emoji", 11),
   bg=NAVY, fg=WHITE, bd=1, relief="solid", width=3, command=toggle_pause
)


volume_slider = tk.Scale(
   root, from_=0.0, to=1.0, resolution=0.05, orient="horizontal",
   showvalue=False, bg=NAVY, fg=WHITE, highlightthickness=0, troughcolor=GREY,
   activebackground=RED, length=100, command=set_volume
)
volume_slider.set(0.35)


sound_button.bind("<Enter>", show_audio_controls)
sound_button.bind("<Leave>", hide_audio_controls)


pause_button.bind("<Enter>", keep_controls_alive)
pause_button.bind("<Leave>", hide_audio_controls)


volume_slider.bind("<Enter>", keep_controls_alive)
volume_slider.bind("<Leave>", hide_audio_controls)


check_music()
show_main_menu()
flash_sound_instruction()


root.mainloop()
