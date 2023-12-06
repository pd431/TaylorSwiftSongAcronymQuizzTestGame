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

def game_logic(album_choice, player_name):
    score, question = 0, 0

    while True:
        if album_choice == "all":
            selected_album = random.choice(albums_data['albums'])
        else:
            selected_album = next((album for album in albums_data['albums'] if album['name'].lower() == album_choice.lower()), None)
            if not selected_album:
                print(f"No album found with the name {album_choice}.")
                break

        album_name = selected_album['name']
        song_title = random.choice(selected_album['songs'])
        song_hint = process_song_title(song_title)

        question += 1
        display_question(album_name, song_hint, question)

        correct_guess = False
        for attempt in range(1, 3):  # Two attempts
            if handle_guess(song_title):
                correct_guess = True
                print("Correct!")
                score = update_score(score, True, attempt)
                print(f"Score: {score}")
                break
            else:
                if attempt == 1:
                    print("Wrong guess. Try again.")
                else:
                    print(f"No more attempts. The correct answer was: {song_title}")
                    break

        if not correct_guess:
            break

    print(f"Game over. Your final score is {score}.")
    save_score(player_name, score)
    display_top_scores()

def save_score(player_name, score):
    scores = []

    try:
        with open("scores.csv", "r") as file:
            scores = [line.strip().split(",") for line in file.readlines()]
    except FileNotFoundError:
        pass

    existing_score = next((s for s in scores if s[0] == player_name), None)
    if existing_score and int(existing_score[1]) < score:
        scores.remove(existing_score)
        scores.append([player_name, str(score)])
    elif not existing_score:
        scores.append([player_name, str(score)])

    with open("scores.csv", "w") as file:
        for s in scores:
            file.write(",".join(s) + "\n")

    # Custom message based on score
    if score < 10:
        print("Well, you didn't do very well now, did you?")
    elif score < 50:
        print("I guess you did okay, well done, your knowledge of Taylor Swift songs isn't too bad.")
    else:
        print("Well done, you have a brilliant knowledge of Taylor Swift songs :D")


def display_top_scores():
    try:
        with open("scores.csv", "r") as file:
            scores = [line.strip().split(",") for line in file.readlines()]
            scores.sort(key=lambda x: int(x[1]), reverse=True)

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

def game_menu(player_name):
    last_choice = None

    while True:
        if not last_choice:
            print(f"{cr.Fore.WHITE}{cr.Style.BRIGHT}Love's a game, wanna play?")
            print(f"{cr.Fore.WHITE}{cr.Style.BRIGHT}1. Play with all song titles")
            print(f"{cr.Fore.WHITE}{cr.Style.BRIGHT}2. Play with a specific album")
            print(f"{cr.Fore.WHITE}{cr.Style.BRIGHT}3. View top scores")
            print(f"{cr.Fore.WHITE}{cr.Style.BRIGHT}4. Exit")

            choice = input("Enter your choice (1-4): ")
        else:
            choice = last_choice

        if choice == "1":
            game_logic("all", player_name)
            last_choice = "1"
        elif choice == "2":
            if not last_choice:
                album_choice = input("Enter the album name: ").title()
            game_logic(album_choice, player_name)
            last_choice = "2"
        elif choice == "3":
            display_top_scores()
            last_choice = None
        elif choice == "4":
            print(f"{cr.Fore.WHITE}{cr.Style.BRIGHT}Goodbye, goodbye, goodbye, you were bigger than the whole sky")
            break
        else:
            print(f"{cr.Fore.RED}{cr.Style.DIM}Please choose a valid option.")
            last_choice = None

        play_again = input("Do you want to play another game? (Press Enter for Yes or type 'no'): ").lower()
        if play_again == "no":
            last_choice = None



def start_game():
    print("Welcome to the Taylor Swift Song Guessing Game!")
    title_intro()
    main_intro()
    player_name = player_login()
    game_menu(player_name)



if __name__ == "__main__":
    start_game()
