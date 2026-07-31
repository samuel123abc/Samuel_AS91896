import tkinter as tk
from tkinter import Canvas, messagebox
import pygame
import os
import random
from PIL import Image, ImageTk


# initialize pygame mixer for sound
pygame.mixer.init()
sound_on = True
is_paused = False


# main window setup
root = tk.Tk()
root.title("New Zealand Quiz")
root.geometry("1000x600")
root.resizable(True, True)


# main color scheme
NAVY = "#0b0f5c"
RED = "#e21b23"
GREEN = "#00a651"
WHITE = "#ffffff"
GREY = "#d9d9d9"
DARK_NAVY = "#060a3d"


# variables to keep track of game state
selected_category = ""
player_name = ""
current_q_index = 0
score = 0
quiz_questions = []


current_image_ref = None
current_screen = "main_menu"


# dictionary storing help text for each screen
HELP_TEXT = {
   "main_menu": {
       "title": "Main Menu - Help",
       "content": (
           "Welcome to the New Zealand Quiz!\n\n"
           "• Click on any category button on the left to start a quiz.\n"
           "• Use the sound icon in the bottom right to select background songs or adjust volume."
       )
   },
   "name_page": {
       "title": "Name Entry - Help",
       "content": (
           "Before starting the quiz:\n\n"
           "• Enter your name into the text box.\n"
           "• Names must contain only letters and spaces.\n"
           "• Numbers and special characters are not allowed.\n"
           "• Click 'Start Quiz' to proceed or '← Back' to pick another category."
       )
   },
   "question_page": {
       "title": "Quiz - Help",
       "content": (
           "How to play:\n\n"
           "• Read the question. Some questions require you to examine the image\n"
           "• Click one of the 4 answer choices on the left to submit your answer.\n"
           "• Each correct answer earns you 10 points.\n"
           "• Your current score and question number are shown in the red banner."
       )
   },
   "pass_screen": {
       "title": "Passed Quiz - Help",
       "content": (
           "Congratulations on passing!\n\n"
           "• You scored over 50 points!\n"
           "• Click 'Play Category Again' to retry this category.\n"
           "• Click 'Go To Home Screen' to return to the main menu and try another quiz."
       )
   },
   "fail_screen": {
       "title": "Failed Quiz - Help",
       "content": (
           "Unfortunate result!\n\n"
           "• You scored 50 points or fewer.\n"
           "• Click 'Try Again' to retry this category and improve your score.\n"
           "• Click 'Go Back Home' to select a different category."
       )
   }
}


# quiz questions for general knowledge
GENERAL_KNOWLEDGE_QUESTIONS = [
   {
       "question": "What year was television first broadcast\nin New Zealand?",
       "choices": ["1960", "1961", "1962", "1963"],
       "answer": "1960",
       "image": "images/q1gk.jpg"
   },
   {
       "question": "What is the name of the famous New Zealander\non the $100 note?",
       "choices": ["James Fisher", "Glen O’Conner", "Edmund Hillary", "Ernest Rutherford"],
       "answer": "Ernest Rutherford",
       "image": "images/q2gk.jpg"
   },
   {
       "question": "What is the capital of New Zealand?",
       "choices": ["Auckland", "Christchurch", "Dunedin", "Wellington"],
       "answer": "Wellington",
       "image": "images/q3gk.png"
   },
   {
       "question": "Who is New Zealand's Current Monarch?",
       "choices": ["King Edward", "King Charles", "Queen Elizabeth", "King Charlie"],
       "answer": "King Charles",
       "image": "images/q4gk.png"
   },
   {
       "question": "Complete the Title of this popular New Zealand \nsong by Kiwi Musician Dave Dobbyn?: Slice of ________",
       "choices": ["Cheese", "Life", "Heaven", "You"],
       "answer": "Heaven",
       "image": "images/q5gk.png"
   },
   {
       "question": "What is the Longest Running Soap Opera in New Zealand?",
       "choices": ["Country Calendar", "Shortland Street", "Emmerdale", "Coronation Street"],
       "answer": "Shortland Street",
       "image": "images/q6gk.jpg"
   },
   {
       "question": "What is the Name of the Traditional New Zealand Maori \nMethod of Cooking Food Using Heated Rocks Buried Underground?",
       "choices": ["Rock Oven", "Maori Oven", "Kupu", "Hangi"],
       "answer": "Hangi",
       "image": "images/q7gk.jpg"
   },
   {
       "question": "What Desert do Australians and New Zealanders both \nClaim as their Own?",
       "choices": ["Pavlova", "Lamington", "Fairy Bread", "Chocolate Cake"],
       "answer": "Pavlova",
       "image": "images/q8gk.png"
   },
   {
       "question": "What is the Name of the National Rugby Team of New Zealand?",
       "choices": ["The Kiwi's", "The Blackies", "The All Blacks", "The All Whites"],
       "answer": "The All Blacks",
       "image": "images/q9gk.webp"
   },
   {
       "question": "Which Sport was Richard Hadlee Known for Playing?",
       "choices": ["Cricket", "Rugby", "Golf", "Lawn Bowls"],
       "answer": "Cricket",
       "image": "images/q10gk.jpg"
   },
]


