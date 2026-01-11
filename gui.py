import tkinter as tk
from tkinter import messagebox
from game_logic import NimGame

# Create a Nim game GUI
class NimGameGUI:
    """
    Initialize the main window and the game engine.
    """
    def __init__(self):
        # Create a game instance
        self.game = NimGame()
        pass

    """
    Creates the title page with difficulty buttons.
    """
    def create_main_menu(self):
        # Refresh when game over or back to main menu
        self.clear_window()
        # Title :
        tk.Label(self.root, text="Welcome to Nim Game", font=("Arial", 28, "bold")).pack(pady=40)
        tk.Label(self.root, text="Select Difficulty:", font=("Arial", 16)).pack(pady=10)
        # Buttons :
        # Easy difficulty
        Easy = tk.Button(self.root, text="Easy (1 Pile)", font=("Arial", 14), width=20, bg="#e1f5fe",command=lambda: self.show_roll_dice_for_starter_1(1))
        Easy.pack(pady=10)
        # Medium difficulty
        Medium = tk.Button(self.root, text="Medium (2 Piles)", font=("Arial", 14), width=20, bg="#fff9c4",command=lambda: self.show_roll_dice_for_starter_1(2))
        Medium.pack(pady=10)
        # Hard difficulty
        Hard = tk.Button(self.root, text="Hard (3 Piles)", font=("Arial", 14), width=20, bg="#ffcdd2",command=lambda: self.show_roll_dice_for_starter_1(3))
        Hard.pack(pady=10)



    def show_roll_dice_for_starter_1(self,difficulty):
        # Initialize the game differing from difficulty to define different attributes
        self.game.game_config(difficulty)
        # Clear all the widgets
        self.clear_window()
        # Show the default window
        title_roll_dice = tk.Label(self.root, text="🎲 Rolling Dice to decide the starter 🎲", font=("Arial", 24, "bold"))
        title_roll_dice.pack(pady=40)
        result_label = tk.Label(self.root, text="Click the button below to start rolling the dice.", font=("Arial", 20))
        result_label.pack(pady=20)
        start_rolling_button = tk.Button(self.root,text="Start rolling",font=("Arial", 16, "bold"),command=lambda: self.show_roll_dice_for_starter_2(start_rolling_button))
        start_rolling_button.pack(pady=20)

    def show_roll_dice_for_starter_2(self,start_rolling_button):
        # Remove the button
        start_rolling_button.destroy()
        # Execute rolling dice
        p_roll, c_roll, current_player= self.game.roll_dice_for_starter()
        # Show the rolling points result
        result_text = tk.Label(self.root, text=f"You: {p_roll}  vs  Computer: {c_roll}", font=("Arial", 20))
        result_text.pack(pady=20)
        # Show the starter
        winner_text = f"{current_player} goes first!"
        # If player won,it is green,or it is red
        color = "#4caf50" if current_player == "Player" else "#f44336"
        # Show the result
        result = tk.Label(self.root, text=winner_text, font=("Arial", 22, "bold"), fg=color)
        result.pack(pady=20)
        # Show the time prompt
        time_prompt = tk.Label(self.root, text="(Game starting in 3 seconds...)", font=("Arial", 12), fg="gray")
        time_prompt.pack(pady=10)
        # Set a timer: Automatically enter the game after 3 seconds
        self.root.after(3000, lambda: self.start_game_ui(current_player))

    def start_game_ui(self,current_player):
        # Feedback to prove it works
        print("Starter:", current_player)
        # Show the game screen
        self.show_game_window(current_player)

    """
    Draws the piles
    Redraws the whole screen every turn
    """
    def show_game_window(self,current_player):
        # Firstly clear the window
        self.clear_window()
        # Display whose turn it is currently.
        status_label = tk.Label(self.root, text=f"Turn: {current_player}", font=("Arial", 16, "bold"))
        status_label.pack(pady=10)
        # Draw each pile of coins using a loop.
        for pile in self.game.piles:
            pile_id = pile['id']
            count = pile['count']
            # Coins visualization: Repeat the letter 'O' 'count' times
            visual_coins = "O" * count
            # Display
            label_text = f"Pile {pile_id}: {visual_coins} ({count})"
            tk.Label(self.root, text=label_text, font=("Arial", 14), fg="blue").pack(pady=5)

        # Create "Back to Main Menu" button
        Back_to_Main_Menu = tk.Button(self.root, text="Back to Main Menu", font=("Arial", 14), bg="#2196f3", fg="white", width=15, command=self.create_main_menu)
        Back_to_Main_Menu.pack(side ='bottom',pady=5)
        # The input box and buttons are only displayed during the player's turn.
        if current_player == "Player":
            # Create input box
            input_frame = tk.Frame(self.root)
            input_frame.pack(pady=20)
            # Create the entry and label
            tk.Label(input_frame, text="Pile Index: ").pack(side=tk.LEFT)
            self.pile_entry = tk.Entry(input_frame, width=5)
            self.pile_entry.pack(side=tk.LEFT)
            # Create the entry and label
            tk.Label(input_frame, text="Amount(1-3): ").pack(side=tk.LEFT)
            self.amount_entry = tk.Entry(input_frame, width=5)
            self.amount_entry.pack(side=tk.LEFT)

            # Confirm button
            tk.Button(self.root, text="Take Coins", command=self.take_coins_handler).pack(pady=10)
        else:
            self.root.after(3000, self.execute_computer)



    def take_coins_handler(self):
        """
        Read the input, invoke the logic, and refresh the screen
        """
        try:
            # Get user input
            pile_idx = int(self.pile_entry.get())
            amount = int(self.amount_entry.get())

            # Call game logic to safety check and execute the substraction
            if_success = self.game.take_coins(pile_idx, amount)
            # Once the player has claimed the item correctly, the interface will refresh immediately to display the new status
            if if_success:
                self.show_game_window(self.game.current_player)
                # Check if this step by the player leads to the end of the game.
                if self.game.is_game_over():
                    # If game is over, open the checkout window
                    self.game_over_window()
                else:
                    # Execute the computer action after a 1.5-second pause.
                    self.root.after(1500, self.execute_computer)
            # If the input is not valid for current game status, show the error prompt
            else:
                messagebox.showerror("Invalid Move", "Check amount or pile index.")
        # If the input is not number,show the error prompt
        except ValueError:
            messagebox.showerror("Input Error", "Please enter numbers only.")

    """
    Function that takes over computer actions
    """
    def execute_computer(self):
        # 1. Computer move
        self.game.computer_move()

        # 2. Check if the game ends
        if self.game.is_game_over():
            self.game_over_window()
        else:
            self.current_player = self.game.current_player
            # 3. After the computer finishes, refresh the interface
            self.show_game_window(self.current_player)

    """
    Checkout window
    """
    def game_over_window(self):
        # Firstly clear all the widgets
        self.clear_window()
        # Get the winner from current player
        winner = self.game.current_player
        color = "#4caf50" if winner == "Player" else "#f44336"
        msg = "YOU WIN!" if winner == "Player" else "YOU LOST"
        # Create the labels
        tk.Label(self.root, text="GAME OVER", font=("Arial", 24, "bold")).pack(pady=40)
        tk.Label(self.root, text=msg, font=("Arial", 36, "bold"), fg=color).pack(pady=20)
        tk.Label(self.root, text=f"Winner: {winner}", font=("Arial", 16)).pack(pady=10)
        # Create "Back to Main Menu" button
        tk.Button(self.root, text="Back to Main Menu", font=("Arial", 14), bg="#2196f3", fg="white", width=15,command=self.create_main_menu).pack(pady=40)


    """
    Function created to clear screen
    """
    def clear_window(self):
        # Loop over all the widgets in window and then remove them
        for widget in self.root.winfo_children():
            widget.destroy()

    """
    Run program
    """
    def run(self):
        # Setup main window, title and size
        self.root = tk.Tk()
        self.root.title("Nim Game")
        window_width = 800
        window_height = 600
        # Get the width and height of your computer screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Calculate x (left margin) and y (top margin)
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        # Application settings
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        # Start with the Main menu
        self.create_main_menu()
        # Start the GUI loop
        self.root.mainloop()