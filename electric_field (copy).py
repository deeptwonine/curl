# curl - a simple electric field visualiser

import pygame


def pot(charge_list, P):
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

def f(charge_list, P):
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
        field_dir = [int(field_components[0]/field_mag), int(field_components[1]/field_mag)]
    return [field_mag, field_dir]
        
    
# colors
black = (0, 0, 0)
grey = (45, 45, 45)
light_grey = (120, 120, 120)
white = (255, 255, 255)
cream = (255, 168, 153)
light_red = (245, 99, 73)
gradient_6 = (245, 66, 66)
gradient_55 = (245, 120, 66)
gradient_5 = (245, 194, 66)
gradient_45 = (225, 225, 66)
gradient_4 = (194, 245, 66)
gradient_35 = (120, 245, 120)
gradient_3 = (66, 245, 194)
gradient_25 = (66, 225, 225)
gradient_2 = (66, 194, 245)
gradient_15 = (66, 120, 245)
gradient_1 = (66, 66, 245)

# constants
width, height = 1400, 1000
charge_btn_width = 150
charge_btn_height = 70

# initiate pygame and set up the display, timer, frame_rate, font
pygame.init()
screen = pygame.display.set_mode([width, height], pygame.SCALED|pygame.RESIZABLE)
pygame.display.set_caption("Curl")

timer = pygame.time.Clock()
frame_rate = 50
font = pygame.font.Font("font/SourceSerif4_18pt-Black.ttf", 15)

# resources
plus_q = pygame.image.load('images/+.png').convert_alpha()
minus_q = pygame.image.load('images/-.png').convert_alpha()
icon = pygame.image.load('images/icon.png').convert_alpha()
pygame.display.set_icon(icon)

# takes a surface, a piece of text, a color, and blits the given
# text in given colour onto given surface
def write_text(surface, text, color, x, y):
	screen_text = font.render(text, True, color)
	surface.blit(screen_text, [x, y])
	return screen_text

def draw_field_arrow(surface, field, colour, start=[-1, -1], end=[-1, -1]):    
    field_mag = field[0]
    field_dir = field[1]
    
    if start != [-1, -1]:
        start_point = start
        if field_mag == 0:
            end_point = start_point
        else:
            end_x = start[0] + (50)*field_dir[0]
            end_y = start[1] + (50)*field_dir[1]
            end_point = [end_x, end_y]
    elif end != [-1, -1]:
        end_point = end
        if field_mag == 0:
            start_point = end_point
        else:
            start_x = end[0] - (50)*field_dir[0]
            start_y = end[1] - (50)*field_dir[1]
            start_point = [start_x, start_y]
    
    centre_point = [int((start_point[0]+end_point[0])/2), int((start_point[1]+end_point[1])/2)]
    # plot electric field arrow
    pygame.draw.line(surface, colour, start_point, end_point)
    triangle=[centre_point, [centre_point[0]+(3)*(field_dir[1]-field_dir[0]), centre_point[1]+(3)*(-field_dir[1]-field_dir[0])], [centre_point[0]+(3)*(-field_dir[1]-field_dir[0]), centre_point[1]+(3)*(-field_dir[1]+field_dir[0])]]
    pygame.draw.polygon(surface, colour, triangle)
    
    return start_point, end_point

# global program variables
charge_list = []
selected_charge = None
right_click_charge = None
delete_text = None
rename_text = None
new_name = None
rename_btn = None

running = True

