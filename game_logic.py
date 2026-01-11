import random

# Create a Nim game class
class NimGame:
    """
    Initialize game objects
    """
    def __init__(self):

        #Initial a list to store multiple piles (which are dictionaries)
        self.piles = []
        #Initial a variable to store the status of whose turn is it currently
        self.current_player = None


    def game_config(self, difficulty_level):

        # Clear previous game data
        self.piles = []
        print(f"Game initialization complete")

        # difficulty_level: 1, 2, 3 (corresponds to number of piles)
        if difficulty_level == 1:
            # Easy: 1 pile of 20 coins (Classic version)
            config = [20]
        elif difficulty_level == 2:
            # Medium: 3 piles (Standard Nim Game)
            config = [10, 15]
        else:
            # Hard: 3 piles (Standard Nim Game)
            config = [3, 5, 7]

            # Create a list of dictionaries
        for i, count in enumerate(config):
                self.piles.append({'id': i, 'count': count})

    """
    Firstly clear all the widgets to start
    """
    def roll_dice_for_starter(self):

        # The score is calculated in the background (if there is a tie, a re-bet is immediately made until a winner is determined).
        p_roll = random.randint(1, 6)
        c_roll = random.randint(1, 6)
        while p_roll == c_roll:
            p_roll = random.randint(1, 6)
            c_roll = random.randint(1, 6)

        # Decide the starter by the rolling point
        starter = "Player" if p_roll > c_roll else "Computer"
        return p_roll, c_roll,starter


    """
    The logic of players taking coins
    """
    def take_coins(self, pile_index, num_to_take):
        # 1.Safety check: Index validation
        # pile_index: The index of the pile you want to take
        if pile_index < 0 or pile_index >= len(self.piles):
            print(f"[Error] Invalid pile index: {pile_index}")
            return False
        target_pile = self.piles[pile_index]

        # 1.Safety check: Amount validation
        if num_to_take < 1 or num_to_take > 300 or num_to_take > target_pile['count']:
            print(f"[Error] Invalid amount {num_to_take} from pile {pile_index}")
            return False

        # 2.Execute the subtraction
        target_pile['count'] -= num_to_take
        print(f"{self.current_player} took {num_to_take} from pile {pile_index}")

        # Check if there is a winner,or switch turn
        if self.is_game_over():
            print(f"Game Over. Winner: {self.current_player}")
        else:
            self.switch_turn()
        return True

    """
    Switch turn
    """
    def switch_turn(self):
        self.current_player = "Computer" if self.current_player == "Player" else "Player"
        return self.current_player

    """
    Function checks if the game is over
    """
    def is_game_over(self):
        # Game is not over if there is a not empty pile
        for pile in self.piles:
            if pile['count'] > 0:
                return False
        return True

    """
    Computer's strategy
    """
    def computer_move(self):
        # Find available pile
        available_piles = []
        for pile in self.piles:
            if pile['count'] > 0:
                available_piles += [pile]
        if not available_piles:
            return
        # The computer will randomly choose a pile
        chosen_pile = random.choice(available_piles)

        # Find the max allowance
        max_allowed = min(3, chosen_pile['count'])

        # The computer will randomly select 1 to 3 (or all of the remaining ones).
        num_to_take = random.randint(1, max_allowed)

        # The computer also needs to call “take_coins” to perform the operation.
        self.take_coins(chosen_pile['id'], num_to_take)
