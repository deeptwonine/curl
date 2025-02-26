# electric field visualiser

import pygame

# take magnitude (Qm) and position (Qp) of a charge, and returns
# potential at point P
def pot(Q_mag, Q_pos, P):
    k = 9*(10**9)
    r = [P[0]-Q_pos[0], P[1]-Q_pos[1]]
    r_mag = (r[0]**2 + r[1]**2)**(1/2)
    if r_mag == 0:
        return 0
    else:
        return int(k*Q_mag/r_mag)

# take magnitude (Qm) and position (Qp) of a charge, and finds
# electric field at point P as [field_magnitude, field_direction],
# where field_direction is a unit vector
def f(Q_mag,Q_pos,P):
    k=9*(10**9)
    r=[P[0]-Q_pos[0],P[1]-Q_pos[1]]
    r_mag = (r[0]**2 + r[1]**2)**(1/2)
    if r_mag == 0:
        return [0,[0,0]]
    else: 
        field_mag = k*Q_mag/(r_mag**2)
        field_dir=[r[0]/(r_mag),r[1]/(r_mag)]
        return [field_mag, field_dir]
    
# colors
black = (0, 0, 0)
grey = (45, 45, 45)
light_grey = (120, 120, 120)
white = (255, 255, 255)
cream = (255, 168, 153)
light_red = (245, 99, 73)
# gradient_1 = (0, 0, 0)
# gradient_2 = (127, 0, 0)
# gradient_3 = (255, 0, 0)
# gradient_4 = (255, 127, 0)
# gradient_5 = (255, 255, 0)
# gradient_6 = (255, 255, 255)
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
font = pygame.font.SysFont(None, 20)

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

