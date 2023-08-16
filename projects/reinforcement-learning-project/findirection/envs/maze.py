import random

class Cell:
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y, no_walls = False):
        self.x, self.y = x, y
        if no_walls:
            self.walls = {'N': False, 'S': False, 'E': False, 'W': False }
        else:
            self.walls = {'N': True, 'S': True, 'E': True, 'W': True}

    def has_all_walls(self):
        return all(self.walls.values())

    def knock_down_wall(self, other, wall):
        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False

    def add_wall(self, other, wall):
        self.walls[wall] = True
        other.walls[Cell.wall_pairs[wall]] = True  

    def toggle_wall(self, other, wall):
        if self.walls[wall]:
            self.knock_down_wall(other,wall)
        else:
            self.add_wall(other,wall)    


class Maze:
    def __init__(self, nx, ny, ix=0, iy=0, seed = None, no_walls = False):
        if seed is not None: random.seed(seed) 
        
        self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        self.maze_map = [[Cell(x, y, no_walls) for y in range(ny)] for x in range(nx)]

        if no_walls:
            self.add_boundary_walls()

    def add_boundary_walls(self):
        for y in range(self.ny):
            for x in range(self.nx):
                if y == 0:
                    self.cell_at(x, y).walls['N'] = True
                elif (y+1) == self.ny:
                    self.cell_at(x, y).walls['S'] = True

                if x == 0:
                    self.cell_at(x, y).walls['W'] = True
                elif (x+1) == self.nx:
                    self.cell_at(x, y).walls['E'] = True              

    def cell_at(self, x, y):
        return self.maze_map[x][y]
    
    def dimensions(self):
        return self.nx, self.ny

    def __str__(self):
        maze_rows = ['-' * self.nx * 2]
        for y in range(self.ny):
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['E']:
                    maze_row.append(' |')
                else:
                    maze_row.append('  ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['S']:
                    maze_row.append('-+')
                else:
                    maze_row.append(' +')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows)

    def write_svg(self, filename):
        aspect_ratio = self.nx / self.ny
        padding = 10
        height = 500
        width = int(height * aspect_ratio)
        scy, scx = height / self.ny, width / self.nx


    def find_valid_neighbours(self, cell):
        delta = [('W', (-1, 0)),
                 ('E', (1, 0)),
                 ('S', (0, 1)),
                 ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours

    def make_maze(self):
        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.cell_at(self.ix, self.iy)
        nv = 1
        
        while nv < n:
            neighbours = self.find_valid_neighbours(current_cell)

            if not neighbours:
                current_cell = cell_stack.pop()
                continue

            direction, next_cell = random.choice(neighbours)
            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            nv += 1
            
    def write_to_canvas(self, canvas, maze_height, maze_padding, color='#000', wall_width=4 ): 

        aspect_ratio = self.nx / self.ny
        padding = maze_padding
        
        height = maze_height
        width = int(height * aspect_ratio)
        
        scy, scx = height / self.ny, width / self.nx

        canvas.line_width = wall_width
        canvas.line_cap = 'square'    
        
        canvas.stroke_style = color       
        canvas.set_line_dash([0,0])        
