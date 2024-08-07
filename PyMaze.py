import tkinter as tk
from tkinter import messagebox
import random
#Maze Boundry
class Cell:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.visited = False
        self.entry_exit = None

    def draw(self, canvas, offset_x, offset_y):
        x1, y1 = self.x * self.size + offset_x, self.y * self.size + offset_y
        x2, y2 = x1 + self.size, y1 + self.size

        if self.walls['N']:
            canvas.create_line(x1, y1, x2, y1)
        if self.walls['S']:
            canvas.create_line(x1, y2, x2, y2)
        if self.walls['E']:
            canvas.create_line(x2, y1, x2, y2)
        if self.walls['W']:
            canvas.create_line(x1, y1, x1, y2)

        if self.entry_exit == "entry":
            canvas.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1, fill="green")
        elif self.entry_exit == "exit":
            canvas.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1, fill="red")
#Maze Genreator
class Maze:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [[Cell(x, y, cell_size) for y in range(height)] for x in range(width)]
        self.current_cell = (0, 0)
        self.stack = [(0, 0)]
        self.visited_cells = 1
        self.entry_coor = None
        self.exit_coor = None

    def draw(self, canvas):
        canvas.delete("all")
        
        maze_width = self.width * self.cell_size
        maze_height = self.height * self.cell_size
        offset_x = (canvas.winfo_width() - maze_width) // 2
        offset_y = (canvas.winfo_height() - maze_height) // 2

        for row in self.grid:
            for cell in row:
                cell.draw(canvas, offset_x, offset_y)

        if self.entry_coor:
            entry_x, entry_y = self.entry_coor
            canvas.create_text(offset_x - 20, entry_y * self.cell_size + offset_y + self.cell_size // 2,
                               text="Entry", fill="black", anchor=tk.E)

        if self.exit_coor:
            exit_x, exit_y = self.exit_coor
            canvas.create_text(offset_x + maze_width + 20, exit_y * self.cell_size + offset_y + self.cell_size // 2,
                               text="Exit", fill="black", anchor=tk.W)

    def generate(self):
        while self.visited_cells < self.width * self.height:
            neighbours = self.get_neighbours(self.current_cell[0], self.current_cell[1])
            unvisited_neighbours = [neighbour for neighbour in neighbours if not self.grid[neighbour[0]][neighbour[1]].visited]

            if unvisited_neighbours:
                next_cell = random.choice(unvisited_neighbours)
                self.remove_walls(self.current_cell, next_cell)
                self.grid[next_cell[0]][next_cell[1]].visited = True
                self.stack.append(self.current_cell)
                self.current_cell = next_cell
                self.visited_cells += 1
            elif self.stack:
                self.current_cell = self.stack.pop()

        self.entry_coor = (0, random.randint(0, self.height - 1))
        self.grid[self.entry_coor[0]][self.entry_coor[1]].entry_exit = "entry"

        self.exit_coor = (self.width - 1, random.randint(0, self.height - 1))
        self.grid[self.exit_coor[0]][self.exit_coor[1]].entry_exit = "exit"

    def get_neighbours(self, x, y):
        neighbours = []
        if x > 0:
            neighbours.append((x - 1, y))
        if x < self.width - 1:
            neighbours.append((x + 1, y))
        if y > 0:
            neighbours.append((x, y - 1))
        if y < self.height - 1:
            neighbours.append((x, y + 1))
        return neighbours

    def remove_walls(self, current_cell, next_cell):
        cx, cy = current_cell
        nx, ny = next_cell
        if cx - nx == 1:
            self.grid[cx][cy].walls['W'] = False
            self.grid[nx][ny].walls['E'] = False
        elif cx - nx == -1:
            self.grid[cx][cy].walls['E'] = False
            self.grid[nx][ny].walls['W'] = False
        elif cy - ny == 1:
            self.grid[cx][cy].walls['N'] = False
            self.grid[nx][ny].walls['S'] = False
        elif cy - ny == -1:
            self.grid[cx][cy].walls['S'] = False
            self.grid[nx][ny].walls['N'] = False
