from enum import IntFlag
from typing import List,Union
from findirection.envs.actions import Actions

class Direction(IntFlag):
    Stay = 0
    North = 1
    East = 2
    South = 4
    West = 8
    All = 15
        
    def __str__(self): return self.name  


    def get_value( direction_list: List[int] ) -> int:
        dir_value = 0
        for direction,v in direction_list.items():
            if v == True:                                 
                if   direction == 'N': dir_value += Direction.North          
                elif direction == 'S': dir_value += Direction.South  
                elif direction == 'E': dir_value += Direction.East  
                elif direction == 'W': dir_value += Direction.West        
        return dir_value
      

    def get_string( direction: Union[int, List[int]] ) -> str:
        if type(direction) is list:
            return Direction.get_string_from_list( direction )
        else:
            return Direction.get_string_from_value( direction )
      
    
    def get_string_from_value( direction_value: int ) -> str: 
        dir_list = Direction.get_list(direction_value)   
        return Direction.get_string_from_list(dir_list)


    def get_string_from_list( direction_list: List[int] ) -> str:  
        dir_string = ""
        for direction in direction_list:          
            if direction == Direction.North: dir_string += "N"      
            if direction == Direction.South: dir_string += "S"                  
            if direction == Direction.East:  dir_string += "E"                
            if direction == Direction.West:  dir_string += "W"   
        return dir_string


    def get_list( direction_value: int ) -> List[int]:  
        dir_list = []      
        if direction_value & Direction.North: dir_list.append( Direction.North )
        if direction_value & Direction.South: dir_list.append( Direction.South )
        if direction_value & Direction.East:  dir_list.append( Direction.East ) 
        if direction_value & Direction.West:  dir_list.append( Direction.West )    
        return dir_list


    def get_action_list( direction_value: int ) -> List[int]:
        action_list = []       
        if direction_value & Direction.North: action_list.append( Actions.North )
        if direction_value & Direction.South: action_list.append( Actions.South )
        if direction_value & Direction.East:  action_list.append( Actions.East ) 
        if direction_value & Direction.West:  action_list.append( Actions.West )                
        return action_list        


    def get_direction_char( direction: int ):
        if direction == Direction.North: return "N"      
        if direction == Direction.South: return "S"
        if direction == Direction.East:  return "E"
        if direction == Direction.West:  return "W"       
        return ""      


    def from_action( action_value: Actions):
        if Actions(action_value) is not Actions.Stay:         
            return Direction(pow(2, action_value-1))
        return Direction.Stay


    def from_actions( action_values: Actions):
        dir_value = 0
        for action in action_values:
            dir_value += Direction.from_action( action )
        return 