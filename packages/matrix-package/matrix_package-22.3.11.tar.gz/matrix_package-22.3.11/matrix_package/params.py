from typing import Iterable


def params_(nmol : Iterable[int] = None):

    def decor(func):
        def wrap():
            print('============================================================================')
            func()
            print("============================================================================")
        return wrap() 

    global xyz,df, dt, c, dmass, x, y, z, new_m, new_xyz, tab_trajec,mass_m, mass_a, gdr_c
    global d1,d2,d3,d4,d5,d6,d7,d8,d9,d10
    global coordinate,mass,natom,charge,data
    global time , dx, dy, dz, dxx, dyy, dzz, dxxx, dyyy, dzzz
    
    if nmol == 1:
        [new_m, new_xyz, tab_trajec] = [ [[]], [[]], [[]] ]
        [mass_m, mass_a, dt, time] = [ [[]], [[]], [[]], [[]] ]
        [x,y,z, dmass] = [ [[]], [[]], [[]], [[]] ]
        [coordinate,mass,natom,charge] = [ [[]], [[]], [[]], [[]] ]
        [data,xyz,df,c] = [ [[]], [[]], [[]], [[]] ]
        [d1,d2,d3,d4] = [ [[]], [[]], [[]], [[]] ]
        [d5,d6,d7,d8] = [ [[]], [[]], [[]], [[]] ]
        [d9,d10] = [ [[]], [[]] ]
        [dx, dy, dz] = [ [[]], [[]], [[]] ]  
        [dxx, dyy, dzz] = [ [[]], [[]], [[]] ]  
        [dxxx, dyyy, dzzz] = [ [[]], [[]], [[]] ]  

        gdr_c = [ [[],[]], [[],[]] ] 
        gdr_c = [[]]
    elif nmol == 2:   
        [new_m, new_xyz, tab_trajec] = [ [[],[]], [[],[]], [[],[]] ]
        [mass_m, mass_a, dt, time] = [ [[],[]], [[],[]], [[],[]], [[],[]] ]
        [x,y,z, dmass] = [ [[],[]], [[],[]], [[],[]], [[],[]] ]
        [coordinate,mass,natom,charge] = [ [[],[]], [[],[]], [[],[]], [[],[]] ]
        [data,xyz,df,c] = [ [[],[]], [[],[]], [[],[]], [[],[]] ]
        [d1,d2,d3,d4] = [ [[],[]], [[],[]], [[],[]], [[],[]] ]
        [d5,d6,d7,d8] = [ [[],[]], [[],[]], [[],[]], [[],[]] ]
        [d9,d10] = [ [[],[]], [[],[]] ]  
        [dx, dy, dz] = [ [[],[]], [[],[]], [[],[]] ]  
        [dxx, dyy, dzz] = [ [[],[]], [[],[]], [[],[]] ]  
        [dxxx, dyyy, dzzz] = [ [[],[]], [[],[]], [[],[]] ]  
        gdr_c = [ [[],[]], [[],[]] ] 
    elif nmol == 3:
        [new_m, new_xyz, tab_trajec] = [ [[],[],[]], [[],[],[]], [[],[],[]] ]
        [mass_m, mass_a, dt, time] = [ [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]] ]
        [x,y,z, dmass] = [ [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]] ]
        [coordinate,mass,natom,charge] = [ [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]] ]
        [data,xyz,df,c] = [ [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]] ]
        [d1,d2,d3,d4] =[ [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]] ]
        [d5,d6,d7,d8] = [ [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]] ]
        [d9,d10] = [ [[],[],[]], [[],[],[]] ]
        gdr_c = [ [[],[],[]] ,[[],[],[]], [[],[],[]] ] 
        [dx, dy, dz] = [ [[],[],[]], [[],[],[]], [[],[],[]] ]  
        [dxx, dyy, dzz] = [ [[],[],[]], [[],[],[]], [[],[],[]] ]
        [dxxx, dyyy, dzzz] = [ [[],[],[]], [[],[],[]], [[],[],[]] ]
    elif nmol == 4:
        [new_m, new_xyz, tab_trajec] = [ [[],[],[],[]], [[],[],[],[]], [[],[],[],[]] ]
        [mass_m, mass_a, dt, time] = [ [[],[],[],[]], [[],[],[],[]], [[],[],[],[]], [[],[],[],[]] ]
        [x,y,z, dmass] = [ [[],[],[],[]],[[],[],[],[]], [[],[],[],[]], [[],[],[],[]] ]
        [coordinate,mass,natom,charge] = [ [[],[],[],[]], [[],[],[],[]], [[],[],[],[]],[[],[],[],[]] ]
        [data,xyz,df,c] = [ [[],[],[],[]], [[],[],[],[]], [[],[],[],[]], [[],[],[],[]] ]
        [d1,d2,d3,d4] = [ [[],[],[],[]], [[],[],[],[]], [[],[],[],[]], [[],[],[],[]] ]
        [d5,d6,d7,d8] = [ [[],[],[],[]], [[],[],[],[]], [[],[],[],[]], [[],[],[],[]] ]
        [d9,d10] = [ [[],[],[],[]], [[],[],[],[]] ]
        gdr_c = [ [[],[],[],[]], [[],[],[],[]], [[],[],[],[]], [[],[],[],[]] ] 
        [dx, dy, dz] = [ [[],[],[],[]], [[],[],[],[]], [[],[],[],[]] ]  
        [dxx, dyy, dzz] = [ [[],[],[],[]], [[],[],[],[]], [[],[],[],[]] ]
        [dxxx, dyyy, dzzz] = [ [[],[],[],[]], [[],[],[],[]], [[],[],[],[]] ]
    elif nmol == 5:
        [dx, dy, dz] = [ [[],[],[],[],[]], [[],[],[],[],[]], [[],[],[],[],[]] ]  
        [dxx, dyy, dzz] = [ [[],[],[],[],[]], [[],[],[],[],[]], [[],[],[],[],[]] ]
        [dxxx, dyy, dzzyz] = [ [[],[],[],[],[]], [[],[],[],[],[]], [[],[],[],[],[]] ]
        [new_m, new_xyz, tab_trajec] = [ [[],[],[],[],[]], [[],[],[],[],[]], [[],[],[],[],[]] ]
        [mass_m, mass_a, dt, time] = [ [[],[],[],[],[]], [[],[],[],[],[]], [[],[],[],[],[]], [[],[],[],[],[]] ]
        [x,y,z, dmass] = [ [[],[],[],[],[]], [[],[],[],[],[]], [[],[],[],[],[]], [[],[],[],[],[]] ]
        [coordinate,mass,natom,charge] = [ [[],[],[],[],[]], [[],[],[],[],[]], [[],[],[],[],[]], [[],[],[],[],[]] ]
        [data,xyz,df,c] = [ [[],[],[],[],[]], [[],[],[],[],[]], [[],[],[],[],[]], [[],[],[],[],[]] ]
        [d1,d2,d3,d4] = [ [[],[],[],[],[]], [[],[],[],[],[]], [[],[],[],[],[]], [[],[],[],[],[]] ]
        [d5,d6,d7,d8] = [ [[],[],[],[],[]], [[],[],[],[],[]], [[],[],[],[],[]], [[],[],[],[],[]] ]
        [d9,d10] = [ [[],[],[],[],[]], [[],[],[],[],[]] ]
        gdr_c = [ [[],[],[],[],[]], [[],[],[],[],[]], [[],[],[],[],[]], [[],[],[],[],[]], [[],[],[],[],[]] ] 
    elif nmol == 6:
        [dx, dy, dz] = [ [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]] ]  
        [dxxx, dyyy, dzzz] = [ [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]] ]
        [dxx, dyy, dzz] = [ [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]] ]
        [new_m, new_xyz, tab_trajec] = [ [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]] ]
        [mass_m, mass_a, dt, time] = [ [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]] ]
        [x,y,z, dmass] = [ [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]] ]
        [coordinate,mass,natom,charge] = [ [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]] ]
        [data,xyz,df,c] = [ [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]] ]
        [d1,d2,d3,d4] = [ [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]] ]
        [d5,d6,d7,d8] = [ [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]] ]
        [d9,d10] = [ [[],[],[],[],[],[]], [[],[],[],[],[],[]] ]
        gdr_c = [ [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]]  ] 
    elif nmol == 7:
        [new_m, new_xyz, tab_trajec] = [ [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]] ]
        [mass_m, mass_a, dt, time] = [ [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]] ]
        [x,y,z, dmass] = [ [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]] ]
        [coordinate,mass,natom,charge] = [ [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]] ]
        [data,xyz,df,c] = [ [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]] ]
        [d1,d2,d3,d4] = [ [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]] ]
        [d5,d6,d7,d8] = [ [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]] ]
        [d9,d10] = [ [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]] ]
        gdr_c = [ [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]],
        [[],[],[],[],[],[],[]], [[],[],[],[],[],[],[]]]
    elif nmol == 8:
        [new_m, new_xyz, tab_trajec] = [ [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]] ]
        [mass_m, mass_a, dt, time] = [ [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]] ]
        [x,y,z, dmass] = [ [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]] ]
        [coordinate,mass,natom,charge] = [ [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]] ]
        [data,xyz,df,c] = [ [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]] ]
        [d1,d2,d3,d4] = [ [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]] ]
        [d5,d6,d7,d8] = [ [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]] ]
        [d9,d10] = [ [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]] ]
        gdr_c = [ [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]] , [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[]] ,
        [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]]  ]
    elif nmol == 9:
        [new_m, new_xyz, tab_trajec] = [ [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]] ]
        [mass_m, mass_a, dt, time] = [ [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]] ]
        [x,y,z, dmass] = [ [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]] ]
        [coordinate,mass,natom,charge] = [ [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]] ]
        [data,xyz,df,c] = [ [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]] ]
        [d1,d2,d3,d4] = [ [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]] ]
        [d5,d6,d7,d8] = [ [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]] ]
        [d9,d10] = [ [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]] ]
        gdr_c = [ [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]],
        [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]],
        [[],[],[],[],[],[],[],[],[],[]] ]
    elif nmol == 10:
        [new_m, new_xyz, tab_trajec] = [ [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]] ]
        [mass_m, mass_a, dt] = [ [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]]  ]
        [x,y,z] = [ [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]]  ]
        [coordinate,mass,natom] = [ [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]]  ]
        [data,xyz,df] = [ [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]]  ]
        [d1,d2,d3] = [ [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]]  ]
        [d4,c,charge] = [ [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]]  ]
        [d5,d6,d7] = [ [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]]  ]
        [d8,d9,d10] = [ [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]]  ]
        [dmass, time] = [ [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]] ]
        gdr_c = [ [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]],
        [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]],
        [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]]]
    elif nmol == 11:
        [new_m, new_xyz, tab_trajec] = [ [[],[],[],[],[],[],[],[],[],[], []], [[],[],[],[],[],[],[],[],[],[], []], [[],[],[],[],[],[],[],[],[],[], []] ]
        [mass_m, mass_a, dt] = [ [[],[],[],[],[],[],[],[],[],[], []], [[],[],[],[],[],[],[],[],[],[], []], [[],[],[],[],[],[],[],[],[],[], []] ]
        [x,y,z] = [ [[],[],[],[],[],[],[],[],[],[], []], [[],[],[],[],[],[],[],[],[],[], []], [[],[],[],[],[],[],[],[],[],[], []] ]
        [coordinate,mass,natom] = [ [[],[],[],[],[],[],[],[],[],[], []], [[],[],[],[],[],[],[],[],[],[], []], [[],[],[],[],[],[],[],[],[],[], []] ]
        [data,xyz,df] = [ [[],[],[],[],[],[],[],[],[],[], []], [[],[],[],[],[],[],[],[],[],[], []], [[],[],[],[],[],[],[],[],[],[], []] ]
        [d1,d2,d3] = [ [[],[],[],[],[],[],[],[],[],[], []], [[],[],[],[],[],[],[],[],[],[], []], [[],[],[],[],[],[],[],[],[],[], []] ]
        [d4,c,charge] = [ [[],[],[],[],[],[],[],[],[],[], []], [[],[],[],[],[],[],[],[],[],[], []], [[],[],[],[],[],[],[],[],[],[], []] ]
        [d5,d6,d7] = [ [[],[],[],[],[],[],[],[],[],[], []], [[],[],[],[],[],[],[],[],[],[], []], [[],[],[],[],[],[],[],[],[],[], []] ]
        [d8,d9,d10] = [ [[],[],[],[],[],[],[],[],[],[], []], [[],[],[],[],[],[],[],[],[],[], []], [[],[],[],[],[],[],[],[],[],[], []] ]
        [dmass, time] = [ [[],[],[],[],[],[],[],[],[],[], []], [[],[],[],[],[],[],[],[],[],[], []] ]
    elif nmol == 12:
        [new_m, new_xyz, tab_trajec] = [ [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[], [],[]] ]
        [mass_m, mass_a, dt] = [ [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[], [],[]] ]
        [x,y,z] = [ [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[], [],[]] ]
        [coordinate,mass,natom] = [ [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[], [],[]] ]
        [data,xyz,df] = [ [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[], [],[]] ]
        [d1,d2,d3] = [ [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[], [],[]] ]
        [d4,c,charge] = [ [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[], [],[]] ]
        [d5,d6,d7] = [ [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[], [],[]] ]
        [d8,d9,d10] = [ [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[], [],[]] ]
        [dmass, time] = [ [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[]] ]
    elif nmol == 13:
        [new_m, new_xyz, tab_trajec] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[], [],[],[]] ]
        [mass_m, mass_a, dt] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[], [],[],[]] ]
        [x,y,z] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[], [],[],[]] ]
        [coordinate,mass,natom] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[], [],[],[]] ]
        [data,xyz,df] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[], [],[],[]] ]
        [d1,d2,d3] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[], [],[],[]] ]
        [d4,c,charge] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[], [],[],[]] ]
        [d5,d6,d7] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[], [],[],[]] ]
        [d8,d9,d10] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[], [],[],[]] ]
        [dmass, time] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
    elif nmol == 14:
        [new_m, new_xyz, tab_trajec] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[], [],[],[]] ]
        [mass_m, mass_a, dt] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[], [],[],[]] ]
        [x,y,z] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[], [],[],[]] ]
        [coordinate,mass,natom] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[], [],[],[]] ]
        [data,xyz,df] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[], [],[],[]] ]
        [d1,d2,d3] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[], [],[],[]] ]
        [d4,c,charge] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[], [],[],[]] ]
        [d5,d6,d7] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[], [],[],[]] ]
        [d8,d9,d10] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[], [],[],[]] ]
        [dmass, time] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
    elif nmol == 15:
        [new_m, new_xyz, tab_trajec] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[], [],[],[],[]] ]
        [mass_m, mass_a, dt] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[], [],[],[],[]] ]
        [x,y,z] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[], [],[],[],[]] ]
        [coordinate,mass,natom] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[], [],[],[],[]] ]
        [data,xyz,df] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[], [],[],[],[]] ]
        [d1,d2,d3] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[], [],[],[],[]] ]
        [d4,c,charge] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[], [],[],[],[]] ]
        [d5,d6,d7] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[], [],[],[],[]] ]
        [d8,d9,d10] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[], [],[],[],[]] ]
        [dmass, time] = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
    else:
        @decor
        def print_error():
            print('InputError 😊')
            print("sorry nmol higher is than 15 please make a choice in the list below")
            print(list(range(15)))
            print("Put the good value and try again ")
        exit()