# quiz questions for native animals
NATIVE_ANIMALS_QUESTIONS = [
   {
       "question": "Which Native Animal is This?",
       "choices": ["Kiwi", "Kakapo", "NZ Falcon", "Pukeko"],
       "answer": "Kiwi",
       "image": "images/q1na.png"
   },
   {
       "question": "Which Native Animal is This?",
       "choices": ["Tui", "Pukeko", "Weka", "Tomtit"],
       "answer": "Pukeko",
       "image": "images/q2na.png"
   },
   {
       "question": "Which Native Animal is This?",
       "choices": ["Kakapo", "Kea", "NZ Dotterel", "NZ Pigeon"],
       "answer": "NZ Pigeon",
       "image": "images/q3na.png"
   },
   {
       "question": "Which Native Animal is This?",
       "choices": ["NZ Falcon", "Morepork", "Dabchick", "Fantail"],
       "answer": "Morepork",
       "image": "images/q4na.png"
   },
   {
       "question": "Which Native Animal is This?",
       "choices": ["Fantail", "Kakapo", "NZ Dotterel", "Tomtit"],
       "answer": "Fantail",
       "image": "images/q5na.png"
   },
   {
       "question": "Which Native Animal is This?",
       "choices": ["Shore Plover", "Rock Wren", "Spotted Shag", "Stitchbird"],
       "answer": "Spotted Shag",
       "image": "images/q6na.png"
   },
   {
       "question": "Which Native Animal is This?",
       "choices": ["Kingfisher", "Dabchick", "Chatham Island Pigeon", "Grey Warbler"],
       "answer": "Grey Warbler",
       "image": "images/q7na.png"
   },
   {
       "question": "Which Native Animal is This?",
       "choices": ["Black Petrel", "Brown Teal", "Bellbird", "Saddleback"],
       "answer": "Brown Teal",
       "image": "images/q8na.png"
   },
   {
       "question": "Which Native Animal is This?",
       "choices": ["Bellbird", "Saddleback", "Hutton's Shearwater", "Kaka"],
       "answer": "Hutton's Shearwater",
       "image": "images/q9na.png"
   },
   {
       "question": "Which Native Animal is This?",
       "choices": ["Australiasian Bittern", "Blue Duck", "Black-Fronted Tern", "Bell Bird"],
       "answer": "Bell Bird",
       "image": "images/q10na.png"
   }
]


