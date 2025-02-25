'''
width- 1125
height- 790
** 1083
** 748
GIVEN-
Qlist=[[1,Qx,Qy], ...]

Qp=[a,b]

P=[x,y]
'''


'''
Throughout this program the suffix 'm' denotes magnitude
whereas the suffix 'p' denotes postion
'u' denotes direction or unit vector
'''

# We define F which will give us the 
# magnitude of force due to 1 charge at 1 point along with it's unit vector
def F(Qm,Qp,P):
    
    # Relative position of P wrt Qp
    d=[P[0]-Qp[0],P[1]-Qp[1]]
    # Magnitude of d, squared
    dmsq=(((d[0])**2+(d[1])**2))
    
    Fm=Qm*9*(10**9)/dmsq
    
    Fu=[d[0]/(dmsq**(1/2)),d[1]/(dmsq**(1/2))]
    
    return [Fm,Fu]

'''
We get started with the computation here
'''

# The magnitude, x, y of each charge gets appended to this list
Qlist=[]
# The Output List will be made to contain the start and end points of vectors
# at each lattice point in the form of lists containing two lists each
Output=[]
for i in range(1126):
    for j in range(791):
        
        Flist=[]
        
        Fij=[0,0]
        Fijp=[0,0]
        for Qk in Qlist:
            
            Flist.append(F(Qk[0],Qk[1:3],[i,j]))
            
        
        # Total force magnitude
        for k in Flist:
            Fij[0]+=k[0]*k[1][0]
            Fij[1]+=k[0]*k[1][1]
            
            Fijm=(((Fij[0])**2+(Fij[1])**2))**(1/2)
            
            
        # Unit vector
        Fiju=[Fij[0]/Fijm, Fij[1]/Fijm]
        
        # We shall now scale the magnitude down to a presentable length
        # Assuming the lattice points to have a unit disctance of 10 pixels
        # and the charges to be 1 unit
        
        Fmax=9*(10**9)/200
        
        length=Fijm/Fmax
        start=[i,j]
        end=[i+length*Fiju[0], j+length*Fiju[1]]
        
        Output.append([start,end])
        

        
