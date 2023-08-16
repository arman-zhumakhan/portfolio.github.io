
import numpy as np
from typing import Union


from ipycanvas import hold_canvas
from findirection.envs.arrows import Arrows
from findirection.envs.directions import Direction

from findirection.envs.grid_base import GridBase


class GridInfo():
  
    def __init__(self, gridbase: GridBase, **kwargs: dict):
        self.grid = gridbase

    def get_cell_directions(self, x: int, y: int, direction: Direction = None) -> list:
        grid = self.grid

        if (x == grid.end[0]) and (y == grid.end[1]):
            return {}
    
        for area in grid.base_areas: 
            if type(area[0]).__name__ == 'int':
                ax,ay,aw,ah = grid.get_area_defn(area)
            else:
                ax,ay,aw,ah = grid.get_area_defn(area[0])      

            if grid.in_area(x,y,ax,ay,aw,ah):
                return {}

        if grid.maze is not None:        
            cell = grid.maze.cell_at( x, y )  
      
            actions = {k: not v for k, v in cell.walls.items()}      
        else:
            actions = {'N':True,'E':True,'S':True,'W':True}
            
            if x == 0: del actions['W']
            if x == grid.width-1: del actions['E']
            if y == 0: del actions['N']
            if y == grid.height-1: del actions['S']   

        for area in grid.base_areas: 
            if type(area[0]).__name__ == 'int':
                ax,ay,aw,ah = grid.get_area_defn(area)
            else:
                ax,ay,aw,ah = grid.get_area_defn(area[0])      

            if grid.in_area(x+1,y,ax,ay,aw,ah): del actions['E']
            if grid.in_area(x-1,y,ax,ay,aw,ah): del actions['W']
            if grid.in_area(x,y-1,ax,ay,aw,ah): del actions['N']
            if grid.in_area(x,y+1,ax,ay,aw,ah): del actions['S']
    

        if direction is not None:
            dir_value = direction
            for dir,v in actions.items():        
                if v == True:
                    if (dir == 'N') and not (dir_value & Direction.North): actions['N'] = False
                    if (dir == 'S') and not (dir_value & Direction.South): actions['S'] = False
                    if (dir == 'E') and not (dir_value & Direction.East):  actions['E'] = False
                    if (dir == 'W') and not (dir_value & Direction.West):  actions['W'] = False                     
      
        return actions


    def get_directions( self, x: int = None, y: int = None ) -> Union[Direction,np.ndarray]:
        if (x is None) or (y is None):
            return self.get_direction_array()
        else:
            return self.get_direction_value(x,y)


    def get_direction_value( self, x: int, y: int ) -> Direction:
        return Direction.get_value( self.get_cell_directions( x, y ) )   


    def get_direction_array(self) -> np.ndarray:
        height = self.grid.height
        width = self.grid.width
        direction_arr = np.zeros((height,width)).astype(int)
        for y in range(height):
            for x in range(width):
                direction_arr[y][x] = self.get_direction_value(x,y) 
        return direction_arr       