import json
import random
import colorama as cr
cr.init(autoreset=True)

def load_data_from_json():
    with open('albums.json', 'r') as file:
        data = json.load(file)
    return data

albums_data = load_data_from_json()

def process_song_title(song_title):
    song_title_with_space = song_title + " "
    words = song_title_with_space.split(" ")
    first_words = words[:-1]
    last_word = words[-1]
    first_letters = [x[0] for x in first_words]
    return "{} {}".format(" ".join(first_letters), last_word)

def handle_guess(correct_answer):
    guess = input("What is the song title? ").lower()
    return guess == correct_answer.lower()

def update_score(current_score, is_correct, attempt):
    if is_correct:
        return current_score + (3 if attempt == 1 else 1)
    return current_score

def display_question(album, song_hint, question_number):
    print(f"\n{question_number}) {album} - {song_hint}")

def player_login():
    while True:
        entered_password = input("Password: ").lower()
        if entered_password == 'blondie':
            print("Hey, you got it right, you're not completely dumb!")
            break
        else:
            print("Ha, you got it wrong")
            print("You are not worthy")
            print("But I'll let you try again because I'm nice\n")

    player_name = input("\nPlease enter your name: ").strip()
    while not player_name:
        print("You need to actually enter a name!")
        player_name = input("Please enter your name: ").strip()

    print(f"\n{player_name}, nice to meet you, where you been?")
    print("Baby let the games begin\n")
    return player_name

def game_logic(player_name):
    score, question = 0, 0

    while True:
        selected_album = random.choice(albums_data['albums'])
        album_name = selected_album['name']
        song_title = random.choice(selected_album['songs'])
        song_hint = process_song_title(song_title)

        question += 1
        display_question(album_name, song_hint, question)

        attempt = 0
        while attempt < 2:
            attempt += 1
            if handle_guess(song_title):
                print("Correct!")
                score = update_score(score, True, attempt)
                break
            else:
                print("Wrong guess. Try again." if attempt == 1 else "No more attempts.")
        
        if attempt == 2 and not handle_guess(song_title):
            print(f"The correct answer was {song_title}.")
            break

        print(f"Your current score is: {score}")

    print(f"Game over. Your final score is {score}.")
    save_score(player_name, score)
    display_top_scores()

def save_score(player_name, score):
    with open("scores.csv", "a") as file:
        file.write(f"{player_name},{score}\n")
    print("Your score has been saved.")

def display_top_scores():
    try:
        with open("scores.csv", "r") as file:
            scores = [line.strip().split(",") for line in file.readlines()]
            scores.sort(key=lambda x: int(x[1]), reverse=True)  # Sort by score in descending order

        print("\nTop Scores:")
        for name, score in scores:
            print(f"{name} - {score}")
    except FileNotFoundError:
        print("No scores recorded yet.")

def title_intro():
    print(f"{cr.Fore.YELLOW}   _______       __")
    print(f"{cr.Fore.YELLOW} /   ------.   / ._`_")
    print(f"{cr.Fore.YELLOW}|  /         ~--~    \"                                                      _                                  ")
    print(f"{cr.Fore.YELLOW}| |             __    `.____________________ _^-----^         -/-__,        //  _,_ ,_      ,       ,_ .  /) -/-") 
    print(f"{cr.Fore.YELLOW}| |  I=|=======/--\=========================| o o o |        _/_(_/(__(_/__(/__(_/_/ (_   _/_)__/_/_/_/__//__/_ ")
    print(f"{cr.Fore.YELLOW}\ |  I=|=======\__/=========================|_o_o_o_|                 _/_                              _/       ")
    print(f"{cr.Fore.YELLOW} \|                   /                       ~    ~                 (/                                /)       ")
    print(f"{cr.Fore.YELLOW}  \       .---.    .                                                                                   `        ")
    print(f"{cr.Fore.YELLOW}     -----'     ~~''")
    print("\n")
    print(f"{cr.Fore.WHITE}{cr.Style.BRIGHT}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print()
    print(f"{cr.Fore.WHITE}{cr.Style.BRIGHT}                                                       By Cara")
    print()
    print(f"{cr.Fore.WHITE}{cr.Style.BRIGHT}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print()
    input()

def main_intro():
    input(f"{cr.Fore.WHITE}{cr.Style.BRIGHT}This is a Taylor Swift song acronym quiz game, made for my own amusement (and coding practice)")
    input(f"{cr.Fore.WHITE}{cr.Style.BRIGHT}You will be given the album title, and the first letter of each word in the song title")
    input(f"{cr.Fore.WHITE}{cr.Style.BRIGHT}Before you begin, you will have to guess the password")
    input(f"{cr.Fore.WHITE}{cr.Style.BRIGHT}I'll give you a hint: it's a nickname")
    print(f"{cr.Fore.WHITE}{cr.Style.BRIGHT}Good luck!")
    print()
    input()

def start_game():
    print("Welcome to the Taylor Swift Song Guessing Game!")
    title_intro()
    main_intro()
    player_name = player_login()
    game_logic(player_name)

if __name__ == "__main__":
    start_game()
