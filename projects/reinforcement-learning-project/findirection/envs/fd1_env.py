import numpy as np
from gym.spaces import Discrete, MultiDiscrete
from findirection.envs.fd0_env import FindDirection_v0
from findirection.envs.directions import Direction
from findirection.envs.actions import Actions
from findirection.envs.grid_level import GridLevel
from findirection.envs.robot_draw import RobotDraw

class FindDirection_v1(FindDirection_v0):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reset() 

   
    def get_available_actions( self ):     

        direction_value = self.level.get_directions(self.x,self.y) 

        action_list = []       
        if direction_value & Direction.North: action_list.append( Actions.North )
        if direction_value & Direction.South: action_list.append( Actions.South )
        if direction_value & Direction.East:  action_list.append( Actions.East ) 
        if direction_value & Direction.West:  action_list.append( Actions.West )
        return action_list     

    def get_available_actions( self, x = None, y = None ):

        if x is None: x = self.x
        if y is None: y = self.y

        direction_value = self.level.get_directions(x,y) 

        return Direction.get_action_list(direction_value) 
    
            
    def set_available_actions( self ):
        action_list = self.get_available_actions()   


    def take_action(self, action):

        super().take_action( action )   
        
        self.set_available_actions() 
        
        direction = Direction.from_action(action) 
        
        next_pos,reward,target_reached = self.level.get_next_state( self.x, self.y, direction )  
        
        self.x = next_pos[0]
        self.y = next_pos[1]
      
        self.set_available_actions()      

        return reward, target_reached  
      
      
    def reset(self):
        result = super().reset()
        self.set_available_actions()
        return result      
    
    def step(self, action): 
        reward, target_reached = self.take_action(action)      
        obs = np.array([self.x,self.y])      
        done = (self.x == self.end[0]) and (self.y == self.end[1])
        
        info = {'target_reached':target_reached}
        return obs, reward, done, info    
    
    def render(self, mode='human', info = None):     
        self.robot.move(self.x,self.y)    
        self.level.show_info(info) 
        return self.level.draw() 
    
    def show_info(self,info):
        self.level.show_info( info )

    def clear_info(self,all_info=False):
        self.level.clear(all_info)   
    
    def save(self, filename):
        self.level.save(filename) 
   
    def get_transition_probability( self, x = None, y = None ):
        if not x: x = self.x
        if not y: y = self.y      
        return self.level.grid_base.get_transition_probability( x, y )
    
    def get_reward( self, x, y, direction = None ):
        return self.level.get_reward(x,y,direction)