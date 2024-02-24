import tkinter as tk
from tkinter import Label, Entry, Button, Canvas, messagebox, IntVar
import sys
import time
from genetic_algorithm import genetic_algorithm

sys.setrecursionlimit(10**6)

class KnightTourApp:
    def __init__(self, master):
        # Initialize the GUI components
        self.master = master
        master.title("Knight's Tour Solver")

        # Labels and entry widgets for user input
        self.label_size = Label(master, text="Enter Chessboard Size:")
        self.label_size.pack()

        self.entry_size = Entry(master)
        self.entry_size.pack()

        self.label_start_row = Label(master, text="Enter Starting Row:")
        self.label_start_row.pack()

        self.entry_start_row = Entry(master)
        self.entry_start_row.pack()

        self.label_start_col = Label(master, text="Enter Starting Column:")
        self.label_start_col.pack()

        self.entry_start_col = Entry(master)
        self.entry_start_col.pack()

        # Genetic algorithm parameters input
        self.label_population_size = Label(master, text="Enter Population Size (Genetic Algorithm):")
        self.label_population_size.pack()

        self.entry_population_size = Entry(master)
        self.entry_population_size.pack()

        self.label_generations = Label(master, text="Enter Number of Generations (Genetic Algorithm):")
        self.label_generations.pack()

        self.entry_generations = Entry(master)
        self.entry_generations.pack()

        self.label_mutation_rate = Label(master, text="Enter Mutation Rate (Genetic Algorithm):")
        self.label_mutation_rate.pack()

        self.entry_mutation_rate = Entry(master)
        self.entry_mutation_rate.pack()

        # Radio buttons for algorithm choice
        self.algorithm_choice = IntVar()
        self.algorithm_choice.set(1)
        self.backtracking_radio = tk.Radiobutton(master, text="Backtracking", variable=self.algorithm_choice, value=1)
        self.backtracking_radio.pack()

        self.genetic_radio = tk.Radiobutton(master, text="Genetic Algorithm", variable=self.algorithm_choice, value=2)
        self.genetic_radio.pack()

        # Button to initiate solving
        self.solve_button = Button(master, text="Solve", command=self.solve_knights_tour)
        self.solve_button.pack()

        # Canvas for displaying the chessboard
        self.canvas_size = 400
        self.canvas = Canvas(master, width=self.canvas_size, height=self.canvas_size + 50)
        self.canvas.pack()

        # List to store the order of visited cells
        self.visited_order = []

    def display_solution(self, solution, n):
        # Display the solution on the canvas with animations
        cell_size = self.canvas_size // n
        self.canvas.delete("all")

        # Sort visited cells based on the order of visit
        self.visited_order.sort(key=lambda x: x[2])

        for visit_info in self.visited_order:
            row, col, move_number = visit_info
            x1, y1, x2, y2 = col * cell_size, row * cell_size, (col + 1) * cell_size, (row + 1) * cell_size
            color = "lightgreen" if (row + col) % 2 == 0 else "lightblue"
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
            text_x, text_y = (x1 + x2) / 2, (y1 + y2) / 2
            font_size = int(cell_size / 3)
            self.canvas.create_text(text_x, text_y, text=str(move_number), fill="black", font=("Arial", font_size, "bold"))
            self.master.update()
            time.sleep(0.2)

        for i, row in enumerate(solution):
            for j, move_number in enumerate(row):
                x1, y1, x2, y2 = j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size
                color = "lightgreen" if (i + j) % 2 == 0 else "lightblue"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                text_x, text_y = (x1 + x2) / 2, (y1 + y2) / 2
                font_size = int(cell_size / 3)
                self.canvas.create_text(text_x, text_y, text=str(move_number), fill="black",
                                        font=("Arial", font_size, "bold"))
                self.master.update()
                time.sleep(0.05)

    def solve_knights_tour(self):
        # Solve the Knight's Tour problem based on user input
        self.visited_order = []
        board_size = self.entry_size.get()

        if not board_size.isdigit() or int(board_size) <= 0:
            messagebox.showinfo("Invalid Input", "Please enter a positive integer for the chessboard size.")
            return

        board_size = int(board_size)

        if board_size > 64:
            messagebox.showinfo("Warning", "Board size greater than 64 may take a very long time to compute.")

        start_row, start_col = self.entry_start_row.get(), self.entry_start_col.get()

        if not start_row.isdigit() or not start_col.isdigit() or \
                not (0 <= int(start_row) < board_size) or not (0 <= int(start_col) < board_size):
            messagebox.showinfo("Invalid Input", "Please enter valid positive integers for the starting row and column.")
            return

        start_row, start_col = int(start_row), int(start_col)

        if self.algorithm_choice.get() == 2:
            try:
                population_size = int(self.entry_population_size.get() or 100)
                generations = int(self.entry_generations.get() or 1000)
                mutation_rate = float(self.entry_mutation_rate.get() or 0.01)
            except ValueError:
                messagebox.showinfo("Invalid Input", "Please enter valid numbers for genetic algorithm parameters.")
                return

            solution_board, best_solution, best_fitness = genetic_algorithm(board_size, population_size=population_size,
                                                                            generations=generations, mutation_rate=mutation_rate)
        else:
            solution_board = self.solve_l_shaped_knights_tour(board_size, start_row, start_col)

        if solution_board:
            self.display_solution(solution_board, board_size)
            if self.algorithm_choice.get() == 2:
                print("Best Solution:", best_solution)
                print("Best Fitness:", best_fitness)
        else:
            messagebox.showinfo("No Solution", "No solution found for the given chessboard size and starting block.")

    def solve_l_shaped_knights_tour(self, n, start_row, start_col):
        # Solve the Knight's Tour problem using backtracking
        board = [[-1 for _ in range(n)] for _ in range(n)]
        move_number = 1
        board[start_row][start_col] = move_number

        move_x = [2, 1, -1, -2, -2, -1, 1, 2]
        move_y = [1, 2, 2, 1, -1, -2, -2, -1]

        def is_valid_move(row, col):
            return 0 <= row < n and 0 <= col < n and board[row][col] == -1

        def count_available_moves(row, col):
            count = 0
            for i in range(8):
                new_row, new_col = row + move_x[i], col + move_y[i]
                if is_valid_move(new_row, new_col):
                    count += 1
            return count

        def next_moves_sorting_order(row, col):
            next_moves = []
            for i in range(8):
                new_row, new_col = row + move_x[i], col + move_y[i]
                if is_valid_move(new_row, new_col):
                    next_moves.append((new_row, new_col, count_available_moves(new_row, new_col)))
            next_moves.sort(key=lambda x: x[2])
            return next_moves

        def solve_tour(row, col, move_number):
            if move_number == n * n:
                return True

            next_moves = next_moves_sorting_order(row, col)

            for move in next_moves:
                new_row, new_col, _ = move
                board[new_row][new_col] = move_number + 1
                self.visited_order.append((new_row, new_col, move_number + 1))

                if solve_tour(new_row, new_col, move_number + 1):
                    return True

                board[new_row][new_col] = -1

            return False

        self.visited_order.append((start_row, start_col, move_number))

        if not solve_tour(start_row, start_col, move_number):
            return []

        return board

    def update_progress(self, generation, best_fitness):
        # Update the GUI with the current state of the genetic algorithm
        self.master.update()
        self.master.title(f"Knight's Tour Solver - Generation: {generation}, Best Fitness: {best_fitness}")

# Main entry point of the program
if __name__ == "__main__":
    root = tk.Tk()
    app = KnightTourApp(root)
    root.mainloop()
