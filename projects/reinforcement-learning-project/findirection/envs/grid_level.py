import numpy as np
import os 
from typing import Union

from findirection.envs.directions import Direction
from findirection.envs.grid_base import GridBase
from findirection.envs.grid_info import GridInfo
from findirection.envs.draw_grid import DrawGrid
from findirection.envs.draw_info import DrawInfo


class GridLevel():
    def __init__( self, **kwargs: dict ):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        self.grid_base = GridBase( dir_path, **kwargs )
        self.grid_info = GridInfo( self.grid_base, **kwargs )
        self.draw_grid = DrawGrid( self.grid_base, **kwargs )    
        self.draw_info = DrawInfo( self.draw_grid, self.grid_info, **kwargs )


 
    def get_directions( self, x: int = None, y: int = None ) -> Union[Direction,np.ndarray]:
        return self.grid_info.get_directions( x, y )


    def get_rewards( self, x: int = None, y: int = None ) -> Union[Direction,np.ndarray]:
        return self.grid_base.get_reward( x, y )


    def get_next_state( self, x, y, direction ):
        assert direction >= Direction.Stay and direction <= Direction.West    
        
        possible_actions = self.grid_info.get_cell_directions(x,y,direction)
        if not possible_actions: 
            return [x,y],-1,(direction==Direction.Stay) 

        chosen_action = [key for (key, value) in possible_actions.items() if value]
        if len(chosen_action) != 1:
            return [x,y],-1,False

        all_actions = self.grid_info.get_cell_directions(x,y)     
        all_actions.pop(chosen_action[0], None)
        other_states = [key for (key, value) in all_actions.items() if value]

        transition_probability = self.grid_base.get_transition_probability( x, y )

        target_state_reached = True
        if (np.random.random() < transition_probability) or (len(other_states) == 0):
            direction = chosen_action[0]
        else:
            direction = np.random.choice(other_states)

            target_state_reached = False

        next_pos = self.get_next_state_position( x, y, direction )   

        reward = self.grid_base.get_reward( next_pos[0], next_pos[1] )

        return next_pos, reward, target_state_reached  


    def get_next_state_position( self, x, y, direction ):
        next_pos = []    
        if direction == 'N': next_pos = [x,y-1]
        if direction == 'S': next_pos = [x,y+1]
        if direction == 'E': next_pos = [x+1,y]
        if direction == 'W': next_pos = [x-1,y] 
        return next_pos


    def get_reward( self, x, y, direction = None ):
        if direction:

            if type(direction) != str:
                direction = Direction.get_direction_char(direction)

            nx,ny = self.get_next_state_position( x, y, direction )
            return self.grid_base.get_reward(nx,ny),[nx,ny]

        return self.grid_base.get_reward(x,y)    
    

    def draw( self ):
        return self.draw_grid.canvases

    def clear( self, all_info=False ):
        self.draw_grid.clear(all_info)

    def show_info( self, info: dict ):
        self.draw_info.draw( info )

    def save( self, filename ): 
        canvases = self.get_canvases()
        canvases[3].save()
        canvases[3].restore()
        return canvases.to_file(filename)    

    def get_canvases(self):
        return self.draw_grid.canvases

    def get_canvas_dimensions( self ):
        return [self.draw_grid.total_width, self.draw_grid.total_height]
        