# quiz questions for famous places
PLACES_QUESTIONS = [
   {
       "question": "Which Place is Famous for the Big L&P Bottle",
       "choices": ["Auckland", "Wellington", "Dargaville", "Paeroa"],
       "answer": "Paeroa",
       "image": "images/q1p.png"
   },
   {
       "question": "What is Coromandel Famous For?",
       "choices": ["Cathedral Cove", "Flying Pigs", "Piha Beach", "Geysers"],
       "answer": "Cathedral Cove",
       "image": "images/q2p.png"
   },
   {
       "question": "What is Dunedin Famous For?",
       "choices": ["Cheese Making", "Big, Snowy Mountains", "Scottish Heritage", "Irish Heritage"],
       "answer": "Scottish Heritage",
       "image": "images/q3p.png"
   },
   {
       "question": "Where is the Victorian Precinct Located",
       "choices": ["Otago", "Oamaru", "Whangarei", "Featherton"],
       "answer": "Oamaru",
       "image": "images/q4p.png"
   },
   {
       "question": "Where is the Hobbiton Movie Set Located",
       "choices": ["Matamata", "Queenstown", "Napier", "Cardrona"],
       "answer": "Matamata",
       "image": "images/q5p.png"
   },
   {
       "question": "What Part of New Zealand is Known as the\n'Adventure Capital of the World'",
       "choices": ["New Plymouth", "Gisborne", "Queenstown", "Rotorua"],
       "answer": "Queenstown",
       "image": "images/q6p.png"
   },
   {
       "question": "What is Mt Taranaki's Former Name?",
       "choices": ["Mt Egmont", "Mt Dobson", "Mt Ward", "Mt Arrowsmith"],
       "answer": "Mt Egmont",
       "image": "images/q7p.png"
   },
   {
       "question": "Which District is Mt Cook Located In?",
       "choices": ["Mackenzie District", "Murray District", "Birchwood District", "Trotter District"],
       "answer": "Mackenzie District",
       "image": "images/q8p.png"
   },
   {
       "question": "Where is Huka Falls Located",
       "choices": ["Tauranga", "Taupo", "Rotorua", "Coromandel"],
       "answer": "Taupo",
       "image": "images/q9p.png"
   },
   {
       "question": "Approximately How Many People Live in Stewart Island?",
       "choices": ["800-900", "10-20", "Nobody", "400-490"],
       "answer": "400-490",
       "image": "images/q10p.png"
   }
]


# quiz questions for nz slang
SLANG_QUESTIONS = [
   {
       "question": "What does 'Buggered' Mean",
       "choices": ["Sore", "Tired", "Happy", "Sad"],
       "answer": "Tired",
       "image": "images/q1s.webp"
   },
   {
       "question": "What is a 'Chilly Bin'",
       "choices": ["Bin to Keep Rubbish Cold", "A Cold Morning", "A Cold Night",
                   "Box for keeping drinks cold"],
       "answer": "A Cooler Box Used for Keeping Drinks Cold",
       "image": "images/q2s.jpg"
   },
   {
       "question": "What does 'The Wops' mean",
       "choices": ["Chopping Up Fruit Quickly", "Middle of Nowhere", "Cheering Loudly", "A Stupid Person"],
       "answer": "Middle of Nowhere",
       "image": "images/q3s.jpeg"
   },
   {
       "question": "What does 'Chocka Block' mean?",
       "choices": ["Full or Crowded", "Chopping up a Block of Cheese", "Building Blocks", "Throwing Up/Vomiting"],
       "answer": "Full or Crowded",
       "image": "images/q4s.jpg"
   },
   {
       "question": "What does 'Scull' Mean",
       "choices": ["Dead", "Break Something", "Drink Something Without Stopping", "Elderly Person"],
       "answer": "Drink Something Without Stopping",
       "image": "images/q5s.jpg"
   },
   {
       "question": "What is a 'Bogan'",
       "choices": ["An Uncultured Person", "Snot", "A Fat Person", "A Bald Person"],
       "answer": "An Uncultured Person",
       "image": "images/q6s.jpeg"
   },
   {
       "question": "What Does 'Yarn' mean",
       "choices": ["Roll Down a Hill", "A Friendly Chat", "Something Soft", "Wool"],
       "answer": "A Friendly Chat",
       "image": "images/q7s.jpeg"
   },
   {
       "question": "What is a 'Dunny'?",
       "choices": ["A Container for Storing Food", "Toilet", "A Dumb Person", "Completing A Task"],
       "answer": "Toilet",
       "image": "images/q8s.jpg"
   },
   {
       "question": "What Does 'Cark It' Mean?",
       "choices": ["Die", "Get Fired", "Move Country", "Stop Talking"],
       "answer": "Die",
       "image": "images/q9s.png"
   },
   {
       "question": "What Does it Mean for Someone to 'Have a Blue'",
       "choices": ["Have a Bad Day", "Get Painted Blue", "Have an Argument", "Have a Swim"],
       "answer": "Have an Argument",
       "image": "images/q10s.png"
   }
]


