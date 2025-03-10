# curl.py - a simple electric field visualiser

import pygame
import copy
from math import pi, sin, cos, fabs
from colors import *
from electrostatics import *

# constants
PROG_NAME = "Curl"
WIDTH, HEIGHT = 1185, 630
PLAY_SURF_WIDTH, PLAY_SURF_HEIGHT = 1000, 600
charge_btn_width = 150
charge_btn_height = 70
mode_btn_height = 50
TEXT_SIZE = 20
FPS = 30

# initiate pygame and set up the display, timer, font
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED|pygame.RESIZABLE)
timer = pygame.time.Clock()
font = pygame.font.Font('font/Doto-Black.ttf', TEXT_SIZE)

# get resources
plus_q = pygame.image.load('images/plus.png').convert_alpha()
minus_q = pygame.image.load('images/minus.png').convert_alpha()
plus_btn_up = pygame.image.load('images/plus_btn_up.png').convert_alpha()
minus_btn_up = pygame.image.load('images/minus_btn_up.png').convert_alpha()
custom_btn_up = pygame.image.load('images/custom_btn_up.png').convert_alpha()
discrete_mode_btn_up = pygame.image.load('images/discrete_mode_btn_up.png').convert_alpha()
cont_mode_btn_up = pygame.image.load('images/cont_mode_btn_up.png').convert_alpha()
plus_btn_down = pygame.image.load('images/plus_btn_down.png').convert_alpha()
minus_btn_down = pygame.image.load('images/minus_btn_down.png').convert_alpha()
custom_btn_down = pygame.image.load('images/custom_btn_down.png').convert_alpha()
discrete_mode_btn_down = pygame.image.load('images/discrete_mode_btn_down.png').convert_alpha()
cont_mode_btn_down = pygame.image.load('images/cont_mode_btn_down.png').convert_alpha()
play_surf_frame = pygame.image.load('images/play_surf_frame.png').convert_alpha()
edit_charge_dialog_img = pygame.image.load('images/edit_charge_dialog.png')
plus_mag_btn_up = pygame.image.load('images/plus_mag_btn_up.png').convert_alpha()
minus_mag_btn_up = pygame.image.load('images/minus_mag_btn_up.png').convert_alpha()
done_btn_up = pygame.image.load('images/done_btn_up.png').convert_alpha()
plus_mag_btn_down = pygame.image.load('images/plus_mag_btn_down.png').convert_alpha()
minus_mag_btn_down = pygame.image.load('images/minus_mag_btn_down.png').convert_alpha()
done_btn_down = pygame.image.load('images/done_btn_down.png').convert_alpha()
icon = pygame.image.load('images/icon.png').convert_alpha()

# set up display nuances
pygame.display.set_caption(PROG_NAME)
pygame.display.set_icon(icon)

# returns a pygame.surface.Surface with given text
def write_text(text, color):
	screen_text = font.render(text, False, color)
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
editing_charge = None
right_click_charge = None
delete_text = None
rename_text = None

is_plus_btn_pressed = False
is_minus_btn_pressed = False
is_custom_btn_pressed = False
is_mode_btn_pressed = False

is_editing_charge = False
is_name_field_focused = True
is_mag_field_focused = False
is_x_field_focused = False
is_y_field_focused = False
is_charge_mag_btn_pressed = False
is_done_btn_pressed = False
is_cursor_visible = False

is_continuous_mode = False

running = True
frame_count = 0

