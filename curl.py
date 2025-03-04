# curl.py - a simple electric field visualiser

import pygame
from math import pi, sin, cos
from colors import *

# constants
PROG_NAME = "Curl"
WIDTH, HEIGHT = 1345, 890
PLAY_SURF_WIDTH, PLAY_SURF_HEIGHT = 1180, 880
charge_btn_width = 150
charge_btn_height = 70
mode_btn_height = 50
TEXT_SIZE = 15
FPS = 50

# initiate pygame and set up the display, timer, font
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.SCALED|pygame.RESIZABLE)
timer = pygame.time.Clock()
font = pygame.font.Font("font/PixelifySans-SemiBold.ttf", TEXT_SIZE)

# get resources
plus_q = pygame.image.load('images/plus.png').convert_alpha()
minus_q = pygame.image.load('images/minus.png').convert_alpha()
plus_btn_up = pygame.image.load('images/plus_btn_up.png').convert_alpha()
minus_btn_up = pygame.image.load('images/minus_btn_up.png').convert_alpha()
custom_btn_up = pygame.image.load('images/custom_btn_up.png').convert_alpha()
discrete_mode_btn_up = pygame.image.load('images/discrete_mode_btn_up.png').convert_alpha()
plus_btn_down = pygame.image.load('images/plus_btn_down.png').convert_alpha()
minus_btn_down = pygame.image.load('images/minus_btn_down.png').convert_alpha()
custom_btn_down = pygame.image.load('images/custom_btn_down.png').convert_alpha()
discrete_mode_btn_down = pygame.image.load('images/discrete_mode_btn_down.png').convert_alpha()
icon = pygame.image.load('images/icon.png').convert_alpha()

# set up display nuances
pygame.display.set_caption(PROG_NAME)
pygame.display.set_icon(icon)

# calculates potential at a point P (x, y) 
# due to charges in charge_list
def calc_potential(charge_list, P):
    k = 9*(10**9)
    potential = 0
    for charge in charge_list:
        r = [P[0]-charge[1], P[1]-charge[2]]
        r_mag = (r[0]**2 + r[1]**2)**(1/2)
        if r_mag == 0:
            potential += 0
        else:
            potential += int(k*charge[0]/r_mag)
    return potential

# calculates electric field at a point P (x, y) 
# due to charges in charge_list
def calc_field(charge_list, P):
    k=9*(10**9)
    field_parts = []
    for charge in charge_list:
        r=[P[0]-charge[1],P[1]-charge[2]]
        r_mag = (r[0]**2 + r[1]**2)**(1/2)
        if r_mag == 0:
            field_parts.append([0,[0,0]])
        else: 
            field_mag = k*charge[0]/(r_mag**2)
            field_dir=[r[0]/(r_mag),r[1]/(r_mag)]
            field_parts.append([field_mag, field_dir])
    
    field_components = [0, 0]
    for part in field_parts:
        field_components[0] += part[0]*part[1][0]
        field_components[1] += part[0]*part[1][1]
    field_mag = (field_components[0]**2 + field_components[1]**2)**(1/2)
    if field_mag == 0:
        field_dir = [0, 0]
    else:
        field_dir = [field_components[0]/field_mag, field_components[1]/field_mag]
    return [field_mag, field_dir]

# returns a pygame.surface.Surface with given text
def write_text(text, color):
	screen_text = font.render(text, True, color)
	return screen_text

