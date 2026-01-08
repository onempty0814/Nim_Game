import random

class NimGame:
    def __init__(self):
        """
        Initialize game objects
        self.pile_size: The number of coins in the storage
        self.current_player: Whose turn is it currently?
        """
        self.pile_size = 20  # Initial default value, which can also be modified in start_game.
        self.current_player = None

    def start_game(self, first_player, initial_count=20):
        """
        Start the game and set the parameters
        first_player: Who goes first? ("Player" or "Computer")
        initial_count: How many coins do you want to set in this game? (Default: 20)
        """
        self.current_player = first_player
        self.pile_size = initial_count
        print(f"Game initialization complete")
        print(f"Current inventory (pile_size): {self.pile_size}")
        print(f"First move player: {self.current_player}")

    def take_coins(self, num_to_take):
        """
        The logic of players taking coins
        num_to_take: The number of coins you want to take
        """
        # 1. Security check: Negative numbers and numbers exceeding the existing stock cannot be taken.
        if num_to_take < 1:
            print(f"[Error] At least 1 coin must be taken!")
            return False

        if num_to_take > self.pile_size:
            print(f"[Error] There are only {self.pile_size} coins left. You cannot take {num_to_take} coins!")
            return False

        # 2. Perform subtraction
        self.pile_size = self.pile_size - num_to_take
        print(f"{self.current_player} has taken {num_to_take} coins. Remaining inventory: {self.pile_size}")

        # 3. Check if the game is over (if not, switch turns).
        if self.pile_size > 0:
            self.switch_turn()
        else:
            print(f"Game over! The winner is: {self.current_player}!")
        return True  # Operation successful

    def switch_turn(self):
        """Switch turn"""
        if self.current_player == "Player":
            self.current_player = "Computer"
        else:
            self.current_player = "Player"

    def computer_move(self):
        """
        Computer's turn
        """
        if self.pile_size <= 0:
            return 0

        # The computer's strategy: randomly select 1 to 3 (or all of the remaining ones).
        max_allowed = min(3, self.pile_size)
        num_to_take = random.randint(1, max_allowed)

        # The computer also needs to call “take_coins” to perform the operation.
        self.take_coins(num_to_take)
        return num_to_take