# game execution loop starts
while running:
    
    # setup timer, screen and some screen elements
    timer.tick(frame_rate)
    screen.fill(grey)
    plus_btn = pygame.draw.rect(screen, light_grey, [5, 5, charge_btn_width, charge_btn_height])
    minus_btn = pygame.draw.rect(screen, light_grey, [5, 80, charge_btn_width, charge_btn_height])
    screen.blit(plus_q, [5 + charge_btn_width/2 - plus_q.get_width()/2, 5 + charge_btn_height/2 - plus_q.get_height()/2])
    screen.blit(minus_q, [5 + charge_btn_width/2 - minus_q.get_width()/2, 80 + charge_btn_height/2 - minus_q.get_height()/2])
    play_rect = pygame.draw.rect(screen, grey, [charge_btn_width+35, 30, width-charge_btn_width-50, height-40])
    charge_list_surface = pygame.surface.Surface((charge_btn_width, 10+5*(len(charge_list)-1)+39*len(charge_list)))
    
    # handle mouse and keyboard events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False   
        if event.type == pygame.MOUSEBUTTONUP:
            if plus_btn.collidepoint(event.pos): # check if plus_btn is clicked
                charge_list.append([1, charge_btn_width+10+int(play_rect.width/2), 5+int(play_rect.height/2), "Charge"+str(len(charge_list)+1)])
            elif minus_btn.collidepoint(event.pos): # check if minus_btn is clicked
                charge_list.append([-1, charge_btn_width+10+int(play_rect.width/2), 5+int(play_rect.height/2), "Charge"+str(len(charge_list)+1)])
            elif delete_text and right_click_charge and delete_text.collidepoint(event.pos): # check if delete button is clicked
                charge_list.remove(right_click_charge)
                right_click_charge = None
            elif rename_text and right_click_charge and rename_text.collidepoint(event.pos): # check if rename button is clicked
                new_name = ""
                rename_text = None
            elif rename_btn and right_click_charge and new_name != None and rename_btn.collidepoint(event.pos): # check if rename button is clicked after renaming
                right_click_charge[3] = new_name
                right_click_charge = None
                new_name = None
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
        if event.type == pygame.MOUSEBUTTONDOWN: # check if a charge is selected
            for charge in charge_list[::-1]:
                if pygame.Rect(charge[1]-plus_q.get_width()/2, charge[2]-plus_q.get_height()/2, plus_q.get_width(), plus_q.get_height()).collidepoint(event.pos):
                    selected_charge = charge
                    break
        if event.type == pygame.KEYDOWN: # handle charge name typing
            if new_name != None:
                if event.key == pygame.K_BACKSPACE and len(new_name)>0:
                    new_name = new_name[:-1]
                elif event.key == pygame.K_RETURN:
                    right_click_charge[3] = new_name
                    right_click_charge = None
                    new_name = None
                else:
                    new_name += event.unicode
                    
    # draw_field_arrow(screen, [1, [-35, -2]], white, start=[500, 800])
    
    for charge in charge_list:
        if charge[0] > 0:
            global_end_points = []
            end_points = []
            end_points.append(draw_field_arrow(screen, [charge[0], [0, 1]], white, start=charge[1:3])[1])
            end_points.append(draw_field_arrow(screen, [charge[0], [0, -1]], white, start=charge[1:3])[1])
            end_points.append(draw_field_arrow(screen, [charge[0], [1, 0]], white, start=charge[1:3])[1])
            end_points.append(draw_field_arrow(screen, [charge[0], [-1, 0]], white, start=charge[1:3])[1])
            end_points.append(draw_field_arrow(screen, [charge[0], [1, 1]], white, start=charge[1:3])[1])
            end_points.append(draw_field_arrow(screen, [charge[0], [-1, 1]], white, start=charge[1:3])[1])
            end_points.append(draw_field_arrow(screen, [charge[0], [1, -1]], white, start=charge[1:3])[1])
            end_points.append(draw_field_arrow(screen, [charge[0], [-1, -1]], white, start=charge[1:3])[1])
            for end_point in end_points:
                if end_point[0] in range(play_rect.left, play_rect.right-4) and end_point[1] in range(play_rect.top, play_rect.bottom-4):
                    global_end_points.append(end_point)
                    
            while global_end_points:
                to_add = []
                to_remove = []
                for end_point in global_end_points:
                    to_remove.append(end_point)
                    field = f(charge_list, end_point)
                    field_mag = field[0]
                    field_dir = field[1]
                    arrow_end = draw_field_arrow(screen, [field_mag, field_dir], white, start=end_point)[1]
                    if arrow_end[0] in range(play_rect.left, play_rect.right-4) and arrow_end[1] in range(play_rect.top, play_rect.bottom-4):
                        to_add.append(arrow_end)
                for end_point in to_remove:
                    global_end_points.remove(end_point)
                for end_point in to_add:
                    global_end_points.append(end_point)
                    
        elif charge[0] < 0:
            global_start_points = []
            start_points = []
            start_points.append(draw_field_arrow(screen, [charge[0], [0, -1]], white, end=charge[1:3])[0])
            start_points.append(draw_field_arrow(screen, [charge[0], [0, 1]], white, end=charge[1:3])[0])
            start_points.append(draw_field_arrow(screen, [charge[0], [-1, 0]], white, end=charge[1:3])[0])
            start_points.append(draw_field_arrow(screen, [charge[0], [1, 0]], white, end=charge[1:3])[0])
            start_points.append(draw_field_arrow(screen, [charge[0], [-1, -1]], white, end=charge[1:3])[0])
            start_points.append(draw_field_arrow(screen, [charge[0], [1, -1]], white, end=charge[1:3])[0])
            start_points.append(draw_field_arrow(screen, [charge[0], [-1, 1]], white, end=charge[1:3])[0])
            start_points.append(draw_field_arrow(screen, [charge[0], [1, 1]], white, end=charge[1:3])[0])
            for start_point in start_points:
                if int(start_point[0]) in range(play_rect.left, play_rect.right-4) and int(start_point[1]) in range(play_rect.top, play_rect.bottom-4):
                    global_start_points.append(start_point) 
                    
            while global_start_points:
                to_add = []
                to_remove = []
                for start_point in global_start_points:
                    field = f(charge_list, start_point)
                    field_mag = field[0]
                    field_dir = field[1]
                    arrow_start = draw_field_arrow(screen, [field_mag, field_dir], white, end=start_point)[0]
                    if arrow_start[0] in range(play_rect.left, play_rect.right-4) and arrow_start[1] in range(play_rect.top, play_rect.bottom-4):
                        to_add.append(arrow_start)
                    to_remove.append(start_point)
                for end_p in to_remove:
                    global_start_points.remove(end_p)
                for start_p in to_add:
                    global_start_points.append(start_p)
    
    # list charges on charge_list_surface
    for i in range(len(charge_list)):
        charge = charge_list[i]
        write_text(charge_list_surface, "Q = "+str(charge[0])+"C ("+charge[3]+")", cream, 5, i*39 + 5*(i+1))
        write_text(charge_list_surface, str(charge[1:3]), white, 5, i*39 + 5*(i+1) + 21)
    screen.blit(charge_list_surface, [5, 155])
    
    # handle drag and drop of selected charge
    if selected_charge:
        charge_move_area = pygame.Rect(play_rect.left, play_rect.top, play_rect.width, play_rect.height)
        if charge_move_area.collidepoint(pygame.mouse.get_pos()):
            selected_charge[1] = pygame.mouse.get_pos()[0]
            selected_charge[2] = pygame.mouse.get_pos()[1]
        else:
            selected_charge = None
    
    # display charges in charge_list            
    for charge in charge_list:
        if charge[0] == 1:
            screen.blit(plus_q, [charge[1]-plus_q.get_width()/2, charge[2]-plus_q.get_height()/2])
        elif charge[0] == -1:
            screen.blit(minus_q, [charge[1]-minus_q.get_width()/2, charge[2]-minus_q.get_height()/2])
    
    # display charge details on hover
    for charge in charge_list[::-1]:
        if charge != right_click_charge and pygame.Rect(charge[1]-plus_q.get_width()/2, charge[2]-plus_q.get_height()/2, plus_q.get_width(), plus_q.get_height()).collidepoint(pygame.mouse.get_pos()):
            charge_details_surface = pygame.surface.Surface((130, 28))
            write_text(charge_details_surface, "Q = "+str(charge[0])+"C ("+charge[3]+")", light_red, 5, 5)
            screen.blit(charge_details_surface, [charge[1]-plus_q.get_width()/2-120, charge[2]-plus_q.get_height()/2])
    
    # display potential and field value at each position
    if play_rect.collidepoint(pygame.mouse.get_pos()):
        pot_field_surface = pygame.surface.Surface((300, 74))
        potential = "{:e}".format(pot(charge_list, pygame.mouse.get_pos())) + "V"
        field = "{:e}".format(f(charge_list, pygame.mouse.get_pos())[0]) + "V/m"
        write_text(pot_field_surface, str(pygame.mouse.get_pos()), white, 5, 5)
        write_text(pot_field_surface, "Potential (V) = "+potential, light_red, 5, 28)
        write_text(pot_field_surface, "Field (E) = "+field, light_red, 5, 51)
        screen.blit(pot_field_surface, [pygame.mouse.get_pos()[0]-plus_q.get_width()/2-120, pygame.mouse.get_pos()[1]-plus_q.get_height()/2+30])
    
    # show menu on right clicking charge
    if right_click_charge:
        right_click_surface = pygame.surface.Surface((70, 51))
        write_text(right_click_surface, "Delete", light_red, 5, 5)
        write_text(right_click_surface, "Rename", white, 5, 28)
        delete_text = pygame.Rect(right_click_charge[1]-plus_q.get_width()/2-80, right_click_charge[2]-plus_q.get_height()/2, 80, 25)
        rename_text = pygame.Rect(right_click_charge[1]-plus_q.get_width()/2-80, right_click_charge[2]-plus_q.get_height()/2+20, 80, 26)
        screen.blit(right_click_surface, [right_click_charge[1]-plus_q.get_width()/2-70, right_click_charge[2]-plus_q.get_height()/2])
    
    # handle renaming a charge
    if new_name != None:
        rename_surface = pygame.surface.Surface((120, 51))
        type_surface = pygame.surface.Surface((110, 22))
        type_surface.fill(white)
        new_name_text = write_text(type_surface, new_name, black, 2, 2)
        write_text(rename_surface, "Rename", white, 5, 28)
        rename_btn = pygame.Rect(right_click_charge[1]-plus_q.get_width()/2-120, right_click_charge[2]-plus_q.get_height()/2+28, 120, 23)
        rename_surface.blit(type_surface, [5, 5])
        screen.blit(rename_surface, [right_click_charge[1]-plus_q.get_width()/2-120, right_click_charge[2]-plus_q.get_height()/2])
    
    # blit stuff to the screen and flip it
    pygame.display.flip()

# quit when out of game execution loop
pygame.quit()