# takes a surface, potential and field value, and draws an electric field
# arrow of required magnitude, with colour gradient as per potntial,
# with arrow tail at start OR arrow head at end OR arrow centred at centre
def draw_field_arrow(surface, potential, field, centre_arrow=True, start=[-1, -1], end=[-1, -1], centre=[-1, -1]):
    pot_max = 9*10**9
    pot_min = -9*10**9
    # set arrow colour as per potential gradient
    if potential in range(pot_min, -8*10**7):
        r,g,b = gradient_10
    elif potential in range(-8*10**7, -4*10**7):
        r,g,b = gradient_15   
    elif potential in range(-4*10**7, -4*10**6):
        r,g,b = gradient_20
    elif potential in range(-4*10**6, -9*10**5):
        r,g,b = gradient_25
    elif potential in range(-9*10**5, -8*10**5):
        r,g,b = gradient_30
    elif potential in range(-8*10**5, 8*10**5):
        r,g,b = gradient_35
    elif potential in range(8*10**5, 9*10**5):
        r,g,b = gradient_40
    elif potential in range(9*10**5, 4*10**6):
        r,g,b = gradient_45
    elif potential in range(4*10**6, 4*10**7):
        r,g,b = gradient_50
    elif potential in range(4*10**7, 8*10**7):
        r,g,b = gradient_55
    elif potential in range(8*10**7, pot_max):
        r,g,b = gradient_60
    else:
        if potential >= pot_max:
                r,g,b = gradient_60
        elif potential <= pot_min:
                r,g,b = gradient_10
    
    field_max = 10**5   
    field_mag = field[0]
    field_dir = field[1]
    length = abs(field_mag)/field_max
    
    # set arrow length as per strength
    if 7500 <= length < 10**4:
        length=40
        w=3
    elif 5000 <= length < 7500:
        length=35
        w=3
    elif 1000 <= length < 5000:
        length=30
        w=3
    elif 100 <= length < 1000:
        length=25
        w=3
    elif 10 <= length < 100:
        length=20
        w=2
    elif 10**(-1) <= length < 10:
        length=17
        w=2
    elif 10**(-2) <= length < 10**(-1):
        length=13
        w=2
    elif 10**(-3) <= length < 10**(-2):
        length=10
        w=1
    elif (1/5)*10**(-3) <= length < 10**(-3):
        length=6
        w=1
    elif (1/75)*10**(-2) <= length < (1/5)*10**(-3):
        length=4
        w=1
    elif 10**(-4) <= length < (1/75)*10**(-2):
        length=2
        w=1
    else:
        if length >= 10**4:
            length=45
            w=4
        elif length < 10**(-4):
            length=0
            w=0
    
    if start != [-1, -1]:
        start_point = start
        if field_mag == 0:
            end_point = start
        else:
            end_x = start[0] + (16)*field_dir[0]
            end_y = start[1] + (16)*field_dir[1]
            end_point = [round(end_x), round(end_y)]
    elif end != [-1, -1]:
        end_point = end
        if field_mag == 0:
            start_point = end
        else:
            start_x = end[0] - (16)*field_dir[0]
            start_y = end[1] - (16)*field_dir[1]
            start_point = [round(start_x), round(start_y)]
    elif centre != [-1, 1]:
        start_x = centre[0] - (length/2)*field_dir[0]
        start_y = centre[1] - (length/2)*field_dir[1]
        start_point = [start_x, start_y]
        if field_mag == 0:
            end_point = centre
        else:
            end_x = centre[0] + (length/2)*field_dir[0]
            end_y = centre[1] + (length/2)*field_dir[1]
            end_point = [end_x, end_y]
    
    if centre_arrow:
        arrow_point = [(start_point[0]+end_point[0])/2, (start_point[1]+end_point[1])/2]
    else:
        arrow_point = end_point
    
    pygame.draw.line(surface, (r,g,b), start_point, end_point, width=w)
    triangle=(arrow_point, 
              (arrow_point[0]+(w+2)*(field_dir[1]-field_dir[0]), arrow_point[1]+(w+2)*(-field_dir[1]-field_dir[0])), 
              (arrow_point[0]+(w+2)*(-field_dir[1]-field_dir[0]), arrow_point[1]+(w+2)*(-field_dir[1]+field_dir[0])))
    pygame.draw.polygon(surface, (r,g,b), triangle)
    
    return start_point, end_point

# global program variables
charge_list = []
selected_charge = None
right_click_charge = None
delete_text = None
rename_text = None
new_name = None
rename_btn = None
charge_to_add = None
charge_name = None
charge_mag_str = None
charge_pos_str = None
add_charge_btn = None
charge_add_selected = None
type_name_rect = None
type_mag_rect = None
type_pos_rect = None

is_plus_btn_pressed = False
is_minus_btn_pressed = False
is_custom_btn_pressed = False
is_mode_btn_pressed = False
is_continuous_mode = False

running = True