def param_atom_atom(gamma : Iterable[int] = None):
    if gamma == 1:
        gdr_aa = [[]]
    elif  gamma == 2:
        gdr_aa = [[],[]]
    elif  gamma == 3:
        gdr_aa = [[],[],[]]
    elif  gamma == 4:
        gdr_aa = [[],[],[],[]]
    elif  gamma == 5:
        gdr_aa = [[],[],[],[],[]]
    elif  gamma == 6:
        gdr_aa = [[],[],[],[],[],[]]
    elif  gamma == 7:
        gdr_aa = [[],[],[],[],[],[],[]]
    elif  gamma == 8:
        gdr_aa = [[],[],[],[],[],[],[],[]]
    elif  gamma == 9:
        gdr_aa = [[],[],[],[],[],[],[],[],[]]
    elif  gamma == 10:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 11:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 12:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 13:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 14:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 15:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 16:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 17:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 18:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 19:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 20:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 21:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 22:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 23:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 24:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 25:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 26:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 27:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 28:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 29:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    elif  gamma == 30:
        gdr_aa = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    else:
        print('InputError 😊')
        print('gamme not in [1:30]')
        print('PUt the good value and try again')
        exit()
    return gdr_aa 
    
def params_control():
    return [coordinate,mass,natom,charge,data]
def params_gdr():
    return [xyz, df, dmass]
def params_gdr1():
    return [d1,d2,d3,d4,d5,d6,d7,d8,d9,d10]
def params_DF():
    return df 
def params_XYZ():
    return [x,y,z]
def params_tab():
    return [new_m, new_xyz, tab_trajec]
def params_mass():
    return [mass_m, mass_a]
def scale_init():
    return [d9, d10]
def params_data():
    return dt 
def param_time():
    return time 
def gdr_c():
    return gdr_c
def new_array1():
    return [dx, dy, dz]
def new_array2():
    return [dxx, dyy, dzz]
def new_array3():
    return [dxxx, dyyy, dzzz]