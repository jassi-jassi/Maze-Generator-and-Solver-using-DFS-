# Maze-Generator-and-Solver-using-DFS-

This project is a Python-based maze generator and solver with a graphical user interface (GUI) built using tkinter. The maze is generated using the Depth-First Search (DFS) algorithm, and the solver also employs DFS to find a path from the entry to the exit.

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Approach](#approach)
- [Data Structures](#data-structures)
- [Depth-First Search (DFS)](#depth-first-search-dfs)


## Description
The Maze Generator and Solver project provides a fun and interactive way to generate and solve mazes using Python. The application uses a tkinter-based GUI to allow users to specify the dimensions of the maze and visualize the generation and solving process in real-time. The mazes are generated randomly each time, ensuring a unique experience with each use. This project is an excellent example of using DFS for both generating complex structures and finding solutions in a systematic manner.

## Features
- Random maze generation using DFS
- Maze solving using DFS
- Graphical interface to interact with the maze
- Customizable maze dimensions

## Usage
1. Run the main script:
    ```sh
    python maze_generator.py
    ```
2. Use the GUI to input the desired maze width and height.
3. Click "Generate Maze" to create a new maze.
4. Click "Solve Maze" to find and display the solution path.

## How It Works
The project consists of several classes and functions that handle maze generation, drawing, and solving. The main components are the `Cell`, `Maze`, `MazeGeneratorApp`, and `DepthFirstSolver` classes.

### Approach
#### Maze Generation
The maze is generated using the Depth-First Search (DFS) algorithm with backtracking. Starting from a random cell, the algorithm visits neighboring cells recursively, removing walls to create passages until all cells are visited.

#### Maze Solving
The solver uses the DFS algorithm to find a path from the entry to the exit of the maze. It explores each path fully before backtracking and trying a different path.

### Data Structures
1. **Cell**: Represents each cell in the maze with attributes for walls, visited state, and entry/exit status.
2. **Maze**: A grid of `Cell` objects that handles the generation and drawing of the maze.
3. **Stack**: Used in the DFS algorithm for backtracking during maze generation and solving.

### Depth-First Search (DFS)
DFS is a graph traversal algorithm that explores as far as possible along each branch before backtracking. It uses a stack data structure to remember the path and backtrack when necessary.


---

This README provides a detailed overview of the project, explaining the main components, their roles, and how the DFS algorithm is used for both generating and solving the maze.
