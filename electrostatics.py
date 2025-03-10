# electrostatics.py - functions to calculate values 
# useful in electrostatics

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