# game execution loop
while running:
    
    # setup timer, screen and some screen elements
    timer.tick(FPS)
    frame_count += 1
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
        minus_btn_rect = minus_btn_down.get_rect(left=5, top=86)
        screen.blit(minus_btn_down, (5, 86))
        
    if not is_custom_btn_pressed:
        custom_btn_rect = custom_btn_up.get_rect(left=5, top=155)
        screen.blit(custom_btn_up, (5, 155))
    else:
        custom_btn_rect = custom_btn_down.get_rect(left=5, top=161)
        screen.blit(custom_btn_down, (5, 161))
    
    if is_continuous_mode:
        if not is_mode_btn_pressed:
            mode_btn_rect = cont_mode_btn_up.get_rect(left=5, top=555)
            screen.blit(cont_mode_btn_up, (5, 555))
        else:
            mode_btn_rect = cont_mode_btn_down.get_rect(left=5, top=561)
            screen.blit(cont_mode_btn_down, (5, 561))
    else:
        if not is_mode_btn_pressed:
            mode_btn_rect = discrete_mode_btn_up.get_rect(left=5, top=555)
            screen.blit(discrete_mode_btn_up, (5, 555))
        else:
            mode_btn_rect = discrete_mode_btn_down.get_rect(left=5, top=561)
            screen.blit(discrete_mode_btn_down, (5, 561))

    # display play space as per selected mode
    screen.blit(play_surf_frame, (160, 5))
    play_surface = pygame.surface.Surface((PLAY_SURF_WIDTH, PLAY_SURF_HEIGHT))
    play_surface.fill(dark_lavender)
    play_rect = play_surface.get_rect(left=168, top=13)
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
        potential = "{:e}".format(calc_potential(charge_list, pygame.mouse.get_pos())) + "V"
        field = "{:e}".format(calc_field(charge_list, pygame.mouse.get_pos())[0]) + "V/m"
        pos_text = write_text(str(pygame.mouse.get_pos()), white)
        potential_text = write_text("Potential(V) = "+potential, light_red)
        field_text = write_text("Field(E) = "+field, light_red)
        hover_bg = pygame.surface.Surface((max(pos_text.get_width(), potential_text.get_width(), field_text.get_width()) + 8,
                                           pos_text.get_height() + potential_text.get_height() + field_text.get_height() + 8))
        hover_bg.fill(grey)
        hover_bg.blit(pos_text, (4, 4))
        hover_bg.blit(potential_text, (4, 4 + pos_text.get_height()))
        hover_bg.blit(field_text, (4, 4 + pos_text.get_height() + potential_text.get_height()))
        if hover_bg.get_rect(left=pygame.mouse.get_pos()[0]-168, top=pygame.mouse.get_pos()[1]-13).right > 1000:
            if hover_bg.get_rect(left=pygame.mouse.get_pos()[0]-168, top=pygame.mouse.get_pos()[1]-13).bottom > 600:
                play_surface.blit(hover_bg, (pygame.mouse.get_pos()[0]-168-hover_bg.get_width(), pygame.mouse.get_pos()[1]-13-hover_bg.get_height()))
            else:
                play_surface.blit(hover_bg, (pygame.mouse.get_pos()[0]-168-hover_bg.get_width(), pygame.mouse.get_pos()[1]-13))
        elif hover_bg.get_rect(left=pygame.mouse.get_pos()[0]-168, top=pygame.mouse.get_pos()[1]-13).bottom > 600:
            play_surface.blit(hover_bg, (pygame.mouse.get_pos()[0]-168, pygame.mouse.get_pos()[1]-13-hover_bg.get_height()))
        else:
            play_surface.blit(hover_bg, (pygame.mouse.get_pos()[0]-168, pygame.mouse.get_pos()[1]-13))

    screen.blit(play_surface, (168, 13))
    
    # show charge adding dialogue
    if is_editing_charge:
        overlay = pygame.Surface((1185, 630))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        edit_charge_dialog = edit_charge_dialog_img.convert_alpha()
        if not is_charge_mag_btn_pressed:
            if editing_charge[4] == "+":
                charge_mag_btn_rect = plus_mag_btn_up.get_rect(left=446, top=309)
                edit_charge_dialog.blit(plus_mag_btn_up, (13, 137))
            elif editing_charge[4] == "-":
                charge_mag_btn_rect = minus_mag_btn_up.get_rect(left=446, top=309)
                edit_charge_dialog.blit(minus_mag_btn_up, (13, 137))
        else:
            if editing_charge[4] == "+":
                charge_mag_btn_rect = plus_mag_btn_down.get_rect(left=446, top=311)
                edit_charge_dialog.blit(plus_mag_btn_down, (13, 139))
            elif editing_charge[4] == "-":
                charge_mag_btn_rect = minus_mag_btn_down.get_rect(left=446, top=311)
                edit_charge_dialog.blit(minus_mag_btn_down, (13, 139))
        
        if not is_done_btn_pressed:
            done_btn_rect = done_btn_up.get_rect(left=446, top=412)
            edit_charge_dialog.blit(done_btn_up, (13, 240))
        else:
            done_btn_rect = done_btn_down.get_rect(left=446, top=414)
            edit_charge_dialog.blit(done_btn_down, (13, 242))

        charge_name_text = write_text(editing_charge[3], black)
        if editing_charge[0] == "" or editing_charge[0] == ".":
            charge_mag_text = write_text('0', light_grey)
        else:
            charge_mag_text = write_text(editing_charge[0], black)
        if editing_charge[1] == "":
            charge_x_text = write_text('0', light_grey)
        else:
            charge_x_text = write_text(editing_charge[1], black)   
        if editing_charge[2] == "":
            charge_y_text = write_text('0', light_grey)
        else:
            charge_y_text = write_text(editing_charge[2], black)
        edit_charge_dialog.blit(charge_name_text, (20, 75))
        edit_charge_dialog.blit(charge_mag_text,  (52, 137))
        edit_charge_dialog.blit(charge_x_text,  (40, 200))
        edit_charge_dialog.blit(charge_y_text,  (188, 200))

        if frame_count % 15 == 0:
                is_cursor_visible = not is_cursor_visible
        
        if is_name_field_focused and is_cursor_visible:
            pygame.draw.line(edit_charge_dialog, black, (charge_name_text.get_width()+20, 78), (charge_name_text.get_width()+20, 95))
        elif is_mag_field_focused and is_cursor_visible:
            pygame.draw.line(edit_charge_dialog, black, (charge_mag_text.get_width()+52, 140), (charge_mag_text.get_width()+52, 157))
        elif is_x_field_focused and is_cursor_visible:
            pygame.draw.line(edit_charge_dialog, black, (charge_x_text.get_width()+40, 203), (charge_x_text.get_width()+40, 220))
        elif is_y_field_focused and is_cursor_visible:
            pygame.draw.line(edit_charge_dialog, black, (charge_y_text.get_width()+188, 203), (charge_y_text.get_width()+188, 220))
        
        screen.blit(edit_charge_dialog, (433, 172))
        name_text_rect = pygame.Rect(446, 247, 292, 28)
        mag_text_rect = pygame.Rect(478, 309, 260, 28)
        x_text_rect = pygame.Rect(466, 372, 123, 28)
        y_text_rect = pygame.Rect(614, 372, 123, 28)
    
    # handle mouse and keyboard events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False   
        if event.type == pygame.MOUSEBUTTONUP:
            is_plus_btn_pressed = False
            is_minus_btn_pressed = False
            is_custom_btn_pressed = False
            is_mode_btn_pressed = False
            is_charge_mag_btn_pressed = False
            is_done_btn_pressed = False
            
            if plus_btn_rect.collidepoint(event.pos) and not is_editing_charge:
                charge_list.append([1, int(PLAY_SURF_WIDTH/2), int(PLAY_SURF_HEIGHT/2), "Charge"+str(len(charge_list)+1)])
            elif minus_btn_rect.collidepoint(event.pos) and not is_editing_charge:
                charge_list.append([-1, int(PLAY_SURF_WIDTH/2), int(PLAY_SURF_HEIGHT/2), "Charge"+str(len(charge_list)+1)])
            elif custom_btn_rect.collidepoint(event.pos) and not is_editing_charge:
                is_editing_charge = True
                charge_list.append([1, int(PLAY_SURF_WIDTH/2), int(PLAY_SURF_HEIGHT/2), "Charge"+str(len(charge_list)+1)])
                editing_charge = [str(fabs(charge_list[-1][0])), str(charge_list[-1][1]), str(charge_list[-1][2]), charge_list[-1][3], "+"]
            elif delete_text and right_click_charge and delete_text.collidepoint(event.pos):
                charge_list.remove(right_click_charge)
                right_click_charge = None
            elif rename_text and right_click_charge and rename_text.collidepoint(event.pos):
                new_name = right_click_charge[3]
                rename_text = None
            elif is_editing_charge and charge_mag_btn_rect.collidepoint(event.pos):
                if editing_charge[4] == "+":
                    editing_charge[4] = "-"
                elif editing_charge[4] == "-":
                    editing_charge[4] = "+"
            elif is_editing_charge and done_btn_rect.collidepoint(event.pos):
                is_editing_charge = False
                if (editing_charge[0] == "" or editing_charge[0] == ".") and editing_charge[4] == "+":
                    editing_charge[0] = 0.0
                elif (editing_charge[0] == "" or editing_charge[0] == ".") and editing_charge[4] == "-":
                    editing_charge[0] = -0.0
                else:
                    editing_charge[0] = float(editing_charge[4] + editing_charge[0])
                if editing_charge[1] == "":
                    editing_charge[1] = 0
                else:
                    editing_charge[1] = int(editing_charge[1])
                if editing_charge[2] == "":
                    editing_charge[2] = 0
                else:
                    editing_charge[2] = int(editing_charge[2])
                del editing_charge[4]
                charge_list[-1] = editing_charge
            elif is_editing_charge and name_text_rect.collidepoint(event.pos):
                is_name_field_focused = True
                is_mag_field_focused = False
                is_x_field_focused = False
                is_y_field_focused = False
            elif is_editing_charge and mag_text_rect.collidepoint(event.pos):
                is_name_field_focused = False
                is_mag_field_focused = True
                is_x_field_focused = False
                is_y_field_focused = False
            elif is_editing_charge and x_text_rect.collidepoint(event.pos):
                is_name_field_focused = False
                is_mag_field_focused = False
                is_x_field_focused = True
                is_y_field_focused = False
            elif is_editing_charge and y_text_rect.collidepoint(event.pos):
                is_name_field_focused = False
                is_mag_field_focused = False
                is_x_field_focused = False
                is_y_field_focused = True
            elif mode_btn_rect.collidepoint(event.pos) and not is_editing_charge:
                is_continuous_mode = not is_continuous_mode
            elif not is_editing_charge: # check if a selected charge is released
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
            if mode_btn_rect.collidepoint(event.pos):
                is_mode_btn_pressed = True
            if is_editing_charge and charge_mag_btn_rect.collidepoint(event.pos):
                is_charge_mag_btn_pressed = True
            if is_editing_charge and done_btn_rect.collidepoint(event.pos):
                is_done_btn_pressed = True
            
            for charge in charge_list[::-1]:
                if pygame.Rect(168+charge[1]-plus_q.get_width()/2, 13+charge[2]-plus_q.get_height()/2, plus_q.get_width(), plus_q.get_height()).collidepoint(event.pos):
                    selected_charge = charge
                    break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                is_editing_charge = False
                if (editing_charge[0] == "" or editing_charge[0] == ".") and editing_charge[4] == "+":
                    editing_charge[0] = 0.0
                elif (editing_charge[0] == "" or editing_charge[0] == ".") and editing_charge[4] == "-":
                    editing_charge[0] = -0.0
                else:
                    editing_charge[0] = float(editing_charge[4] + editing_charge[0])
                if editing_charge[1] == "":
                    editing_charge[1] = 0
                else:
                    editing_charge[1] = int(editing_charge[1])
                if editing_charge[2] == "":
                    editing_charge[2] = 0
                else:
                    editing_charge[2] = int(editing_charge[2])
                del editing_charge[4]
                charge_list[-1] = editing_charge
            
            if is_editing_charge and is_name_field_focused:
                charge_name = editing_charge[3]
                if event.key == pygame.K_BACKSPACE and len(charge_name)>0:
                    charge_name = charge_name[:-1]
                elif event.key != pygame.K_BACKSPACE and len(charge_name)<10: 
                    charge_name += event.unicode
                editing_charge[3] = charge_name
            elif is_editing_charge and is_mag_field_focused:
                allowed_chars = (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                                 pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_PERIOD)
                charge_mag_str = editing_charge[0]
                if event.key == pygame.K_BACKSPACE and len(charge_mag_str)>0:
                    charge_mag_str = charge_mag_str[:-1]
                elif event.key in allowed_chars:
                    charge_mag_str += event.unicode
                editing_charge[0] = charge_mag_str
            elif is_editing_charge and is_x_field_focused:
                charge_x_str = editing_charge[1]
                allowed_chars = (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                                 pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9)
                if event.key == pygame.K_BACKSPACE and len(charge_x_str)>0:
                    charge_x_str = charge_x_str[:-1]
                elif event.key in allowed_chars and int(charge_x_str + event.unicode) <= 1000:
                    charge_x_str += event.unicode
                editing_charge[1] = charge_x_str
            elif is_editing_charge and is_y_field_focused:
                charge_y_str = editing_charge[2]
                allowed_chars = (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                                 pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9)
                if event.key == pygame.K_BACKSPACE and len(charge_y_str)>0:
                    charge_y_str = charge_y_str[:-1]
                elif event.key in allowed_chars and int(charge_y_str + event.unicode) <= 600:
                    charge_y_str += event.unicode
                editing_charge[2] = charge_y_str
    
    # handle drag and drop of selected charge
    if selected_charge:
        charge_move_area = pygame.Rect(play_rect.left, play_rect.top, PLAY_SURF_WIDTH, PLAY_SURF_HEIGHT)
        if charge_move_area.collidepoint(pygame.mouse.get_pos()):
            selected_charge[1] = pygame.mouse.get_pos()[0]-168
            selected_charge[2] = pygame.mouse.get_pos()[1]-13
        else:
            selected_charge = None
    
    # show menu on right clicking charge
    if right_click_charge:
        right_click_surface = pygame.surface.Surface((70, 51))
        right_click_surface.blit(write_text("Delete", light_red), (5, 5))
        right_click_surface.blit(write_text("Rename", white), (5, 28))
        delete_text = pygame.Rect(right_click_charge[1]-plus_q.get_width()/2-80, right_click_charge[2]-plus_q.get_height()/2, 80, 25)
        rename_text = pygame.Rect(right_click_charge[1]-plus_q.get_width()/2-80, right_click_charge[2]-plus_q.get_height()/2+20, 80, 26)
        screen.blit(right_click_surface, [right_click_charge[1]-plus_q.get_width()/2-70, right_click_charge[2]-plus_q.get_height()/2])
    
    # blit stuff to the screen and flip it #5;5,28,51
    pygame.display.flip()

# quit when out of game execution loop
pygame.quit()