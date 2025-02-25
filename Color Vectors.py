# Electric Field Visualiser

import pygame

def pot(Qm, Qp, P):
    k = 9*(10**9)
    r = [P[0]-Qp[0], P[1]-Qp[1]]
    r_mag = (r[0]**2 + r[1]**2)**(1/2)
    if r_mag == 0:
        return 0
    else:
        return int(k*Qm/r_mag)


def F(Qm,Qp,P):
    
    # Relative position of P wrt Qp
    r=[P[0]-Qp[0],P[1]-Qp[1]]
    # Magnitude of d, squared
    rmsq=(((r[0])**2+(r[1])**2))
    
    if rmsq==0:
        return [0,[0,0]]
    
    else: 
        Fm=Qm*9*(10**9)/rmsq
        Fu=[r[0]/(rmsq**(1/2)),r[1]/(rmsq**(1/2))]
    
        return [Fm,Fu]


pygame.init()

width, height = 1400, 1000

screen = pygame.display.set_mode([width, height], pygame.SCALED|pygame.RESIZABLE)
pygame.display.set_caption("Electric Field Visualiser")

timer = pygame.time.Clock()
frame_rate = 30

charge_btn_width = 60
charge_btn_height = 50

# colors
black = (0, 0, 0)
grey = (45, 45, 45)
white = (255, 255, 255)
cream = (255, 168, 153)
light_red = (245, 99, 73)
gradient_1 = (0, 0, 0)
gradient_2 = (127, 0, 0)
gradient_3 = (255, 0, 0)
gradient_4 = (255, 127, 0)
gradient_5 = (255, 255, 0)
gradient_6 = (255, 255, 255)

# resources
plus_q = pygame.image.load('images/+.png').convert_alpha()
minus_q = pygame.image.load('images/-.png').convert_alpha()

charge_list = []

running = True

selected_charge = None

while running:
    timer.tick(frame_rate)
    screen.fill(grey)
    screen.blit(plus_q, [5 + charge_btn_width/2 - plus_q.get_width()/2, 5 + charge_btn_height/2 - plus_q.get_height()/2])
    screen.blit(minus_q, [5 + charge_btn_width/2 - minus_q.get_width()/2, 60 + charge_btn_height/2 - minus_q.get_height()/2])
    plus_btn = pygame.draw.rect(screen, white, [5, 5, charge_btn_width, charge_btn_height], 5)
    minus_btn = pygame.draw.rect(screen, white, [5, 60, charge_btn_width, charge_btn_height], 5)
    play_space = pygame.draw.rect(screen, white, [70, 5, width-75, height-10], 5)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False   
        if event.type == pygame.MOUSEBUTTONUP:
            if plus_btn.collidepoint(event.pos):
                charge_list.append([1, 70+play_space.width/2, 5+play_space.height/2])
            elif minus_btn.collidepoint(event.pos):
                charge_list.append([-1, 70+play_space.width/2, 5+play_space.height/2])
            else:
                if selected_charge:
                    selected_charge = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            for charge in charge_list[::-1]:
                if pygame.Rect(charge[1]-plus_q.get_width()/2, charge[2]-plus_q.get_height()/2, plus_q.get_width(), plus_q.get_height()).collidepoint(event.pos):
                    selected_charge = charge
                    break
    
    if selected_charge:
        charge_move_area = pygame.Rect(play_space.left+21, play_space.top+21, play_space.width-42, play_space.height-42)
        if charge_move_area.collidepoint(pygame.mouse.get_pos()):
            selected_charge[1] = pygame.mouse.get_pos()[0]
            selected_charge[2] = pygame.mouse.get_pos()[1]
        else:
            selected_charge = None
    
    count=0
    Output=[]
    potentials = []
    positions = [] # corresponding positions
    if charge_list != []: 
            for x in range(play_space.left, play_space.right-4, 20):
                for y in range(play_space.top, play_space.bottom-4, 20):
                    
                    potential_parts = []
                    for charge in charge_list:
                        potential_parts.append(pot(charge[0], charge[1:3], [x, y]))
                    potentials.append(sum(potential_parts))
                    positions.append([x, y])
            
                    Flist=[]
                    
                    Fxy=[0,0]
                    Fxyp=[0,0]
                    for Qk in charge_list:
                        
                        Flist.append(F(Qk[0],Qk[1:3],[x,y]))
                        
                    
                    # Total force magnitude
                    for Fk in Flist:
                        Fxy[0]+=Fk[0]*Fk[1][0]
                        Fxy[1]+=Fk[0]*Fk[1][1]
                        
                        Fxym=(((Fxy[0])**2+(Fxy[1])**2))**(1/2)
                        
                        
                    # Unit vector
                    if Fxym != 0:
                        unit=[Fxy[0]/Fxym, Fxy[1]/Fxym]
                    else:
                        unit=[0,0]
                    # We shall now scale the magnitude down to a presentable length
                    # Assuming the lattice points to have a unit disctance of 10 pixels
                    # and the charges to be 1 unit
                    
                    Fmax=9*(10**8)/200
                    
                    length=15
                    start=[x,y]
                    end=[x+length*unit[0], y+length*unit[1]]
                    
                    Output.append([start,end])
        
                    pot_max = 9*10**9
                    pot_min = -9*10**9
                    for i in range(len(potentials)):
                        potential = potentials[i]
                        if potential in range(pot_min, -4*10**9):
                            r,g,b = gradient_1
                            
                        elif potential in range(-4*10**8, -9*10**7):
                            r,g,b = gradient_2
                            
                        elif potential in range(-9*10**7, 0):
                            r,g,b = gradient_3
                            
                        elif potential in range(0, 9*10**7):
                            r,g,b = gradient_4
                            
                        elif potential in range(9*10**7, 4*10**8):
                            r,g,b = gradient_5
                            
                        elif potential in range(4*10**8, pot_max):
                            r,g,b = gradient_6
                            
                        else:
                            if potential >= pot_max:
                                    r = 255
                                    g = 255
                                    b = 255
                            elif potential <= pot_min:
                                    r = 0
                                    g = 0
                                    b = 0
                                    
                    pygame.draw.line(screen, (r,g,b), [x,y], Output[count][1], width=2)
                    triangle=[Output[count][1], [Output[count][1][0]+3*(unit[1]-unit[0]),Output[count][1][1]+3*(-unit[1]-unit[0])], [Output[count][1][0]+3*(-unit[1]-unit[0]),Output[count][1][1]+3*(-unit[1]+unit[0])]]
                    pygame.draw.polygon(screen, (r,g,b), triangle)
                    count+=1
                
    for charge in charge_list:
        if charge[0] == 1:
            screen.blit(plus_q, [charge[1]-plus_q.get_width()/2, charge[2]-plus_q.get_height()/2])
        elif charge[0] == -1:
            screen.blit(minus_q, [charge[1]-minus_q.get_width()/2, charge[2]-minus_q.get_height()/2])
    
    pygame.display.flip()

pygame.quit()