# pathfinding-python

## About

A* path finding algorithm implementation written in python for the [pathfinding into programming](https://reverend-toady.github.io/pathfinding-into-programming/) project

## How To Run

1. Download the repository
2. install necessary libraries

```shell
$ py -m pip install -r requirements.txt
```

3. Traverse to where the repository got downloaded and run the `main.py` file
   
```shell
$ py main.py
```

## How to change the program

1. Open `settings.toml` in your favorite code editor
2. Update the values in the `settings` property
   
   - cell_size: size of each cell
   - row_cells: number of cells in each row
   - col_cells: number of cells in each column

**Note: the size of the screen [width, height] will be (cell_size * row_cells, cell_size * col_cells)**

## How to use the program

Click anywhere on the window the screen grid that opens up when the program is run. 
    
- The first click sets the starting point
- The second click sets the ending point  
- All clicks further on set or remove blockades 

Hit space bar to run the program when satisfied with the board state

## Visualization 

https://user-images.githubusercontent.com/75803854/215267836-690e5bf7-b81b-4d8a-a21f-eb12953eaefc.mp4