# check if songs folder exists, create it if missing, and load files
MUSIC_FOLDER = "songs"


if not os.path.exists(MUSIC_FOLDER):
   os.makedirs(MUSIC_FOLDER)


music_files = [
   file for file in os.listdir(MUSIC_FOLDER)
   if file.endswith(".mp3")
]


current_song = ""




# play a specific track and set button states
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




# pick a random track from the folder to play
def play_random_music():
   if not music_files or not sound_on:
       return
   song = random.choice(music_files)
   play_song(song)




# keep checking if music stopped so the next track plays automatically
def check_music():
   if not pygame.mixer.music.get_busy() and sound_on and not is_paused:
       play_random_music()
   root.after(1000, check_music)




# adjust volume
def set_volume(val):
   pygame.mixer.music.set_volume(float(val))




# pause or resume background music
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




# display pause button and volume slider on mouse hover
def show_audio_controls(e):
   global hover_job
   if hover_job:
       root.after_cancel(hover_job)
       hover_job = None


   if canvas.find_withtag("pause_win"):
       return


   canvas.create_window(915, 560, window=pause_button, tags="pause_win", anchor="center")
   canvas.create_window(845, 560, window=volume_slider, tags="slider_win", anchor="center")




# hide audio controls after a short delay
def hide_audio_controls(e):
   global hover_job
   if hover_job:
       root.after_cancel(hover_job)
   hover_job = root.after(300, perform_hide)




# stop controls from hiding if mouse stays over them
def keep_controls_alive(e):
   global hover_job
   if hover_job:
       root.after_cancel(hover_job)
       hover_job = None




# remove sound control widgets from the canvas
def perform_hide():
   canvas.delete("pause_win")
   canvas.delete("slider_win")




# popup window to pick a song from the list
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




# show a temporary popup message telling users how to play music
def flash_sound_instruction():
   canvas.delete("sound_btn_win")


   msg_box = tk.Label(
       root, text="To play music,\npress the sound\nbutton and\nchoose a song",
       font=("Arial", 9, "bold"), bg=WHITE, fg=NAVY, bd=2, relief="solid", padx=5, pady=5
   )


   canvas.create_window(1000 - 40, 600 - 40, window=msg_box, tags="msg_box_win")
   root.after(4000, lambda: restore_sound_button(msg_box))




# bring back the sound button after instruction prompt closes
def restore_sound_button(msg_box_widget):
   msg_box_widget.destroy()
   canvas.delete("msg_box_win")
   canvas.create_window(1000 - 40, 600 - 40, window=sound_button, tags="sound_btn_win")




# update current song title label on screen
def update_now_playing_text():
   if sound_on and current_song:
       canvas.itemconfig("now_playing", text=f"Now Playing: {current_song}")




# create main canvas for graphics
canvas = Canvas(root, width=1000, height=600, bg=NAVY, highlightthickness=0)
canvas.pack(fill="both", expand=True)




# clear and draw common background shapes
def draw_background():
   canvas.delete("all")
   canvas.create_text(
       20, 575, text="", fill=WHITE, font=("Arial", 10), anchor="w", tags="now_playing"
   )
   canvas.create_polygon(450, 600, 1000, 300, 1000, 340, 500, 600, fill=WHITE, outline="")
   canvas.create_polygon(520, 600, 1000, 360, 1000, 395, 580, 600, fill=RED, outline="")




