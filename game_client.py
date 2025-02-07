
import tkinter as tk
from tkinter import *
import socket
from time import sleep
from PIL import ImageTk, Image
import threading

# MAIN GAME'S WINDOW AND VARIABLE
window_main = tk.Tk()
window_main.iconbitmap("icon.ico")
window_main.title("Game Client")
your_name = ""
opponent_name = ""
game_round = 0
game_timer = 4
your_choice = ""
opponent_choice = ""
TOTAL_NO_OF_ROUNDS = 3
your_score = 0
opponent_score = 0

# NETWORK
client = None
HOST_ADDR = "192.168.43.50"
HOST_PORT = 8000

# MAIN WINDOW
top_welcome_frame= tk.Frame(window_main)
lbl_name = tk.Label(top_welcome_frame, text = "Name:")
lbl_name.pack(side=tk.LEFT)
ent_name = tk.Entry(top_welcome_frame)
ent_name.pack(side=tk.LEFT)
btn_connect = tk.Button(top_welcome_frame, text="Connect", command=lambda : connect())
btn_connect.pack(side=tk.LEFT)
top_welcome_frame.pack(side=tk.TOP)

top_message_frame = tk.Frame(window_main)
lbl_line = tk.Label(top_message_frame, text="***********************************************************").pack()
lbl_welcome = tk.Label(top_message_frame, text="")
lbl_welcome.pack()
lbl_line_server = tk.Label(top_message_frame, text="***********************************************************")
lbl_line_server.pack_forget()
top_message_frame.pack(side=tk.TOP)

# PLAYER'S NAME SECTION
top_frame = tk.Frame(window_main)
top_left_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
lbl_your_name = tk.Label(top_left_frame, text="Your name: " + your_name, font = "Helvetica 13 bold")
lbl_opponent_name = tk.Label(top_left_frame, text="Opponent: " + opponent_name)
lbl_your_name.grid(row=0, column=0, padx=5, pady=8)
lbl_opponent_name.grid(row=1, column=0, padx=5, pady=8)
top_left_frame.pack(side=tk.LEFT, padx=(10, 10))

# TIMER SECTIONS
top_right_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
lbl_game_round = tk.Label(top_right_frame, text="Game round (x) starts in", foreground="blue", font = "Helvetica 14 bold")
lbl_timer = tk.Label(top_right_frame, text=" ", font = "Helvetica 24 bold", foreground="blue")
lbl_game_round.grid(row=0, column=0, padx=5, pady=5)
lbl_timer.grid(row=1, column=0, padx=5, pady=5)
top_right_frame.pack(side=tk.RIGHT, padx=(10, 10))

top_frame.pack_forget()

middle_frame = tk.Frame(window_main)

lbl_line = tk.Label(middle_frame, text="***********************************************************").pack()
lbl_line = tk.Label(middle_frame, text="**** GAME LOG ****", font = "Helvetica 13 bold", foreground="blue").pack()
lbl_line = tk.Label(middle_frame, text="***********************************************************").pack()

round_frame = tk.Frame(middle_frame)
lbl_round = tk.Label(round_frame, text="Round")
lbl_round.pack()
lbl_your_choice = tk.Label(round_frame, text="Your choice: " + "None", font = "Helvetica 13 bold")
lbl_your_choice.pack()
lbl_opponent_choice = tk.Label(round_frame, text="Opponent choice: " + "None")
lbl_opponent_choice.pack()
lbl_result = tk.Label(round_frame, text=" ", foreground="blue", font = "Helvetica 14 bold")
lbl_result.pack()
round_frame.pack(side=tk.TOP)

final_frame = tk.Frame(middle_frame)
lbl_line = tk.Label(final_frame, text="***********************************************************").pack()
lbl_final_result = tk.Label(final_frame, text=" ", font = "Helvetica 13 bold", foreground="blue")
lbl_final_result.pack()
lbl_line = tk.Label(final_frame, text="***********************************************************").pack()
final_frame.pack(side=tk.TOP)

middle_frame.pack_forget()

# BUTTONS PART 1
button_frame = tk.Frame(window_main)
prock = Image.open("rockUp.png")
pr = prock.resize((100,100), Image.ANTIALIAS)
photo_rock = ImageTk.PhotoImage(pr)
ppaper = Image.open("paperUp.png")
pp = ppaper.resize((100,100), Image.ANTIALIAS)
photo_paper = ImageTk.PhotoImage(pp)
pscissor = Image.open("scissorUp.png")
ps = pscissor.resize((100,100), Image.ANTIALIAS)
photo_scissors = ImageTk.PhotoImage(ps)

# BUTTONS PART 2
btn_rock = tk.Button(button_frame, text="Rock", command=lambda : choice("rock"), state=tk.DISABLED, image=photo_rock)
btn_paper = tk.Button(button_frame, text="Paper", command=lambda : choice("paper"), state=tk.DISABLED, image=photo_paper)
btn_scissors = tk.Button(button_frame, text="Scissors", command=lambda : choice("scissors"), state=tk.DISABLED, image=photo_scissors)
btn_rock.grid(row=0, column=0)
btn_paper.grid(row=0, column=1)
btn_scissors.grid(row=0, column=2)
button_frame.pack(side=tk.BOTTOM)

