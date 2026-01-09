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
        """
        Creates the title page with 3 difficulty buttons.
        """
        # 1. Clear any existing widgets (useful when restarting)
        #for widget in self.root.winfo_children():
            #widget.destroy()

        # 2. Title Label
        title_label = tk.Label(self.root, text="Welcome to Nim Game", font=("Arial", 24, "bold"))
        title_label.pack(pady=40)  # Add vertical padding

        # 3. Subtitle
        subtitle = tk.Label(self.root, text="Select Difficulty (Number of Piles):", font=("Arial", 14))
        subtitle.pack(pady=10)

        # 4. Difficulty Buttons
        # We use 'lambda' to pass arguments to the function when clicked
        btn_easy = tk.Button(self.root, text="1 Pile (Easy)", font=("Arial", 12), width=20,
                             command=lambda: self.start_game_ui(1))
        btn_easy.pack(pady=5)

        btn_medium = tk.Button(self.root, text="2 Piles (Medium)", font=("Arial", 12), width=20,
                               command=lambda: self.start_game_ui(2))
        btn_medium.pack(pady=5)

        btn_hard = tk.Button(self.root, text="3 Piles (Hard)", font=("Arial", 12), width=20,
                             command=lambda: self.start_game_ui(3))
        btn_hard.pack(pady=5)

    def start_game_ui(self, difficulty):
        """
        Handler for button clicks. Starts the game logic.
        """
        # Initialize the logic
        self.game.start_game("Player", difficulty)

        # Temporary feedback to prove it works (Console log)
        print(f"GUI: Game started with {difficulty} piles.")
        messagebox.showinfo("Game Started", f"You selected {difficulty} piles!\nGame logic initialized.")

    def run(self):
        """Start the GUI loop."""
        self.root.mainloop()