# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 18:26:51 2014

@author: David
"""

import numpy as np;

#Initialize system
N_PARTICLES = 216;
mp = 18/1000.0;  #particle mass in kg/mol
dt = 1e-6;  #timestep in ns
nstep = 10000;  #number of simulation steps

#for lennard-jones potential - taken from TIP4P-EW paper
e_lj = .16275*4184; #(J/mol)
sigma_lj = 3.16435/10;  #nanometers
sigma_lj12 = sigma_lj**12;
sigma_lj6 = sigma_lj**6;

xbox = 2.5; #box dimensions in nanometers
ybox = 2.5;
zbox = 2.5;

x = np.array([0.0]*N_PARTICLES);  #positions in nm
y = np.array([0.0]*N_PARTICLES);
z = np.array([0.0]*N_PARTICLES);

vx = np.array([0.0]*N_PARTICLES);  #velocities in nm / ns
vy = np.array([0.0]*N_PARTICLES);
vz = np.array([0.0]*N_PARTICLES);

dudx = np.array([0.0]*N_PARTICLES);
dudy = np.array([0.0]*N_PARTICLES);
dudz = np.array([0.0]*N_PARTICLES);

T = int(np.round(N_PARTICLES**(1/3.0)));
for i in range(0,T):
    for j in range(0,T):
        for k in range(0,T):
            index = i*T*T + j*T + k;
            x[index] = float(xbox)/T*(i+1);
            y[index] = float(ybox)/T*(j+1);
            z[index] = float(zbox)/T*(k+1);

for i in range(0,N_PARTICLES):
    vx[i] = np.random.uniform(-1,1)*0;
    vy[i] = np.random.uniform(-1,1)*0;
    vz[i] = np.random.uniform(-1,1)*0;



scatter(x,y)
hold(False);

for i in range(0,nstep):
    
    for p in range(0,N_PARTICLES):
        #compute distance
        dx = x - x[p];
        dy = y - y[p];
        dz = z - z[p];
        
        R = np.sqrt(dx**2 + dy**2 + dz**2);
        
        R[p] = 1;#no divide by zero error        
        
        R_factor = 4*e_lj*(-12*sigma_lj12/R**14 + 6*sigma_lj6/R**8);
                
        #compute energy derivatives
        R_factor[p] = 0;#No self interaction
        dudx[p] = np.sum(R_factor * dx);
        dudy[p] = np.sum(R_factor*dy);
        dudz[p] = np.sum(R_factor*dz);
    
    #update positions / velocities
    x = x + vx*dt;
    y = y + vy*dt;
    z = z + vz*dt;
    
    #dudx = kcal/nm    
    
    vx = vx + dudx/mp*dt  #J/kg/(nm/ns) = m/s = nm/ns
    vy = vy + dudy/mp*dt
    vz = vz + dudz/mp*dt
    if(i%10 == 0):        
        scatter(x,y)
        pause(.01);
        
    print i
    
    