# game execution loop
while running:
    
    # setup timer, screen and some screen elements
    timer.tick(FPS)
    screen.fill(lavender)
    
    if not is_plus_btn_pressed:
        plus_btn_rect = plus_btn_up.get_rect(left=5, top=5)
        screen.blit(plus_btn_up, (5, 5))
    else:
        plus_btn_rect = plus_btn_down.get_rect(left=5, top=5)
        screen.blit(plus_btn_down, (5, 11))
    
    if not is_minus_btn_pressed:
        minus_btn_rect = minus_btn_up.get_rect(left=5, top=80)
        screen.blit(minus_btn_up, (5, 80))
    else:
        minus_btn_rect = minus_btn_down.get_rect(left=5, top=80)
        screen.blit(minus_btn_down, (5, 86))
        
    if not is_custom_btn_pressed:
        custom_btn_rect = custom_btn_up.get_rect(left=5, top=155)
        screen.blit(custom_btn_up, (5, 155))
    else:
        custom_btn_rect = custom_btn_down.get_rect(left=5, top=161)
        screen.blit(custom_btn_down, (5, 161))
        
    mode_btn = pygame.draw.rect(screen, light_grey, [5, HEIGHT-5-mode_btn_height, charge_btn_width, mode_btn_height])
    play_surface = pygame.surface.Surface((PLAY_SURF_WIDTH, PLAY_SURF_HEIGHT))
    play_surface.fill(dark_lavender)
    play_rect = play_surface.get_rect(left=160, top=5)
    
    if is_continuous_mode:
        screen.blit(write_text("CONTINUOUS FIELD", white), (mode_btn.left+4, mode_btn.top+3))
        screen.blit(write_text("LINES MODE", white), (mode_btn.left+27, mode_btn.top+27))
    else:
        screen.blit(write_text("DISCRETE FIELD", white), (mode_btn.left+16, mode_btn.top+3))
        screen.blit(write_text("ARROWS MODE", white), (mode_btn.left+18, mode_btn.top+27))
    
    # handle mouse and keyboard events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False   
        if event.type == pygame.MOUSEBUTTONUP:
            is_plus_btn_pressed = False
            is_minus_btn_pressed = False
            is_custom_btn_pressed = False
            
            if plus_btn_rect.collidepoint(event.pos) and charge_name == None: # check if plus_btn is clicked
                charge_list.append([1, PLAY_SURF_WIDTH/2, PLAY_SURF_HEIGHT/2, "Charge"+str(len(charge_list)+1)])
            elif minus_btn_rect.collidepoint(event.pos) and charge_name == None: # check if minus_btn is clicked
                charge_list.append([-1, PLAY_SURF_WIDTH/2, PLAY_SURF_HEIGHT/2, "Charge"+str(len(charge_list)+1)])
            elif custom_btn_rect.collidepoint(event.pos):
                charge_to_add = [1, charge_btn_width+10+int(play_rect.width/2), 5+int(play_rect.height/2), "Charge"+str(len(charge_list)+1)]
                charge_name = charge_to_add[3]
                charge_mag_str = str(charge_to_add[0])
                charge_pos_str = str(charge_to_add[1:3])
                charge_add_selected = "name"
            elif delete_text and right_click_charge and delete_text.collidepoint(event.pos): # check if delete button is clicked
                charge_list.remove(right_click_charge)
                right_click_charge = None
            elif rename_text and right_click_charge and rename_text.collidepoint(event.pos): # check if rename button is clicked
                new_name = right_click_charge[3]
                rename_text = None
            elif rename_btn and right_click_charge and new_name != None and rename_btn.collidepoint(event.pos): # check if rename button is clicked after renaming
                right_click_charge[3] = new_name
                right_click_charge = None
                new_name = None
            elif add_charge_btn and charge_name != None and add_charge_btn.collidepoint(event.pos):
                charge_to_add[3] = charge_name
                charge_to_add[0] = float(eval(charge_mag_str))
                charge_pos = charge_pos_str.lstrip('[').rstrip(']').split(', ')
                charge_pos = [int(charge_pos[0]), int(charge_pos[1])]
                charge_to_add[1:3] = charge_pos
                charge_list.append(charge_to_add)
                charge_name = None
                charge_mag = None
                charge_pos = None
                charge_to_add = None
                type_name_rect = None
                type_mag_rect = None
                type_pos_rect = None
            elif type_name_rect and charge_name != None and type_name_rect.collidepoint(event.pos):
                charge_add_selected = "name"
            elif type_mag_rect and charge_name != None and type_mag_rect.collidepoint(event.pos):
                charge_add_selected = "mag"
            elif type_pos_rect and charge_name != None and type_pos_rect.collidepoint(event.pos):
                charge_add_selected = "pos"
            elif mode_btn.collidepoint(event.pos):
                is_continuous_mode = not is_continuous_mode
            else: # check if a selected charge is released
                if selected_charge:
                    selected_charge = None
                if right_click_charge:
                    right_click_charge = None
                    new_name = None
            
            if event.button == 3: # check if there has been a right click
                for charge in charge_list[::-1]:
                    if pygame.Rect(charge[1]-plus_q.get_width()/2, charge[2]-plus_q.get_height()/2, plus_q.get_width(), plus_q.get_height()).collidepoint(event.pos):
                        right_click_charge = charge
                        break
        if event.type == pygame.MOUSEBUTTONDOWN:
            if plus_btn_rect.collidepoint(event.pos):
                is_plus_btn_pressed = True
            if minus_btn_rect.collidepoint(event.pos):
                is_minus_btn_pressed = True
            if custom_btn_rect.collidepoint(event.pos):
                is_custom_btn_pressed = True
            
            for charge in charge_list[::-1]:
                if pygame.Rect(160+charge[1]-plus_q.get_width()/2, 5+charge[2]-plus_q.get_height()/2, plus_q.get_width(), plus_q.get_height()).collidepoint(event.pos):
                    selected_charge = charge
                    break
        if event.type == pygame.KEYDOWN: # handle charge name typing
            if new_name != None and charge_name == None:
                if event.key == pygame.K_BACKSPACE and len(new_name)>0:
                    new_name = new_name[:-1]
                elif event.key == pygame.K_RETURN:
                    right_click_charge[3] = new_name
                    right_click_charge = None
                    new_name = None
                else:
                    new_name += event.unicode
            if new_name == None and charge_name != None:
                if event.key == pygame.K_RETURN:
                    charge_to_add[3] = charge_name
                    if charge_mag_str == "":
                        charge_to_add[0] = 0
                    elif charge_mag_str[-1] == "-":
                        charge_to_add[0] = -1
                    else:
                        charge_to_add[0] = float(eval(charge_mag_str))
                    charge_pos = charge_pos_str.lstrip('[').rstrip(']').split(', ')
                    charge_pos = [int(charge_pos[0]), int(charge_pos[1])]
                    charge_to_add[1:3] = charge_pos
                    charge_list.append(charge_to_add)
                    charge_name = None
                    charge_mag = None
                    charge_pos = None
                    charge_to_add = None
                    type_name_rect = None
                    type_mag_rect = None
                    type_pos_rect = None
                if charge_add_selected == "name":
                    if event.key == pygame.K_BACKSPACE and len(charge_name)>0:
                        charge_name = charge_name[:-1]
                    elif event.key != pygame.K_RETURN:
                        charge_name += event.unicode
                elif charge_add_selected == "mag":
                    if event.key == pygame.K_BACKSPACE and len(charge_mag_str)>0:
                        charge_mag_str = charge_mag_str[:-1]
                    elif event.key != pygame.K_RETURN:
                        charge_mag_str += event.unicode
                elif charge_add_selected == "pos":
                    if event.key == pygame.K_BACKSPACE and len(charge_pos_str)>0:
                        charge_pos_str = charge_pos_str[:-1]
                    elif event.key != pygame.K_RETURN:
                        charge_pos_str += event.unicode
    
    # display play space as per selected mode
    if is_continuous_mode:
        for i in range(len(charge_list)):
            charge = charge_list[i]
            if charge[0] > 0:
                global_end_points = []
                end_points = []
                for j in range(8):
                        field_dir = [cos(2*pi/8*j+(2*pi/16)), sin(2*pi/8*j+(2*pi/16))]
                        end_points.append(draw_field_arrow(play_surface, calc_potential(charge_list, charge[1:3]), [charge[0], field_dir], start=charge[1:3])[1])
                for end_point in end_points:
                    if end_point[0] in range(0, PLAY_SURF_WIDTH+1) and end_point[1] in range(0, PLAY_SURF_HEIGHT+1):
                        global_end_points.append(end_point)
                
                to_remove = []
                while global_end_points:
                    to_add = []
                    for end_point in global_end_points:
                        to_remove.append(end_point)
                        field = calc_field(charge_list, end_point)
                        arrow_end = draw_field_arrow(play_surface, calc_potential(charge_list, end_point), field, start=end_point)[1]
                        if arrow_end[0] in range(0, PLAY_SURF_WIDTH+1) and arrow_end[1] in range(0, PLAY_SURF_HEIGHT+1):
                            to_add.append(arrow_end)
                    for end_point in to_add:
                        global_end_points.append(end_point)
                    for end_point in to_remove:
                        if end_point in global_end_points:
                            global_end_points.remove(end_point)
                    
                        
            elif charge[0] < 0:
                global_start_points = []
                start_points = []
                for j in range(8):
                    field_dir = [cos(2*pi/8*j+(2*pi/16)), sin(2*pi/8*j+(2*pi/16))]
                    start_points.append(draw_field_arrow(play_surface, calc_potential(charge_list, charge[1:3]), [charge[0], field_dir], end=charge[1:3])[0])
                for start_point in start_points:
                    if int(start_point[0]) in range(0, PLAY_SURF_WIDTH+1) and int(start_point[1]) in range(0, PLAY_SURF_HEIGHT+1):
                        global_start_points.append(start_point) 
                
                to_remove = []
                while global_start_points:
                    to_add = []
                    for start_point in global_start_points:
                        to_remove.append(start_point)
                        field = calc_field(charge_list, start_point)
                        arrow_start = draw_field_arrow(play_surface, calc_potential(charge_list, start_point), field, end=start_point)[0]
                        if arrow_start[0] in range(0, PLAY_SURF_WIDTH+1) and arrow_start[1] in range(0, PLAY_SURF_HEIGHT+1):
                            to_add.append(arrow_start)
                    for start_point in to_add:
                        global_start_points.append(start_point)
                    for start_point in to_remove:
                        if start_point in global_start_points:
                            global_start_points.remove(start_point)
    else:
        for x in range(10, PLAY_SURF_WIDTH-10+1, 20):
            for y in range(10, PLAY_SURF_HEIGHT-10+1, 20):
                draw_field_arrow(play_surface, calc_potential(charge_list, [x, y]), calc_field(charge_list, [x, y]), False, centre=[x, y])
    
    # handle drag and drop of selected charge
    if selected_charge:
        charge_move_area = pygame.Rect(play_rect.left, play_rect.top, PLAY_SURF_WIDTH, PLAY_SURF_HEIGHT)
        if charge_move_area.collidepoint(pygame.mouse.get_pos()):
            selected_charge[1] = pygame.mouse.get_pos()[0]-160
            selected_charge[2] = pygame.mouse.get_pos()[1]-5
        else:
            selected_charge = None
    
    # display charges in play space from charge_list            
    for charge in charge_list:
        if charge[0] > 0:
            play_surface.blit(plus_q, [charge[1]-plus_q.get_width()/2, charge[2]-plus_q.get_height()/2])
        elif charge[0] < 0:
            play_surface.blit(minus_q, [charge[1]-minus_q.get_width()/2, charge[2]-minus_q.get_height()/2])
    
    # display charge details on hover
    for charge in charge_list[::-1]:
        if charge != right_click_charge and pygame.Rect(charge[1]-plus_q.get_width()/2, charge[2]-plus_q.get_height()/2, plus_q.get_width(), plus_q.get_height()).collidepoint(pygame.mouse.get_pos()):
            charge_details_surface = pygame.surface.Surface((130, 28))
            charge_details_surface.blit(write_text("Q = "+str(charge[0])+"C ("+charge[3]+")", light_red), (5, 5))
            screen.blit(charge_details_surface, [charge[1]-plus_q.get_width()/2-120, charge[2]-plus_q.get_height()/2])
    
    # display potential and field value at each position
    if play_rect.collidepoint(pygame.mouse.get_pos()):
        pot_field_surface = pygame.surface.Surface((300, 74))
        potential = "{:e}".format(calc_potential(charge_list, pygame.mouse.get_pos())) + "V"
        field = "{:e}".format(calc_field(charge_list, pygame.mouse.get_pos())[0]) + "V/m"
        pot_field_surface.blit(write_text(str(pygame.mouse.get_pos()), white), (5, 5))
        pot_field_surface.blit(write_text("Potential (V) = "+potential, light_red), (5, 28))
        pot_field_surface.blit(write_text("Field (E) = "+field, light_red), (5, 51))
        screen.blit(pot_field_surface, [pygame.mouse.get_pos()[0]-plus_q.get_width()/2-120, pygame.mouse.get_pos()[1]-plus_q.get_height()/2+30])
    
    # show charge adding dialogue
    if charge_name != None:
        charge_adding_surface = pygame.surface.Surface((charge_btn_width, 100))
        type_surface_name = pygame.surface.Surface((charge_btn_width-10, 22))
        type_surface_mag = pygame.surface.Surface((charge_btn_width-10, 22))
        type_surface_pos = pygame.surface.Surface((charge_btn_width-10, 22))
        type_name_rect = pygame.Rect(12, 205, charge_btn_width-10, 22)
        type_mag_rect = pygame.Rect(12, 232, charge_btn_width-10, 22)
        type_pos_rect = pygame.Rect(12, 259, charge_btn_width-10, 22)
        type_surface_name.fill(white)
        type_surface_mag.fill(white)
        type_surface_pos.fill(white)
        type_surface_name.blit(write_text(charge_name, black), (2, 2))
        type_surface_mag.blit(write_text(charge_mag_str, black), (2, 2))
        type_surface_pos.blit(write_text(charge_pos_str, black), (2, 2))
        charge_adding_surface.blit(write_text("ADD CHARGE", white), (5, 80))
        add_charge_btn = pygame.Rect(5, 280, charge_btn_width, 23)
        charge_adding_surface.blit(type_surface_name, [5, 5])
        charge_adding_surface.blit(type_surface_mag, [5, 32])
        charge_adding_surface.blit(type_surface_pos, [5, 59])
        screen.blit(charge_adding_surface, [5, 200])
    
    # show menu on right clicking charge
    if right_click_charge:
        right_click_surface = pygame.surface.Surface((70, 51))
        right_click_surface.blit(write_text("Delete", light_red), (5, 5))
        right_click_surface.blit(write_text("Rename", white), (5, 28))
        delete_text = pygame.Rect(right_click_charge[1]-plus_q.get_width()/2-80, right_click_charge[2]-plus_q.get_height()/2, 80, 25)
        rename_text = pygame.Rect(right_click_charge[1]-plus_q.get_width()/2-80, right_click_charge[2]-plus_q.get_height()/2+20, 80, 26)
        screen.blit(right_click_surface, [right_click_charge[1]-plus_q.get_width()/2-70, right_click_charge[2]-plus_q.get_height()/2])
    
    # handle renaming a charge
    if new_name != None:
        rename_surface = pygame.surface.Surface((120, 51))
        type_surface = pygame.surface.Surface((110, 22))
        type_surface.fill(white)
        type_surface.blit(write_text(new_name, black), (2, 2))
        rename_surface.blit(write_text("Rename", white), (5, 28))
        rename_btn = pygame.Rect(right_click_charge[1]-plus_q.get_width()/2-120, right_click_charge[2]-plus_q.get_height()/2+28, 120, 23)
        rename_surface.blit(type_surface, [5, 5])
        screen.blit(rename_surface, [right_click_charge[1]-plus_q.get_width()/2-120, right_click_charge[2]-plus_q.get_height()/2])
    
    # blit stuff to the screen and flip it
    screen.blit(play_surface, (160, 5))
    pygame.display.flip()

# quit when out of game execution loop
pygame.quit()