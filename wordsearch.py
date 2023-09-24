import random
import tkinter as tk

class WordSearchGame:
    def __init__(self, root):
        """
        Initialize the WordSearchGame.

        Args:
            root (Tk): The root Tkinter window.
        """
        self.grid_size = 10
        self.grid = [[' ' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.word_list = self.load_word_list('wordlist.txt')  # Load the list of valid words
        self.words_displayed = []  # List to store 10 words displayed at a time
        self.found_words = []
        self.selected_letters = []
        self.current_word = ""

        # Create the main window
        self.root = root
        self.root.title("Word Search Game")

        # Create the canvas for the grid
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Create labels and buttons for the GUI
        self.word_label = tk.Label(self.root, text="Find words: " + ", ".join(self.words_displayed))
        self.word_label.pack()
        self.check_button = tk.Button(self.root, text="Check", command=self.check_words)
        self.check_button.pack()
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_grid)
        self.reset_button.pack()

        # Initialize the game grid and draw it
        self.initialize_grid()
        self.draw_grid()
        self.update_word_display()

    def load_word_list(self, filename):
        """
        Load a list of valid words from a file.

        Args:
            filename (str): The name of the file containing words.

        Returns:
            list: A list of valid words.
        """
        words = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    word = line.strip().upper()  # Convert to uppercase for consistency
                    words.append(word)
        except FileNotFoundError:
            print(f"Error: {filename} not found. Using default word list.")
            words = ["WORD", "SEARCH", "PUZZLE", "PYTHON", "FLASK", "GAME", "DEVELOPMENT", "CHALLENGE", "SOLUTION", "COMPUTER"]

        return words

    def initialize_grid(self):
        """
        Initialize the game grid with random uppercase letters and place words in it.
        """
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.grid[i][j] = random.choice(alphabet)
        self.place_words_in_grid()

    def place_words_in_grid(self):
        """
        Place words randomly in the grid, prioritizing words from the word list.
        """
        for word in self.word_list:
            direction = random.randint(0, 3)
            word_length = len(word)
            valid_positions = []

            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    if direction == 0 and col + word_length <= self.grid_size:
                        valid_positions.append((row, col))
                    elif direction == 1 and row + word_length <= self.grid_size:
                        valid_positions.append((row, col))
                    elif direction == 2 and row + word_length <= self.grid_size and col + word_length <= self.grid_size:
                        valid_positions.append((row, col))
                    elif direction == 3 and row + word_length <= self.grid_size and col - word_length + 1 >= 0:
                        valid_positions.append((row, col))

            if not valid_positions:
                continue

            # Try to place the word from the list if it exists
            if word in self.word_list:
                self.word_list.remove(word)
                row, col = random.choice(valid_positions)
                for letter in word:
                    self.grid[row][col] = letter
                    if direction == 0:
                        col += 1
                    elif direction == 1:
                        row += 1
                    elif direction == 2:
                        row += 1
                        col += 1
                    elif direction == 3:
                        row += 1
                        col -= 1
            else:
                row, col = random.choice(valid_positions)
                for letter in word:
                    self.grid[row][col] = letter
                    if direction == 0:
                        col += 1
                    elif direction == 1:
                        row += 1
                    elif direction == 2:
                        row += 1
                        col += 1
                    elif direction == 3:
                        row += 1
                        col -= 1

    def can_place_word(self, word, row, col, direction):
        """
        Check if a word can be placed at a given position in a specified direction.

        Args:
            word (str): The word to be placed.
            row (int): The starting row position.
            col (int): The starting column position.
            direction (int): The direction (0-3) in which to place the word.

        Returns:
            bool: True if the word can be placed, False otherwise.
        """
        r, c = row, col

        for letter in word:
            if (
                r < 0
                or r >= self.grid_size
                or c < 0
                or c >= self.grid_size
                or (self.grid[r][c] != ' ' and self.grid[r][c] != letter)
            ):
                return False

            if direction == 0:
                c += 1
            elif direction == 1:
                r += 1
            elif direction == 2:
                r += 1
                c += 1
            elif direction == 3:
                r += 1
                c -= 1

        return True

    def draw_grid(self):
        """
        Draw the game grid on the canvas.
        """
        self.canvas.delete("all")
        cell_size = 40
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = col * cell_size
                y = row * cell_size
                letter = self.grid[row][col]
                if (row, col) in self.selected_letters:
                    self.canvas.create_text(x + cell_size / 2, y + cell_size / 2, text=letter, font=("Arial", 16), fill="blue")
                else:
                    self.canvas.create_text(x + cell_size / 2, y + cell_size / 2, text=letter, font=("Arial", 16))

    def on_canvas_click(self, event):
        """
        Handle mouse clicks on the canvas.

        Args:
            event (Event): The mouse click event.
        """
        col = event.x // 40
        row = event.y // 40
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            self.selected_letters.append((row, col))
            self.current_word += self.grid[row][col]
            self.draw_grid()

    def check_words(self):
        """
        Check if the current word is in the list of words.
        """
        if self.current_word in self.word_list and self.current_word not in self.found_words:
            self.found_words.append(self.current_word)
            self.word_list.remove(self.current_word)
            self.update_word_display()
            self.current_word = ""
            self.selected_letters = []
            self.draw_grid()
            if not self.word_list:
                self.word_label.config(text="Congratulations! You found all words.")
        else:
            self.current_word = ""
            self.selected_letters = []
            self.draw_grid()

    def reset_grid(self):
        """
        Reset the game grid and word list with new random words.
        """
        # Clear all data and reinitialize the grid and word list
        self.grid = [[' ' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.word_list = self.load_word_list('wordlist.txt')  # Generate 10 new random words
        random.shuffle(self.word_list)  # Shuffle the words for variety
        self.found_words = []
        self.selected_letters = []
        self.current_word = ""
        self.initialize_grid()
        self.draw_grid()
        self.update_word_display()

    def update_word_display(self):
        """
        Update the displayed word list with the next 10 words.
        """
        self.words_displayed = self.word_list[:10]
        self.word_label.config(text="Find words: " + ", ".join(self.words_displayed))

if __name__ == "__main__":
    root = tk.Tk()
    app = WordSearchGame(root)
    root.mainloop()