# Maze Solver
def solve_maze(maze, start, end):
    stack = [start]
    visited = set()
    parent = {start: None}
    backtracking_paths = []

    def get_neighbors(pos):
        neighbors = []
        x, y = pos
        if x > 0 and not maze.grid[x - 1][y].walls['E']:
            neighbors.append((x - 1, y))
        if x < len(maze.grid) - 1 and not maze.grid[x][y].walls['E']:
            neighbors.append((x + 1, y))
        if y > 0 and not maze.grid[x][y - 1].walls['S']:
            neighbors.append((x, y - 1))
        if y < len(maze.grid[0]) - 1 and not maze.grid[x][y].walls['S']:
            neighbors.append((x, y + 1))
        return neighbors

    while stack:
        current = stack.pop()
        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path_with_intermediates = []
            for i in range(len(path) - 1):
                path_with_intermediates.append(path[i])
                cx, cy = path[i]
                nx, ny = path[i + 1]
                dx, dy = nx - cx, ny - cy
                if dx == 1:
                    path_with_intermediates.extend([(cx + 1, cy)])
                elif dx == -1:
                    path_with_intermediates.extend([(cx - 1, cy)])
                elif dy == 1:
                    path_with_intermediates.extend([(cx, cy + 1)])
                elif dy == -1:
                    path_with_intermediates.extend([(cx, cy - 1)])
            path_with_intermediates.append(end)
            return path[::-1], path_with_intermediates, backtracking_paths

        visited.add(current)
        found = False
        for neighbor in get_neighbors(current):
            if neighbor not in visited and neighbor not in stack:
                stack.append(neighbor)
                parent[neighbor] = current
                found = True
        if not found:
            backtracking_paths.append(current)

    return None, [], backtracking_paths  # No path found
#tkinter generator
class MazeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Generator")

        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()

        self.width_label = tk.Label(root, text="Width:")
        self.width_label.pack(side=tk.LEFT)
        self.width_entry = tk.Entry(root, width=5)
        self.width_entry.pack(side=tk.LEFT)
        self.width_entry.insert(0, "20")

        self.height_label = tk.Label(root, text="Height:")
        self.height_label.pack(side=tk.LEFT)
        self.height_entry = tk.Entry(root, width=5)
        self.height_entry.pack(side=tk.LEFT)
        self.height_entry.insert(0, "20")

        self.generate_button = tk.Button(root, text="Generate Maze", command=self.generate_maze)
        self.generate_button.pack(side=tk.LEFT, padx=10)

        self.solve_button = tk.Button(root, text="Solve Maze", command=self.solve_maze)
        self.solve_button.pack(side=tk.LEFT, padx=10)

        self.maze = None

    def generate_maze(self):
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            if width < 5 or height < 5:
                messagebox.showwarning("Warning", "Width and Height must be at least 5")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid dimensions")
            return

        cell_size = 20
        self.maze = Maze(width, height, cell_size)
        self.maze.generate()
        self.maze.draw(self.canvas)

    def solve_maze(self):
        if not self.maze:
            messagebox.showwarning("Warning", "Please generate a maze first")
            return

        start = self.maze.entry_coor
        end = self.maze.exit_coor
        path, path_with_intermediates, backtracking_paths = solve_maze(self.maze, start, end)

        maze_width = self.maze.width * self.maze.cell_size
        maze_height = self.maze.height * self.maze.cell_size
        offset_x = (self.canvas.winfo_width() - maze_width) // 2
        offset_y = (self.canvas.winfo_height() - maze_height) // 2

        # Draw backtracking paths
        for x, y in backtracking_paths:
            if (x, y) != start and (x, y) != end:
                x1, y1 = x * self.maze.cell_size + offset_x, y * self.maze.cell_size + offset_y
                x2, y2 = x1 + self.maze.cell_size, y1 + self.maze.cell_size
                self.canvas.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1, fill="pink", outline="")

        # Draw path with arrows
        for i in range(len(path_with_intermediates) - 1):
            x1, y1 = path_with_intermediates[i]
            x2, y2 = path_with_intermediates[i + 1]
            if (x1, y1) != start and (x1, y1) != end and (x2, y2) != start and (x2, y2) != end:
                x1_pix = x1 * self.maze.cell_size + offset_x + self.maze.cell_size // 2
                y1_pix = y1 * self.maze.cell_size + offset_y + self.maze.cell_size // 2
                x2_pix = x2 * self.maze.cell_size + offset_x + self.maze.cell_size // 2
                y2_pix = y2 * self.maze.cell_size + offset_y + self.maze.cell_size // 2
                self.canvas.create_line(x1_pix, y1_pix, x2_pix, y2_pix, arrow=tk.LAST, fill="green")

        # Draw start and end points
        for x, y in [start, end]:
            x1, y1 = x * self.maze.cell_size + offset_x, y * self.maze.cell_size + offset_y
            x2, y2 = x1 + self.maze.cell_size, y1 + self.maze.cell_size
            self.canvas.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1, fill="yellow", outline="")


if __name__ == "__main__":
    root = tk.Tk()
    app = MazeGeneratorApp(root)
    root.mainloop()