# helper function to build small square icon buttons
def create_icon_button(symbol, command):
   return tk.Button(
       root, text=symbol, font=("Segoe UI Emoji", 16), bg=NAVY, fg=WHITE,
       activebackground=NAVY, activeforeground=WHITE, bd=1, relief="solid",
       width=3, height=1, command=command
   )




# display help popup based on active screen
def show_help():
   if canvas.find_withtag("help_popup_win"):
       return


   info = HELP_TEXT.get(current_screen, {
       "title": "Help",
       "content": "No instructions available for this page."
   })


   popup_frame = tk.Frame(root, bg=DARK_NAVY, bd=3, relief="solid", highlightbackground=RED, highlightcolor=RED)


   tk.Label(
       popup_frame,
       text=info["title"],
       font=("Times New Roman", 18, "bold"),
       bg=DARK_NAVY,
       fg=WHITE
   ).pack(pady=(15, 10))


   tk.Label(
       popup_frame,
       text=info["content"],
       font=("Arial", 11),
       bg=DARK_NAVY,
       fg=WHITE,
       justify="left",
       wraplength=400
   ).pack(pady=10, padx=20, fill="both", expand=True)


   def close_popup():
       popup_frame.destroy()
       canvas.delete("help_popup_win")


   btn_frame = tk.Frame(popup_frame, bg=DARK_NAVY)
   btn_frame.pack(pady=(5, 15))


   tk.Button(
       btn_frame,
       text="Close",
       font=("Arial", 10, "bold"),
       bg=RED,
       fg=WHITE,
       width=10,
       command=close_popup
   ).pack()


   canvas.create_window(500, 300, window=popup_frame, width=460, height=320, tags="help_popup_win")




# draw bottom-right corner buttons
def draw_icon_buttons(include_home=True):
   if include_home:
       canvas.create_window(1000 - 40, 600 - 40 - 120, window=home_button)
   canvas.create_window(1000 - 40, 600 - 40 - 60, window=help_button)
   canvas.create_window(1000 - 40, 600 - 40, window=sound_button, tags="sound_btn_win")




# create category buttons for main menu with hover colors
def create_menu_button(text, y):
   label = tk.Label(root, text=text, bg=GREY, fg="black", font=("Times New Roman", 18, "italic"), width=18,
                    anchor="center")
   label.bind("<Enter>", lambda e: label.config(bg=RED, fg=WHITE))
   label.bind("<Leave>", lambda e: label.config(bg=GREY, fg="black"))
   label.bind("<Button-1>", lambda e: open_name_page(text))
   canvas.create_window(200, y, window=label)




# build and show main menu page
def show_main_menu():
   global current_screen
   current_screen = "main_menu"


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


   draw_icon_buttons(include_home=False)




# build and show name entry page
def open_name_page(category):
   global selected_category, current_screen
   selected_category = category
   current_screen = "name_page"


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




# validate input name and start chosen quiz category
def start_quiz(category, name):
   global player_name, quiz_questions, current_q_index, score, selected_category


   clean_name = name.strip()


   # check for empty input
   if not clean_name:
       messagebox.showwarning("Name Required", "Please enter your name to begin the quiz.")
       return


   # check that name only contains letters and spaces
   if not clean_name.replace(" ", "").isalpha():
       messagebox.showwarning("Invalid Name", "Your name cannot contain numbers or special characters.")
       return


   selected_category = category
   player_name = clean_name
   current_q_index = 0
   score = 0


   if category == "General Knowledge":
       quiz_questions = GENERAL_KNOWLEDGE_QUESTIONS
       show_question_page()
   elif category == "Native Animals":
       quiz_questions = NATIVE_ANIMALS_QUESTIONS
       show_question_page()
   elif category == "Places":
       quiz_questions = PLACES_QUESTIONS
       show_question_page()
   elif category == "Slang":
       quiz_questions = SLANG_QUESTIONS
       show_question_page()
   else:
       show_main_menu()




