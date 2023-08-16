import os
from enum import IntEnum
from findirection.envs.maze import Maze
import numpy as np
from typing import Union


class Puddle(IntEnum):
    Dry, Small, Large = range(3)   


class GridBase():
    maze = None                 
    puddles = None             
    base_areas = []            
    grid_areas = []            

    debug_maze = False         
    grid_rewards = []          

  
    def __init__( self, working_directory: str = ".", **kwargs: dict ):
        self.working_directory = working_directory
        self.drawmode = kwargs.get('drawmode', 'colab' if 'COLAB_GPU' in os.environ else "" )

        self.width = 6 
        self.height = 6     
    
        self.start = kwargs.get('start',[0,0])       
        self.end = kwargs.get('end',[self.width-1,self.height-1])    
        self.puddles = kwargs.get('puddles',None)     
        puddle_props = kwargs.get('puddle_props',{})
        self.large_puddle_reward = puddle_props.get('large_reward',-4)
        self.small_puddle_reward = puddle_props.get('small_reward',-2)
        self.large_puddle_probability = puddle_props.get('large_prob',0.4)
        self.small_puddle_probability = puddle_props.get('small_prob',0.6)    

        self.base_areas = kwargs.get('base_areas',[])     
        self.grid_areas = kwargs.get('grid_areas',[])       
        
        self.add_maze = kwargs.get('add_maze',False)
        self.maze_seed = kwargs.get('maze_seed',0)
        self.make_maze()
        self.toggle_walls( kwargs.get('walls',[]) )

        self.grid_rewards = self.get_reward()


    def make_maze(self):
        if self.add_maze:
            if self.maze is None:
                self.maze = Maze(self.width, self.height, self.start[0], self.start[1], seed = self.maze_seed)
                self.maze.make_maze()        
            if self.debug_maze: 
                self.maze.write_svg(os.path.join(self.working_directory, "maze.svg"))


    def toggle_walls(self, walls):
        if self.maze is None:
            self.maze = Maze(self.width, self.height, self.start[0], self.start[1], no_walls = True)
            self.add_maze = True 

        for (loc), direction in walls:
            x = loc[0]
            y = loc[1]
            num_cells = loc[2] if len(loc) == 3 else 1
            
            for n in range(num_cells):
                if x >= self.width or y >= self.height:
                    break         

                current_cell = self.maze.cell_at(x,y)
                if   direction == 'E': next_cell = self.maze.cell_at(x+1,y)
                elif direction == 'W': next_cell = self.maze.cell_at(x-1,y)
                elif direction == 'N': next_cell = self.maze.cell_at(x,y-1)
                elif direction == 'S': next_cell = self.maze.cell_at(x,y+1)

                current_cell.toggle_wall(next_cell, direction)           

                if direction == 'E' or direction == 'W': y += 1
                else: x += 1                  


    def get_puddle_size( self, x, y ):
        if self.puddles is not None:
            if isinstance(self.puddles[0],list):
                return Puddle(self.puddles[y][x])
            else:
                for (px,py),puddle_size in self.puddles:
                    if x==px and y==py:         
                        return Puddle(puddle_size) 
        return Puddle.Dry    


    def get_transition_probability( self, x, y ):
        puddle_size = self.get_puddle_size( x, y )         
        
        if puddle_size == Puddle.Large: return self.large_puddle_probability
        if puddle_size == Puddle.Small: return self.small_puddle_probability
    
        return 1.     


    def get_reward( self, x: int = None, y: int = None ) -> Union[int,np.ndarray]:
        if (x is None) or (y is None):
            return self.get_reward_array()
        else:
            return self.get_reward_value(x,y)


    def get_reward_array(self) -> np.ndarray:
        if len(self.grid_rewards) == 0:       
            height = self.height
            width = self.width
            reward_arr = np.zeros((height,width)).astype(int)
            for y in range(height):
                for x in range(width):
                    reward_arr[y][x] = self.get_reward_value(x,y) 
            return reward_arr      

        return self.grid_rewards


    def test_for_base_area( self, x, y ):
        for area in self.base_areas: 
            if type(area[0]).__name__ == 'int':
                ax,ay,aw,ah = self.get_area_defn(area)
            else:
                ax,ay,aw,ah = self.get_area_defn(area[0])      
            return self.in_area(x,y,ax,ay,aw,ah)
        

    def get_reward_value( self, x, y ):
   
        if len(self.grid_rewards) > 0: 
            return self.grid_rewards[y,x]

        puddle_size = self.get_puddle_size( x, y )
        if   puddle_size == Puddle.Large: return self.large_puddle_reward
        elif puddle_size == Puddle.Small: return self.small_puddle_reward  

        if self.test_for_base_area(x,y):      
            return 0

        cell_reward = -1
        for area in self.grid_areas:      
            if len(area) > 2:   
                try:     
                    ax,ay,aw,ah = self.get_area_defn(area[0]) 
                    if self.in_area( x,y,ax,ay,aw,ah ):
                        cell_reward = area[2]        
                except:
                      pass
        return cell_reward    


    def get_area_defn( self, area):
        x,y,*args = area
        wd,ht = args if args else (1,1) 
        return x,y,wd,ht


    def in_area(self,x,y,ax,ay,aw,ah):
        if (x >= ax and x < (ax + aw)) and ((y >= ay and y < (ay + ah))):
            return True
        return False 