# GAME MECHANISMS
def game_logic(you, opponent):
    winner = ""
    rock = "rock"
    paper = "paper"
    scissors = "scissors"
    player0 = "you"
    player1 = "opponent"

    if you == opponent:
        winner = "draw"
    elif you == rock:
        if opponent == paper:
            winner = player1
        else:
            winner = player0
    elif you == scissors:
        if opponent == rock:
            winner = player1
        else:
            winner = player0
    elif you == paper:
        if opponent == scissors:
            winner = player1
        else:
            winner = player0
    return winner

# ENABLE OR DISABLE BUTTONS
def enable_disable_buttons(todo):
    if todo == "disable":
        btn_rock.config(state=tk.DISABLED)
        btn_paper.config(state=tk.DISABLED)
        btn_scissors.config(state=tk.DISABLED)
    else:
        btn_rock.config(state=tk.NORMAL)
        btn_paper.config(state=tk.NORMAL)
        btn_scissors.config(state=tk.NORMAL)

# ENTERS NAME AND CONNECT TO GAME
def connect():
    global your_name
    if len(ent_name.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        your_name = ent_name.get()
        lbl_your_name["text"] = "Your name: " + your_name
        connect_to_server(your_name)

# FUNCTION FOR TIMING COUTDOWN
def count_down(my_timer, nothing):
    global game_round
    if game_round <= TOTAL_NO_OF_ROUNDS:
        game_round = game_round + 1

    lbl_game_round["text"] = "Game round " + str(game_round) + " starts in"

    while my_timer > 0:
        my_timer = my_timer - 1
        print("game timer is: " + str(my_timer))
        lbl_timer["text"] = my_timer
        sleep(1)

    enable_disable_buttons("enable")
    lbl_round["text"] = "Round - " + str(game_round)
    lbl_final_result["text"] = ""

# FUNCTION FOR PLAYER CHOICE
def choice(arg):
    global your_choice, client, game_round
    your_choice = arg
    lbl_your_choice["text"] = "Your choice: " + your_choice

    if client:
        gr = "Game_Round"+str(game_round)+your_choice
        client.send(gr.encode())
        enable_disable_buttons("disable")

# CONNECT TO SERVER
def connect_to_server(name):
    global client, HOST_PORT, HOST_ADDR, your_name

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST_ADDR, HOST_PORT))
    names = name.encode()
    client.send(names) # Send name to server after connecting

    # DISABLE WIDGETS
    btn_connect.config(state=tk.DISABLED)
    ent_name.config(state=tk.DISABLED)
    lbl_name.config(state=tk.DISABLED)
    enable_disable_buttons("disable")

    # START TRHEAD
    threading._start_new_thread(receive_message_from_server, (client, "m"))

# RECEIVE MESSAGE FROM SERVER
def receive_message_from_server(sck, m):
    global your_name, opponent_name, game_round
    global your_choice, opponent_choice, your_score, opponent_score

    while True:
        from_server = sck.recv(4096)
        fromS = str(from_server.decode())
        if not from_server: break

        # RECEIVE WELCOME MESSAGE FROM SERVER
        if fromS.startswith("welcome"):
            print("yes")
            if fromS == "welcome1":
                lbl_welcome["text"] = "Server says: Welcome " + your_name + "! Waiting for player 2"
            elif fromS == "welcome2":
                lbl_welcome["text"] = "Server says: Welcome " + your_name + "! Game will start soon"
            lbl_line_server.pack()

        elif fromS.startswith("opponent_name$"):
            print(fromS)
            opponent_name = fromS.replace("opponent_name$", "")
            lbl_opponent_name["text"] = "Opponent: " + opponent_name
            top_frame.pack()
            middle_frame.pack()

            # WHEN 2 USER CONNECTED, GAME WILL START
            threading._start_new_thread(count_down, (game_timer, ""))
            lbl_welcome.config(state=tk.DISABLED)
            lbl_line_server.config(state=tk.DISABLED)

        elif fromS.startswith("$opponent_choice"):
            print("yes 3")
            # GET OPPONENT'S CHOICE
            opponent_choice = fromS.replace("$opponent_choice", "")

            # CONDITION FOR THE GAME MECHANICS
            who_wins = game_logic(your_choice, opponent_choice)
            round_result = " "
            if who_wins == "you":
                your_score = your_score + 1
                round_result = "WIN"
            elif who_wins == "opponent":
                opponent_score = opponent_score + 1
                round_result = "LOSS"
            else:
                round_result = "DRAW"

            # UPDATE THE GUI AFTER MOVES
            lbl_opponent_choice["text"] = "Opponent choice: " + opponent_choice
            lbl_result["text"] = "Result: " + round_result

            # GAME ROUNDS
            if game_round == TOTAL_NO_OF_ROUNDS:
                # compute final result
                final_result = ""
                color = ""

                # SCORING
                if your_score > opponent_score:
                    final_result = "(You Won!!!)"
                    color = "green"
                elif your_score < opponent_score:
                    final_result = "(You Lost!!!)"
                    color = "red"
                else:
                    final_result = "(Draw!!!)"
                    color = "black"

                lbl_final_result["text"] = "FINAL RESULT: " + str(your_score) + " - " + str(opponent_score) + " " + final_result
                lbl_final_result.config(foreground=color)

                enable_disable_buttons("disable")
                game_round = 0

            # START TIMER
            threading._start_new_thread(count_down, (game_timer, ""))


    sck.close()


window_main.mainloop()