# render question, image, and options for the current question
def show_question_page():
   global current_q_index, score, current_image_ref, current_screen
   current_screen = "question_page"


   draw_background()
   current_q = quiz_questions[current_q_index]


   canvas.create_text(
       60, 45,
       text=current_q["question"],
       fill=WHITE,
       font=("Times New Roman", 24, "bold"),
       anchor="nw"
   )


   canvas.create_rectangle(500, 150, 920, 430, fill="#050738", outline=GREY, width=1)


   try:
       opened_img = Image.open(current_q["image"])
       resized_img = opened_img.resize((400, 260))
       current_image_ref = ImageTk.PhotoImage(resized_img)
       canvas.create_image(710, 290, image=current_image_ref, anchor="center")
   except Exception as e:
       canvas.create_text(710, 290, text=f"[{current_q['image']}\nnot found]", fill=WHITE,
                          font=("Times New Roman", 16, "italic"), anchor="center")


   canvas.create_rectangle(500, 450, 920, 500, fill=RED, outline="")


   canvas.create_text(520, 475, text=f"Points: {score}", fill=WHITE, font=("Times New Roman", 20, "bold"),
                      anchor="w")


   canvas.create_text(900, 475, text=f"Q {current_q_index + 1}/{len(quiz_questions)}", fill=WHITE,
                      font=("Times New Roman", 20, "bold"),
                      anchor="e")


   start_y = 195


   for idx, choice in enumerate(current_q["choices"]):
       y_pos = start_y + (idx * 65)


       bar_id = canvas.create_rectangle(80, y_pos, 420, y_pos + 45, fill=WHITE, outline="")
       text_id = canvas.create_text(250, y_pos + 22, text=choice, fill="black", font=("Times New Roman", 18, "italic"),
                                    anchor="center")


       def on_enter(e, b=bar_id, t=text_id):
           canvas.itemconfig(b, fill=RED)
           canvas.itemconfig(t, fill=WHITE)


       def on_leave(e, b=bar_id, t=text_id):
           canvas.itemconfig(b, fill=WHITE)
           canvas.itemconfig(t, fill="black")


       def on_click(e, c=choice): handle_answer(c)


       canvas.tag_bind(bar_id, "<Button-1>", on_click)
       canvas.tag_bind(text_id, "<Button-1>", on_click)


       canvas.tag_bind(bar_id, "<Enter>", on_enter)
       canvas.tag_bind(text_id, "<Enter>", on_enter)
       canvas.tag_bind(bar_id, "<Leave>", on_leave)
       canvas.tag_bind(text_id, "<Leave>", on_leave)


   if sound_on: update_now_playing_text()
   draw_icon_buttons()




# check clicked answer, update score, and load next question or end screen
def handle_answer(selected_choice):
   global current_q_index, score
   if selected_choice == quiz_questions[current_q_index]["answer"]:
       score += 10
   current_q_index += 1
   if current_q_index < len(quiz_questions):
       show_question_page()
   else:
       show_completion_page()




