from game_logic import NimGame


def run_game():
    # 1. Instantiate game logic
    game = NimGame()

    # 2. Ask the user for configuration options
    print("Welcome to Nim Games!")

    # Choose one to go first
    choice = input("Do you want to go first? (Enter y or n):")
    if choice.lower() == 'y':
        starter = "Player"
    else:
        starter = "Computer"

    # Select difficulty level (number of coins)
    try:
        size_input = int(input("Please enter the initial number of coins (e.g., 20):"))
    except ValueError:
        size_input = 20  # Invalid input detected. Defaulting to 20 coins

    # 3. Pass the user's selection to the logic layer
    game.start_game(starter, size_input)

    # 4. Game main loop
    while game.pile_size > 0:
        print("\n-----------------")
        if game.current_player == "Player":
            # Player's turn: Ask how much to take
            try:
                user_take = int(input("Your turn! How many coins do you want to take (1-3)? "))
                # Call the logic layer to execute
                game.take_coins(user_take)
            except ValueError:
                print("Please enter a valid number!")
        else:
            # Computer Round
            print("The computer is thinking...")
            game.computer_move()


# Run the program
if __name__ == "__main__":
    run_game()