# global program variables
charge_list = []
positions = []
potentials = []
fields = []
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
    play_rect = pygame.draw.rect(screen, grey, [charge_btn_width+25, 20, width-charge_btn_width-30, height-20])
    charge_list_surface = pygame.surface.Surface((charge_btn_width, 10+5*(len(charge_list)-1)+39*len(charge_list)))
    
    # handle mouse and keyboard events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False   
        if event.type == pygame.MOUSEBUTTONUP:
            if plus_btn.collidepoint(event.pos): # check if plus_btn is clicked
                charge_list.append([1, charge_btn_width+10+int(play_rect.width/2), 5+play_rect.height/2, "Charge"+str(len(charge_list)+1)])
            elif minus_btn.collidepoint(event.pos): # check if minus_btn is clicked
                charge_list.append([-1, charge_btn_width+10+int(play_rect.width/2), 5+play_rect.height/2, "Charge"+str(len(charge_list)+1)])
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
    
    # list charges on charge_list_surface
    for i in range(len(charge_list)):
        charge = charge_list[i]
        write_text(charge_list_surface, "Q = "+str(charge[0])+" C ("+charge[3]+")", cream, 5, i*39 + 5*(i+1))
        write_text(charge_list_surface, str(charge[1:3]), white, 5, i*39 + 5*(i+1) + 21)
    screen.blit(charge_list_surface, [5, 155])
    
    # make list of all lattice point positions
    if not positions:
        for x in range(play_rect.left, play_rect.right-4, 20):
            for y in range(play_rect.top, play_rect.bottom-4, 20):
                positions.append([x,y])
    
    # create a dummy potentials list to begin with
    if not potentials:
        for position in positions:
            potentials.append(0)
            
    # make list of potentials at all positions
    for i in range(len(positions)):
        position = positions[i]
        potential_parts = []
        for charge in charge_list:
            potential_parts.append(pot(charge[0], charge[1:3], position))
        potentials[i] = sum(potential_parts)
        
    # create a dummy fields list to begin with
    if not fields:
        for position in positions:
            fields.append([0, [0, 0]])    
    
    # make list of fields at all positions
    for i in range(len(positions)):
        position = positions[i]
        field_parts = []
        for charge in charge_list:
            field_parts.append(f(charge[0], charge[1:3], position))
        temp_field = [0, 0]
        for part in field_parts:
            temp_field[0] += part[0]*part[1][0]
            temp_field[1] += part[0]*part[1][1]
        field_mag = (temp_field[0]**2 + temp_field[1]**2)**(1/2)
        if field_mag == 0:
            field_dir = [0, 0]
        else:
            field_dir = field_dir = [temp_field[0]/field_mag, temp_field[1]/field_mag]
        fields[i] = [field_mag, field_dir]
    
    # plot electric field arrows
    pot_max = 9*10**9
    pot_min = -9*10**9
    for i in range(len(positions)): 
        potential = potentials[i]
        # set arrow colour as per potential gradient
        if potential in range(pot_min, -8*10**7):
            r,g,b = gradient_1
        elif potential in range(-8*10**7, -4*10**7):
            r,g,b = gradient_15   
        elif potential in range(-4*10**7, -4*10**6):
            r,g,b = gradient_2
        elif potential in range(-4*10**6, -9*10**5):
            r,g,b = gradient_25
        elif potential in range(-9*10**5, -8*10**5):
            r,g,b = gradient_3
        elif potential in range(-8*10**5, 8*10**5):
            r,g,b = gradient_35
        elif potential in range(8*10**5, 9*10**5):
            r,g,b = gradient_4
        elif potential in range(9*10**5, 4*10**6):
            r,g,b = gradient_45
        elif potential in range(4*10**6, 4*10**7):
            r,g,b = gradient_5
        elif potential in range(4*10**7, 8*10**7):
            r,g,b = gradient_55
        elif potential in range(8*10**7, pot_max):
            r,g,b = gradient_6
        else:
            if potential >= pot_max:
                    r,g,b = gradient_6
            elif potential <= pot_min:
                    r,g,b = gradient_1
                    
        field_max = 10**5         
        field_mag = fields[i][0]
        field_dir = fields[i][1]
        length = abs(field_mag)/field_max
        
        # set arrow length as per strength
        if 7500 <= length < 10**4:
            length = 40
            w=3
        elif 5000 <= length < 7500:
            length = 35
            w=3
        elif 1000 <= length < 5000:
            length = 30
            w=3
        elif 100 <= length < 1000:
            length = 25
            w=3
        elif 10 <= length < 100:
            length = 20
            w=2
        elif 10**(-1) <= length < 10:
            length = 17
            w=2
        elif 10**(-2) <= length < 10**(-1):
            length = 13
            w=2
        elif 10**(-3) <= length < 10**(-2):
            length = 10
            w=1
        elif (1/5)*10**(-3) <= length < 10**(-3):
            length = 6
            w=1
        elif (1/75)*10**(-2) <= length < (1/5)*10**(-3):
            length = 4
            w=1
        elif 10**(-4) <= length < (1/75)*10**(-2):
            length = 2
            w=1
        else:
            if length >= 10**4:
                length = 45 
                w=4
            elif length < 10**(-4):
                length = 0 
                w=0
                
        # figure out direction of arrow
        start_x = positions[i][0] - (length/2)*field_dir[0]
        start_y = positions[i][1] - (length/2)*field_dir[1]
        start_point = [start_x, start_y]
        if field_mag == 0:
            end_point = positions[i]
        else:
            end_x = positions[i][0] + (length/2)*field_dir[0]
            end_y = positions[i][1] + (length/2)*field_dir[1]
            end_point = [end_x, end_y]
        
        # plot electric field arrow
        pygame.draw.line(screen, (r,g,b), start_point, end_point, width=w)
        triangle=[end_point, [end_point[0]+(w+1)*(field_dir[1]-field_dir[0]), end_point[1]+(w+1)*(-field_dir[1]-field_dir[0])], [end_point[0]+(w+1)*(-field_dir[1]-field_dir[0]), end_point[1]+(w+1)*(-field_dir[1]+field_dir[0])]]
        pygame.draw.polygon(screen, (r,g,b), triangle)
    
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
            coords_surface = pygame.surface.Surface((120, 28))
            write_text(coords_surface, "Q = "+str(charge[0])+" C ("+charge[3]+")", light_red, 5, 5)
            screen.blit(coords_surface, [charge[1]-plus_q.get_width()/2-120, charge[2]-plus_q.get_height()/2])
    
    # display potential and field value at each position
    for i in range(len(positions)):
        position = positions[i]
        if pygame.Rect(position[0]-10, position[1]-10, 20, 20).collidepoint(pygame.mouse.get_pos()):
            pot_field_surface = pygame.surface.Surface((300, 74))
            potential = "{:e}".format(potentials[i]) + " V"
            field = "{:e}".format(fields[i][0]) + " V/m"
            write_text(pot_field_surface, str(position), white, 5, 5)
            write_text(pot_field_surface, "Potential (V) = "+potential, light_red, 5, 28)
            write_text(pot_field_surface, "Field (E) = "+field, light_red, 5, 51)
            screen.blit(pot_field_surface, [position[0]-plus_q.get_width()/2-120, position[1]-plus_q.get_height()/2+30])
    
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