# display final results screen based on pass or fail mark
def show_completion_page():
   global current_screen
   canvas.delete("all")


   passed = score > 50
   current_screen = "pass_screen" if passed else "fail_screen"


   banner_color = GREEN if passed else RED
   header_text = "Good Stuff!" if passed else "Sorry, You Failed"


   display_name = player_name if player_name else "Player"


   prefix = f"Well Done {display_name}" if passed else f"Sorry {display_name}"
   status_text = "PASSED" if passed else "FAILED"
   sub_text = f"{prefix}, You {status_text} the {selected_category} Category. You Got {score} Points"


   canvas.create_rectangle(0, 0, 1000, 600, fill=NAVY, outline="")


   canvas.create_text(
       20, 575, text="", fill=WHITE, font=("Arial", 10), anchor="w", tags="now_playing"
   )


   canvas.create_rectangle(-10, 20, 1010, 25, fill=WHITE, outline="")
   canvas.create_rectangle(-10, 25, 1010, 125, fill=banner_color, outline="")
   canvas.create_rectangle(-10, 125, 1010, 130, fill=WHITE, outline="")
   canvas.create_rectangle(-10, 130, 1010, 190, fill=banner_color, outline="")
   canvas.create_rectangle(-10, 190, 1010, 195, fill=WHITE, outline="")


   canvas.create_text(500, 75, text=header_text, fill=WHITE, font=("Times New Roman", 38, "bold"), anchor="center")
   canvas.create_text(500, 160, text=sub_text, fill=WHITE, font=("Times New Roman", 19, "bold"), anchor="center")


   if passed:
       btn1_text = "Go To Home Screen"
       btn1_cmd = show_main_menu
       btn2_text = "Play Category Again"
       btn2_cmd = lambda: start_quiz(selected_category, player_name)
   else:
       btn1_text = "Try Again"
       btn1_cmd = lambda: start_quiz(selected_category, player_name)
       btn2_text = "Go Back Home"
       btn2_cmd = show_main_menu


   b1_rect = canvas.create_rectangle(210, 265, 790, 315, fill=WHITE, outline="")
   b1_txt = canvas.create_text(500, 290, text=btn1_text, fill="black", font=("Times New Roman", 22, "italic"), anchor="center")


   b2_rect = canvas.create_rectangle(210, 360, 790, 410, fill=WHITE, outline="")
   b2_txt = canvas.create_text(500, 385, text=btn2_text, fill="black", font=("Times New Roman", 22, "italic"), anchor="center")


   def on_enter_1(e):
       canvas.itemconfig(b1_rect, fill=RED)
       canvas.itemconfig(b1_txt, fill=WHITE)


   def on_leave_1(e):
       canvas.itemconfig(b1_rect, fill=WHITE)
       canvas.itemconfig(b1_txt, fill="black")


   def on_enter_2(e):
       canvas.itemconfig(b2_rect, fill=RED)
       canvas.itemconfig(b2_txt, fill=WHITE)


   def on_leave_2(e):
       canvas.itemconfig(b2_rect, fill=WHITE)
       canvas.itemconfig(b2_txt, fill="black")


   canvas.tag_bind(b1_rect, "<Button-1>", lambda e: btn1_cmd())
   canvas.tag_bind(b1_txt, "<Button-1>", lambda e: btn1_cmd())
   canvas.tag_bind(b1_rect, "<Enter>", on_enter_1)
   canvas.tag_bind(b1_rect, "<Leave>", on_leave_1)
   canvas.tag_bind(b1_txt, "<Enter>", on_enter_1)
   canvas.tag_bind(b1_txt, "<Leave>", on_leave_1)


   canvas.tag_bind(b2_rect, "<Button-1>", lambda e: btn2_cmd())
   canvas.tag_bind(b2_txt, "<Button-1>", lambda e: btn2_cmd())
   canvas.tag_bind(b2_rect, "<Enter>", on_enter_2)
   canvas.tag_bind(b2_rect, "<Leave>", on_leave_2)
   canvas.tag_bind(b2_txt, "<Enter>", on_enter_2)
   canvas.tag_bind(b2_txt, "<Leave>", on_leave_2)


   if sound_on:
       update_now_playing_text()


   draw_icon_buttons(include_home=False)




# set up quick action buttons in lower corner
home_button = create_icon_button("🏠", show_main_menu)
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


# mouse event bindings for audio controls
sound_button.bind("<Enter>", show_audio_controls)
sound_button.bind("<Leave>", hide_audio_controls)


pause_button.bind("<Enter>", keep_controls_alive)
pause_button.bind("<Leave>", hide_audio_controls)


volume_slider.bind("<Enter>", keep_controls_alive)
volume_slider.bind("<Leave>", hide_audio_controls)


# start checking music, load home screen, and run app loop
check_music()
show_main_menu()
flash_sound_instruction()


root.mainloop()
