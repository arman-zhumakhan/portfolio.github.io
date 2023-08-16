
import numpy as np
from numpy import inf
from ipycanvas import hold_canvas
from findirection.envs.draw_grid import DrawGrid, Level
from findirection.envs.grid_info import GridInfo
from findirection.envs.arrows import Arrows
from findirection.envs.directions import Direction


class DrawInfo():

    arrow_color = '#00008b'    
    text_bg_color = 'rgba(40,40,40,0.7)' 
    text_fg_color = '#fff'             

    precision = 3   


    def __init__( self, draw_grid: DrawGrid, grid_info: GridInfo, **kwargs: dict ):
    
        self.grid = draw_grid.grid

        self.grid_info = grid_info

        self.draw_grid = draw_grid    
        self.canvas = self.draw_grid.canvases[Level.Text]

        self.set_properties(kwargs.get('grid',None))   

        self.arrows = Arrows( draw_grid.cell_pixels, draw_grid.padding,length=24,width=7,height=11)     


    def draw( self, props: dict ):

        if props is not None:    
            self.precision = props.get('precision', self.precision)
            directions = props.get('directions',None)
            if directions is not None:                                
                self.process_direction_arrows(directions)
                self.process_direction_text(directions)

            self.process_text(props)

            self.process_info(props)

            if props.get('coords',False):
                self.draw_coordinates()



    def set_default_values(self,args): 
  
        defaultargs = ((0,0),"",190,20)

        args += (None,)*len(defaultargs)      

        args = tuple(map(lambda x, y: y if y is not None else x, defaultargs, args))
        return args


    def process_info(self,info):

        fg_color = 'black'
        bk_color = 'white'

        text = info.get('side_info',None)
        if text is not None:     

            if self.draw_grid.side_panel is None:
                raise Exception("\'side_panel\' must be specified during grid creation to allow side panel text.")

            if type(self.draw_grid.side_panel) == dict:
                fg_color = self.draw_grid.side_panel.get('text_fg','black') 
                bk_color = self.draw_grid.side_panel.get('color','white')           

            if self.draw_grid.side_panel:

                for item in text:
                    (cx,cy),value,width,height = self.set_default_values(item)

                    cx += self.draw_grid.width_pixels            
                    self.clear_info_panel_text( cx, cy, width, height, bk_color)

                for item in text:
                    (cx,cy),value,width,height = self.set_default_values(item)

                    cx += self.draw_grid.width_pixels            
                    self.info_panel_text(cx,cy,value,width,height,fg_color=fg_color,bk_color=bk_color)  


        text = info.get('bottom_info',None)
        if text is not None:        

            if self.draw_grid.bottom_panel is None:
                raise Exception("\'bottom_panel\' must be specified during grid creation to allow bottom panel text.")

            if type(self.draw_grid.bottom_panel) == dict:
                fg_color = self.draw_grid.bottom_panel.get('text_fg','black') 
                bk_color = self.draw_grid.bottom_panel.get('color','white')             

            if self.draw_grid.bottom_panel:

                for item in text:
                    (cx,cy),value,width,height = self.set_default_values(item)
                    cy += self.draw_grid.height_pixels 
                    self.clear_info_panel_text( cx, cy, width, height, bk_color)

                for item in text:
                    (cx,cy),value,width,height = self.set_default_values(item)

                    cy += self.draw_grid.height_pixels            
                    self.info_panel_text(cx,cy,value,width,height,fg_color=fg_color,bk_color=bk_color)            


    def process_text(self,info):

        text = info.get('text',None)      
        if text is not None:
            if isinstance(text,np.ndarray):
                self.draw_text_array(text)
            else:
                for (cx,cy),value in text:  
                    self.draw_cell_text(cx,cy,value)


    def process_direction_arrows(self,directions):

        arrows = directions.get('arrows',None)
        if arrows is not None:
            if isinstance(arrows,np.ndarray):
                self.draw_direction_arrow_array(arrows)  
            else:          

                if len(arrows) > 0 and (type(arrows[0][0]) == int):        
                    for (cx,cy) in arrows:
                        direction = self.grid_info.get_directions(cx,cy)
                        self.draw_direction_arrow(cx,cy,direction)   

                else:
                    for (cx,cy),direction in arrows:  
                        self.draw_direction_arrow(cx,cy,direction)  


    def process_direction_text(self,directions):

        text = directions.get('text',None)
        if text is not None:
            if isinstance(text,np.ndarray):
                self.draw_direction_text_array(text)  
            else:
                if len(text) > 0 and (type(text[0][0]) == int):       
                    for (cx,cy) in text:
                        direction = self.grid_info.get_directions(cx,cy)
                        self.draw_direction_text(cx,cy,direction)   

                else:
                    for (cx,cy),direction in text:  
                        self.draw_direction_text(cx,cy,direction)     



    def set_properties( self, grid_props: dict ):

        if grid_props is not None:
            colors = grid_props.get('colors',None)
            if colors is not None:    
                self.arrow_color = colors.get('arrows', self.arrow_color)    
                self.text_fg_color = colors.get('text_fg', self.text_fg_color)  
                self.text_bg_color = colors.get('text_bg', self.text_bg_color)  


          
    def draw_direction_arrow( self, x, y, directions ):   
    
        canvas = self.draw_grid.canvases[Level.Overlay]
        color = self.arrow_color    
        padding = self.draw_grid.padding
        cell_pixels = self.draw_grid.cell_pixels
        px,py = self.draw_grid.grid_to_pixels( [x,y], padding, padding )          

        with hold_canvas(canvas):             
            canvas.clear_rect(px,py,cell_pixels,cell_pixels)

        with hold_canvas(canvas):       
            self.arrows.draw(canvas,px,py,directions,color)       


    def draw_direction_arrow_array(self, directions: np.array):
        canvas = self.draw_grid.canvases[Level.Overlay]      
        with hold_canvas(canvas):    
            for y in range(directions.shape[0]):
                for x in range(directions.shape[1]):
                    self.draw_direction_arrow( x, y, directions[y,x])    


    
    def draw_direction_text( self, x, y, direction ):
        self.draw_cell_text( x, y, Direction.get_string(direction) )


    def draw_direction_text_array(self,directions):                 
        for y in range(directions.shape[0]):
            for x in range(directions.shape[1]):
                if x != self.grid.end[0] or y != self.grid.end[1]: 
                    self.draw_direction_text( x, y, directions[y,x])    
  

    def draw_coordinates(self):
        with hold_canvas(self.canvas):    
            for y in range(self.draw_grid.grid.height):
                for x in range(self.draw_grid.grid.width):
                    self.draw_cell_text( x, y, f"({x},{y})")   
  


    def draw_text_array(self,text):
        with hold_canvas(self.canvas):    
            for y in range(text.shape[0]):
                for x in range(text.shape[1]):
                    self.draw_cell_text( x, y, text[y,x])   


    def info_panel_text( self, x, y, text,width,height,                        
                       fg_color='#000', 
                       bk_color='#fff',
                       font='bold 14px sans-serif',
                       text_align='left',
                       text_baseline='top'):                       
        canvas = self.canvas
        canvas.save()
        with hold_canvas(canvas): 
            canvas.fill_style = fg_color
            canvas.text_align = text_align
            canvas.text_baseline = text_baseline
            canvas.font = font
            canvas.fill_text(text, x, y)
        canvas.restore()


    def clear_info_panel_text( self, x, y, width, height, bk_color='#fff'):
        canvas = self.canvas
        with hold_canvas(canvas):     
            canvas.fill_style = bk_color      
            canvas.fill_rect(x,y-5,width,height) 


    def draw_cell_text( self, x, y, value, color = None, back_color = None ):   
        num_value = False
        if type(value).__name__.startswith('str'):
            if len(value) == 0:
                return
        elif isinstance(x, (int, float, complex)) and not isinstance(x, bool):
            num_value = True
            if np.isnan(value):
                return

        if self.grid.test_for_base_area(x,y):      
            return
    
        if isinstance(value, float):
            if self.precision == 0:
                value = value.astype(int)
            else:
                value = round(value,self.precision)        
    
        canvas = self.canvas
        padding = self.draw_grid.padding

        if color is None: color = self.text_fg_color
        if back_color is None: back_color = self.text_bg_color

        gx,gy = self.draw_grid.grid_to_pixels( [x,y], padding, padding )    
        cx,cy = self.draw_grid.get_center(gx,gy) 

        bk_height = 20
        bk_width = 36

        if len(str(value)) > 4:
            bk_width += (len(str(value))-4) * 6

        if bk_width > (self.draw_grid.cell_pixels - 4):
            bk_width = (self.draw_grid.cell_pixels - 4)

        x_off = (bk_width//2)
        y_off = (bk_height//2)

        font_size = 14
        text_offset = 5
        if (num_value and self.precision > 1) or \
           (not num_value and len(str(value)) >= 3):
            font_size = 12 
            text_offset = 4
        font_str = f"bold {font_size}px sans-serif"

        canvas.save()

        with hold_canvas(canvas):                    
            canvas.clear_rect(cx-x_off,cy-y_off,bk_width,bk_height) 
            if back_color is not None:
                canvas.fill_style = back_color        
                canvas.fill_rect(cx-x_off,cy-y_off,bk_width,bk_height) 

        with hold_canvas(canvas):                         
            canvas.fill_style = color
            canvas.text_align = 'center'
            canvas.font = font_str
            canvas.fill_text(f"{value}", cx, cy+text_offset)

        canvas.restore()