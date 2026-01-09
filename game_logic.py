import random

class NimGame:
    def __init__(self):
        """
        Initialize game objects
        """
        #Initial a list of dictionaries for multiple piles
        self.piles = []
        #Initial a variable to store the status of whose turn is it currently
        self.current_player = None

    def start_game(self, first_player, difficulty_level):
        """
        Start the game and set up piles based on difficulty.
        """
        #first_player: "Player" or "Computer"
        self.current_player = first_player
        self.piles = [] # Clear previous game data
        print(f"Game initialization complete")

        # difficulty_level: 1, 2, 3 (corresponds to number of piles)
        if difficulty_level == 1:
            # Easy: 1 pile of 20 coins (Classic version)
            config = [20]
        elif difficulty_level == 2:
            # Medium: 2 piles
            config = [10, 15]
        else:
            # Hard: 3 piles (Standard Nim Game)
            config = [3, 5, 7]

            # Create a list of dictionaries
        for i, count in enumerate(config):
                self.piles.append({'id': i, 'count': count})

    def take_coins(self, pile_index, num_to_take):
        """
        The logic of players taking coins
        """
        # 1.Safety check: Index validation
        # pile_index: The index of the pile you want to take
        if pile_index < 0 or pile_index >= len(self.piles):
            print(f"[Error] Invalid pile index: {pile_index}")
            return False
        target_pile = self.piles[pile_index]

        # 1.Safety check: Amount validation
        if num_to_take < 1 or num_to_take > target_pile['count']:
            print(f"[Error] Invalid amount {num_to_take} from pile {pile_index}")
            return False

        # 2.Perform subtraction
        target_pile['count'] -= num_to_take
        print(f"{self.current_player} took {num_to_take} from pile {pile_index}")

        # Check if there is a winner,or switch turn
        if self.is_game_over():
            print(f"Game Over. Winner: {self.current_player}")
        else:
            self.switch_turn()
        return True

    def switch_turn(self):
        """
        Switch turn
        """
        self.current_player = "Computer" if self.current_player == "Player" else "Player"

    def is_game_over(self):
        # Game is not over if there is a not empty pile
        for pile in self.piles:
            if pile['count'] > 0:
                return False
        return True


    def computer_move(self):
        """
        Computer's turn
        """
        # Find available pile
        available_piles = []
        for pile in self.piles:
            if pile['count'] > 0:
                available_piles += [pile]
        if not available_piles:
            return
        # The computer will randomly choose a pile
        chosen_pile = random.choice(available_piles)
        # The computer will randomly select 1 to 3 (or all of the remaining ones).
        max_allowed = min(3, chosen_pile['count'])
        num_to_take = random.randint(1, max_allowed)
        # The computer also needs to call “take_coins” to perform the operation.
        self.take_coins(chosen_pile['id'], num_to_take)