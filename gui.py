import tkinter as tk
from tkinter import messagebox
from game_logic import NimGame

class NimGameGUI:
    def __init__(self):
        """
        Initialize the main window and the game engine.
        """
        self.game = NimGame()

        # Setup Main Window
        self.root = tk.Tk()
        self.root.title("Nim Game")
        self.root.geometry("600x400")
        # Start with the Main Menu
        self.create_main_menu()

    def create_main_menu(self):
        """Creates the title page with difficulty buttons."""

        # Refresh when game over or back to main menu
        self.clear_window()

        # Title
        tk.Label(self.root, text="Welcome to Nim Game", font=("Arial", 28, "bold")).pack(pady=40)
        tk.Label(self.root, text="Select Difficulty:", font=("Arial", 16)).pack(pady=10)

        # Buttons
        tk.Button(self.root, text="Easy (1 Pile)", font=("Arial", 14), width=20, bg="#e1f5fe",
                  command=lambda: self.start_game_ui(1)).pack(pady=10)

        tk.Button(self.root, text="Medium (2 Piles)", font=("Arial", 14), width=20, bg="#fff9c4",
                  command=lambda: self.start_game_ui(2)).pack(pady=10)

        tk.Button(self.root, text="Hard (3 Piles)", font=("Arial", 14), width=20, bg="#ffcdd2",
                  command=lambda: self.start_game_ui(3)).pack(pady=10)

    def start_game_ui(self, difficulty):
        """
        Starts the game logic.
        """
        # Initialize the logic
        self.game.start_game("Player", difficulty)
        # Feedback to prove it works
        self.show_game_screen()

    def show_game_screen(self):
        """
        Draws the piles
        Redraws the whole screen every turn
        """

        # Firstly clear the window
        self.clear_window()

        # Display whose turn it is currently.
        status_label = tk.Label(self.root, text=f"Turn: {self.game.current_player}", font=("Arial", 16, "bold"))
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

        # Create input box
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=20)

        tk.Label(input_frame, text="Pile Index: ").pack(side=tk.LEFT)
        self.pile_entry = tk.Entry(input_frame, width=5)
        self.pile_entry.pack(side=tk.LEFT)

        tk.Label(input_frame, text="  Amount: ").pack(side=tk.LEFT)
        self.amount_entry = tk.Entry(input_frame, width=5)
        self.amount_entry.pack(side=tk.LEFT)

        # Confirm button
        tk.Button(self.root, text="Take Coins", command=self.take_coins_handler).pack(pady=10)

    def take_coins_handler(self):
        """
        Read the input, invoke the logic, and refresh the screen
        """
        try:
            # Get user input
            pile_idx = int(self.pile_entry.get())
            amount = int(self.amount_entry.get())

            # Call game logic
            if_success = self.game.take_coins(pile_idx, amount)

            if if_success:
                # 1. Once the player has claimed the item, the interface will refresh immediately to display the new status
                self.show_game_screen()

                # 2. Check if this step by the player leads to the end of the game.
                if self.game.is_game_over():
                    messagebox.showinfo("Game Over", f"Winner is {self.game.current_player}!")
                    self.game_over_screen()
                else:
                    # 3. If it's not over yet, and it's the computer's turn...
                    if self.game.current_player == "Computer":
                        # Execute the computer action after a 1.5-second pause.
                        self.root.after(1500, self.execute_computer)
            else:
                messagebox.showerror("Invalid Move", "Check amount or pile index.")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter numbers only.")

    def execute_computer(self):
        """
        Function that takes over computer actions
        """
        # 1. Computer move
        self.game.computer_move()

        # 2. After the computer finishes, refresh the interface
        self.show_game_screen()

        # 3. check if the game ends
        if self.game.is_game_over():
            messagebox.showinfo("Game Over", f"Winner is {self.game.current_player}!")
            self.game_over_screen()

    def game_over_screen(self):
        """
        Checkout interface
        """
        self.clear_window()
        winner = self.game.current_player
        color = "#4caf50" if winner == "Player" else "#f44336"
        msg = "YOU WIN!" if winner == "Player" else "YOU LOST"

        tk.Label(self.root, text="GAME OVER", font=("Arial", 24, "bold")).pack(pady=40)
        tk.Label(self.root, text=msg, font=("Arial", 36, "bold"), fg=color).pack(pady=20)
        tk.Label(self.root, text=f"Winner: {winner}", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Play Again", font=("Arial", 14), bg="#2196f3", fg="white", width=15,
                  command=self.create_main_menu).pack(pady=40)

    def clear_window(self):
        """
        Function created to clear screen
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        # Start the GUI loop
        self.root.mainloop()