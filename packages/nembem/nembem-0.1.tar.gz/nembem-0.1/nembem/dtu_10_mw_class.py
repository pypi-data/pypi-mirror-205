# %% Init section
# Loading packages

import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess
from scipy.interpolate import interp2d

# Defining the dtu 10 MW turbine class

class DtuTurbine:

    def __init__(self, L_s=7.1, R=89.17, B=3, H=119,
                 V_rated=11.4,
                 P_rated=10.64*10**6,
                 airfoil_data='input/bladedat.txt'):
        self.L_s = L_s # Length of shaft in m
        self.R = R # Turbine radius in m
        self.B = B # Number of blades
        self.A = self.get_area() # Calculating the area of the turbine rotor
        self.H = H # Hub height in m
        self.V_rated = V_rated # Rated wind speed in m/s
        self.P_rated = P_rated # Rated power in W

        # Loading the airfoil data
        # Columns: r [m], beta [deg], c [m], tc [-]
        self.airfoil_data = np.loadtxt(airfoil_data)

        # Unpacking the airfoil data
        self.r, self.beta_deg, self.c, self.tc = self.airfoil_data.T     

    # Note: Remember to use this area
    def get_area(self):
        """Calculates the area of the turbine rotor.

        Returns:
            float: area of the turbine rotor in m (assuming R is in m).
        """
        area = np.pi * self.R**2
        return area


    def visualize_turbine(self):

        """Visualizes the turbine i.e. the tower and the blades. The plot
        shows the hub height and the radius of the turbine. The plot also show how
        the blade elements are distributed along the blade.
        """

        plt.figure()
        ax = plt.axes()
        
        ax.set_title('Wind turbine dimensions')

        # Turbine tower
        plt.plot([0, 0], [0, self.H], color='white', linewidth=3)
        
        # kwargs for the airfoils/blades
        airfoil_kwargs = {'color': 'white',
                          'linewidth': 3,
                          'marker': 'o',
                          'markeredgecolor':'black'
                          }

        # First turbine blade
        plt.plot(np.zeros(self.r.shape),
                    self.r + self.H, **airfoil_kwargs)
        
        # Second turbine blade
        plt.plot(self.r * np.sin(2*np.pi/3),
                    self.r * np.cos(2*np.pi/3) + self.H, **airfoil_kwargs)
        
        # Adding hub and radius visualizations
        plt.plot([0, 0], [0, self.H],
                 color='black', linestyle='--', label=f'Hub height = {self.H:.1f} m')
        
        plt.plot([0, 0], [self.H, self.H + self.R],
                 color='red', linestyle='--', label=f'Radius = {self.R:.1f} m')
        
        # Third turbine blade
        plt.plot(self.r * np.sin(4*np.pi/3),
                    self.r * np.cos(4*np.pi/3) + self.H, **airfoil_kwargs)

        # Adding background image
        check_path = os.path.exists('input/sky.jpg')
        
        # If the path exists, add the image
        if check_path:
            img = plt.imread('input/sky.jpg')
            ax.imshow(img, extent=[-self.R, self.R, 0, self.H + self.R])
        
        # If the path does not exist, set the background color to cornflowerblue
        else:
            ax.set_facecolor('cornflowerblue')
        
        # Adding legend
        plt.legend()
        
        # Scaling, labels and limits
        plt.xlabel('Width [m]')
        plt.ylabel('Height [m]')
        plt.axis('scaled')
        plt.ylim(0)

        plt.show()


    def plot_airfoil_data(self):

        """Plots the airfoil data"""

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

        fig.suptitle('Airfoil data')

        # Plot the data
        ax1.plot(self.r, self.beta_deg)
        ax1.set(ylabel='beta [deg]')
        ax2.plot(self.r, self.c)
        ax2.set(ylabel='c [m]')
        ax3.plot(self.r, self.tc)
        ax3.set(ylabel='tc [-]')

        # Set the x-axis limits and label
        ax3.set(xlabel='r [m]', xlim=(self.r[0], self.r[-1]))

        # Layout
        fig.align_ylabels((ax1, ax2, ax3))
        fig.tight_layout()

        # Add grid
        ax1.grid()
        ax2.grid()
        ax3.grid()

        fig.show()

#%% BEM section

    def bem(self, windspeed=9, theta_p = 0):

        # Based on Aerodynamics of Wind Turbines by Hansen (2015).
        
        # Note: Boolean for using the pitch controller (temporary)
        use_pitch_controller = True
        use_stall = True
        use_dwf = True
        
        """Parameters"""
        V_0 = windspeed # m/s
        timerange = 500 # s
        theta_cone = 0 # rad
        theta_yaw = 0 # rad
        theta_tilt = 0 # rad
        lam_opt = 8 # Optimal tip speed ratio
        C_p_opt = 0.47 # Optimal power coefficient
        rho = 1.225 # kg/m^3
        k_dwf = 0.6 # Dynamic wake filter constant
        
        # Roughness length
        z_0 = 0.9 # m
        # z_0 = 0 # m
        
        # If the roughness length is larger than zero,
        # turbulence is included in the calculations.
        if z_0 > 0:
            # Defining dimensions of the turbulence box
            n1, n2, n3 = 4096, 32, 32
            Lx, Ly, Lz = 6142.5, 180, 180
            
            # Writing turbulence input file
            write_mann_input(n1, n2, n3, Lx, Ly, Lz, self.H, z_0, V_0)
            
            # Run turbulence simulation
            subprocess.run(['input/turbulence/windsimu.exe',
                             'input/turbulence/inputEx3.INP'])
            
            # Load turbulence data
            turb = load_turb_box('input/turbulence/sim1.bin')
            
            # Reshape turbulence data to fit the relevant dimensions
            turb = np.reshape(turb, (n1, n2, n3))
            
            print(turb[0, 0, 0:10])
            
            # Defining the delta values (spacing between points)
            delta_y = Ly/(n2-1)
            delta_x = Lx/(n1-1)
            delta_z = Lz/(n3-1)
            delta_t = delta_x/V_0
            
            # Changing dimensions from box to physical dimensions
            # x corresponds to z (time)
            # z corresponds to x
            # y corresponds to y
            X_turb = np.arange(0, n2)*delta_z + (self.H - (n2-1)*delta_z/2) # Height
            Y_turb = np.arange(0, n3)*delta_y - ((n3-1) * delta_y)/2 # Width
            Z_turb = np.arange(0, n1)*delta_x # Depth (Time)
            
        else:
            delta_t = 0.1 # s
        
        
        # Constant for calculating M_g (Generator torque)
        K = 0.5 * rho*self.A * self.R**3 * (C_p_opt/lam_opt**3)
        
        # Rated omega
        omega_rated = (self.P_rated/K)**(1/3)
        
        # If the wind speed is below rated, use omega corresponding
        # to optiamal tip speed ration. Otherwise, use rated omega.
        if windspeed <= self.V_rated:
            omega = (lam_opt*V_0)/self.R
        else:
            omega = omega_rated
        
        # Reference angular velocity for PI controller
        omega_ref = 1.01 # from DTU course 46310: "Wind Turbine Aeroelasticity"
        
        # Controller parameters
        K1 = np.deg2rad(14) # rad
        K_I = 0.64 # no unit
        K_P = 1.5 # s
        
        # Controller limits
        theta_p_max_ang = np.deg2rad(45) # rad, max pitch angle
        theta_p_min_ang = 0 # rad, min pitch angle
        theta_p_max_vel = np.deg2rad(9) # rad/s, max pitch angle velocity
        
        # Rotor moment of inertia
        I_rotor = 1.6 * 10**8 # kg*m^2
               
        """Initialization"""
        # Time array
        time_arr = np.zeros([timerange])
        
        if use_pitch_controller:
            # Angular velocity changing in time
            omega_arr = np.zeros([timerange])
            omega_arr[0] = omega
        else: 
            # Angular velocity constant (steady BEM)
            omega_arr = np.full(timerange, omega)
        
        # Blade azumithal position: 2D array (blade number, time)
        theta_blade_arr = np.zeros([self.B, timerange])
        theta_blade_arr[1, 0] = 2*np.pi/3
        theta_blade_arr[2, 0] = 4*np.pi/3
        
        # Blade element positions (airfoil number, blade number, time)
        x1_arr = np.zeros([len(self.r), self.B, timerange])
        y1_arr = np.zeros(x1_arr.shape)
        z1_arr = np.zeros(x1_arr.shape)

        # Wind speed array
        # assuming: constant wind speed andd only wind in the z-direction
        V0_array = np.array([0, 0, V_0])
        
        # Saving wind speeds in the x, y and z directions
        # for each blade element, blade and time step
        V0x_arr = np.zeros([len(self.r), self.B, timerange])
        V0y_arr = np.zeros(V0x_arr.shape)
        V0z_arr = np.zeros(V0x_arr.shape)
        
        # Relative wind speeds (only y and z directions)
        # wind speed in x-direction is assumed to be zero
        V_rel_y_arr = np.zeros([len(self.r), self.B, timerange])
        V_rel_z_arr = np.zeros(V_rel_y_arr.shape)
        
        # Similarly for the induced wind
        Wy_arr = np.zeros([len(self.r), self.B, timerange])
        Wz_arr = np.zeros(Wy_arr.shape)
        
        # Quasi-steady induced velocities
        Wy_qs_arr = np.zeros([len(self.r), self.B, timerange])
        Wz_qs_arr = np.zeros(Wy_qs_arr.shape)
        
        # Note: induced wind for dwf
        Wy_int_arr = np.zeros([len(self.r), self.B, timerange])
        Wz_int_arr = np.zeros(Wy_int_arr.shape)
        
        # Lift coefficients
        cl_arr = np.zeros([len(self.r), self.B, timerange])
        
        # Seperation function
        fs_arr = np.zeros(cl_arr.shape)
        
        # Tangential and normal loads
        pt_arr = np.zeros([len(self.r), self.B, timerange])
        pn_arr = np.zeros(pt_arr.shape)
        
        # Thrust and power
        T_arr = np.zeros([timerange])
        P_arr = np.zeros(T_arr.shape)
        
        # Blade pitch angle
        theta_p_arr = np.zeros(timerange)
        
        # PI controller array
        theta_p_i_arr = np.zeros(timerange)
        
        # Cut in and cut out wind speed
        ws_cut_in = 4 #m/s
        ws_cut_out = 25 #m/s
        
        # Cut in and cut out wind speed
        if not ws_cut_in <= V_0 <= ws_cut_out:
            raise ValueError('Wind speed is outside the cut in and cut out speed')
        
        # Note: this can be removed when PI controller is implemented
        elif self.V_rated < V_0:
            pass
            # raise ValueError('Not implemented yet')
            # print('Maximum power output because wind speed is higher than rated wind speed')
            # return time_arr, pt_arr, pn_arr, P_arr, T_arr
        
        """Transformation matrices"""
        
        # Transformation matrix: yaw, tilt, roll (system 1 to 2)
        a12 = tm_yaw_tilt_roll(theta_yaw, theta_tilt)
        
        # Transformation matrix: yaw, tilt, roll (system 2 to 1)
        a21 = np.transpose(a12)
        
        # Transformation matrix: cone (system 3 to 4)
        a34 = np.array([[np.cos(theta_cone), 0, -np.sin(theta_cone)],
                        [0, 1, 0],
                        [np.sin(theta_cone), 0, np.cos(theta_cone)]])
        
        # Height of the hub
        rt1 = np.array([self.H, 0, 0])
        
        # Length of the shaft
        rs1 = a21 @ np.array([0, 0, -self.L_s])

        # Loading force coefficients
        (aoa_tab, cl_stat_tab, cd_stat_tab,
        cm_stat_tab, f_stat_tab, cl_inv_tab,
        cl_fs_tab) = load_force_coeff_files()
        
        """"BEM code (nested loop): time, blade, blade element"""
        
        for n in range(1, timerange):
            """Time loop"""
            
            time_arr[n] = n*delta_t
            
            # If turbulent box is used
            if z_0 > 0:
                        
                # The turbulent box has time as the first coordinate
                # and not as the last coordinate as we usually do
                f2d = interp2d(X_turb, Y_turb, turb[n, :, :], kind='linear')
            
            for i in range(self.B):
                """Blade loop"""   
                
                # Rotating the blades
                theta_blade_arr[i, n] = rotate_blades(i, n, theta_blade_arr, omega_arr, delta_t)
                
                # Transformation matrix: system 2 to system 3
                a23 = np.array([[np.cos(theta_blade_arr[i, n]), np.sin(theta_blade_arr[i, n]), 0],
                                [-np.sin(theta_blade_arr[i, n]), np.cos(theta_blade_arr[i, n]), 0],
                                [0, 0, 1]])

                # Transformation matrix: system 1 to system 4
                a14 = a34 @ a23 @ a12
                
                # Transformation matrix: system 4 to system 1
                a41 = np.transpose(a14)
                
                for k in range(len(self.r)):
                    """Airfoil loop"""
                    
                    # Blade element position in system 1
                    rb1 = a41 @ np.array([self.r[k], 0, 0])
                    
                    # Coordinates based on hub height, shaft length and blade element position
                    r1 = rt1 + rs1 + rb1
                    
                    # Saving the coordinates
                    x1_arr[k, i, n] = r1[0]
                    y1_arr[k, i, n] = r1[1]
                    z1_arr[k, i, n] = r1[2]
                    
                    # If turbulent box is used
                    if z_0 > 0:
                        turb_interp = f2d([x1_arr[k, i, n]],[y1_arr[k, i, n]])[0]
                        
                        V0_array = np.array([0, 0, turb_interp + V_0])
                        
                    else:
                        V0_array = np.array([0, 0, V_0])
                    
                    # Wind speed transformed to system 4
                    V0_4 = a14 @ V0_array
                    
                    # Saving the wind speeds in system 4
                    V0x_arr[k, i, n] = V0_4[0]
                    V0y_arr[k, i, n] = V0_4[1]
                    V0z_arr[k, i, n] = V0_4[2]
                    
                    # Relative wind speeds in system 4
                    V_rel_y_arr[k, i, n] = V0y_arr[k, i, n] + Wy_arr[k, i, n-1] - omega_arr[n-1] * self.r[k] * np.cos(theta_cone)
                    V_rel_z_arr[k, i, n] = V0z_arr[k, i, n] + Wz_arr[k, i, n-1]
                    
                    # Flow angle [rad]
                    phi = np.arctan(V_rel_z_arr[k, i, n]/(-V_rel_y_arr[k, i, n]))
                    
                    # Angle of attack [deg]
                    if use_pitch_controller:
                        # With PI controller
                        aoa_deg = np.rad2deg(phi) - (self.beta_deg[k] + np.rad2deg(theta_p_arr[n-1]))
                    else:
                        # Without PI controller
                        aoa_deg = np.rad2deg(phi) - (self.beta_deg[k] + np.rad2deg(theta_p))
                    
                    # Force coefficients                    
                    (cl, cd,
                     cm, f_stat,
                     cl_inv, cl_fs) = interp_force_coeffs(aoa_deg, self.tc[k],
                                                        aoa_tab, cl_stat_tab,
                                                        cd_stat_tab, cm_stat_tab,
                                                        f_stat_tab, cl_inv_tab,
                                                        cl_fs_tab)
                    
                    # Absolute relative wind speed
                    V_rel_abs = np.sqrt(V_rel_y_arr[k, i, n]**2 + V_rel_z_arr[k, i, n]**2)
                    
                    # Dynamic stall model
                    if use_stall:
                        tau_stall = 4 * self.c[k] / V_rel_abs
                
                        fs_arr[k, i, n] = f_stat + (fs_arr[k, i, n-1]-f_stat) * np.exp(-delta_t/tau_stall)

                        # Saving the lift coefficients
                        cl_arr[k, i, n] = f_stat * cl_inv + (1-fs_arr[k, i, n]) * cl_fs
            
                    else:
                        # Saving the lift coefficients
                        cl_arr[k, i, n] = cl
                    
                    # Glauert correction
                    a = -Wz_arr[k, i, n-1]/V_0
                    
                    if a <= 0.33:
                        f_g = 1
                    else:
                        f_g = 0.25*(5-3*a)
                    
                    # Calculating the term abs(V0 + f_g * Wn) for the quasi-steady induced wind
                    V_f_W = np.sqrt(V0y_arr[k, i, n]**2 + (V0z_arr[k, i, n] + f_g * Wz_arr[k, i, n-1])**2)
                    
                    # Lift and drag forces
                    l = 0.5 * rho * V_rel_abs**2 * self.c[k] * cl_arr[k, i, n]
                    d = 0.5 * rho * V_rel_abs**2 * self.c[k] * cd
                   
                   # Setting the tangential and normal loads to zero at the tip
                    if k==len(self.r)-1:
                        p_z=0
                        p_y=0
                    else:
                    # Calculating the tangential and normal loads
                        p_z = l * np.cos(phi) + d * np.sin(phi)      
                        p_y = l * np.sin(phi) - d * np.cos(phi)
                    
                    # Saving the tangential and normal loads                                
                    pt_arr[k, i, n] = p_y
                    pn_arr[k, i, n] = p_z
                    
                    # Prandtl tip loss correction
                    # F is set to 1 if the flow angle is too small
                    # or the blade element is too close to the tip
                    if np.sin(abs(phi)) <= 0.01 or self.R-self.r[k] <= 0.005:
                        F = 1
                    else:
                        F = (2/np.pi) * np.arccos(np.exp(-(self.B/2) * ((self.R-self.r[k])/(self.r[k] * np.sin(abs(phi))))))
                    
                    # Calculating the quasi-steady induced velocities
                    Wz_qs_arr[k, i, n] = (-self.B * l * np.cos(phi))/(4 * np.pi * rho * self.r[k] * F * V_f_W)
                    Wy_qs_arr[k, i, n] = (-self.B * l * np.sin(phi))/(4 * np.pi * rho * self.r[k] * F * V_f_W)
                    
                    # Dynamic wake filter
                    if use_dwf:
                        tau_1 = 1.1/(1 - 1.3*a) * self.R/V_0
                        tau_2 = (0.39 - 0.26 * (self.r[k]/self.R)**2)*tau_1
                        
                        Hy_dwf = Wy_qs_arr[k, i, n] + k_dwf * tau_1 * (Wy_qs_arr[k, i, n] - Wy_qs_arr[k, i, n-1])/delta_t
                        Hz_dwf = Wz_qs_arr[k, i, n] + k_dwf * tau_1 * (Wz_qs_arr[k, i, n] - Wz_qs_arr[k, i, n-1])/delta_t
                        
                        Wy_int_arr[k, i, n] = Hy_dwf + (Wy_int_arr[k, i, n-1] - Hy_dwf)*np.exp(-delta_t/tau_1)
                        Wz_int_arr[k, i, n] = Hz_dwf + (Wz_int_arr[k, i, n-1] - Hz_dwf)*np.exp(-delta_t/tau_1)
                        
                        Wy_arr[k, i, n] = Wy_int_arr[k, i, n] + (Wy_arr[k, i, n-1] - Wy_int_arr[k, i, n])*np.exp(-delta_t/tau_2)
                        Wz_arr[k, i, n] = Wz_int_arr[k, i, n] + (Wz_arr[k, i, n-1] - Wz_int_arr[k, i, n])*np.exp(-delta_t/tau_2)
                    
                    # Without dynamic wake filter
                    else:
                        # Saving the induced velocities which are equal to the quasi-steady
                        # induced velocities for the steady BEM
                        Wz_arr[k, i, n] = Wz_qs_arr[k, i, n]
                        Wy_arr[k, i, n] = Wy_qs_arr[k, i, n]
                    
            # Using trapetzoidal integration to calculate the rotor moment
            M_r = np.trapz(np.sum(pt_arr,axis=1)[:, n]*self.r, self.r)
            
            # Calculating and saving the rotor power
            # based on the rotor moment and the angular velocity
            P_arr[n] = omega_arr[n-1]*M_r

            # Calculating and saving the rotor thrust
            T = np.trapz(np.sum(pn_arr,axis=1)[:,n], self.r)
            T_arr[n] = T

            if use_pitch_controller:
                        
                #Region 1
                if omega_arr[n-1] < omega_ref: 
                    #update omega
                    M_g = K * omega_arr[n-1]**2
                    
                # Region 2+3
                else:
                    #update omega 
                    # M_g = M_g_max
                    M_g = 1.0545* 10**7
                
                #update theta_pitch
                GK = (1/ (1 + (theta_p_arr[n-1]/K1)))
                theta_p_p = GK * K_P * ( omega_arr[n-1] -omega_ref)
                theta_p_i_arr[n] = theta_p_i_arr[n-1] + GK * K_I * (omega_arr[n-1]-omega_ref) * delta_t
                
                #limit på theta_p_I angle
                if theta_p_i_arr[n] > theta_p_max_ang:
                    theta_p_i_arr[n] = theta_p_max_ang
                elif theta_p_i_arr[n] < theta_p_min_ang:
                    theta_p_i_arr[n] = theta_p_min_ang
                
                theta_p_arr[n] = theta_p_p + theta_p_i_arr[n]
                
                #hvis theta_p skal ændres hurtigere end den må (stigende i grader)
                if (theta_p_arr[n] > theta_p_arr[n-1] + theta_p_max_vel * delta_t):
                    theta_p_arr[n] = theta_p_arr[n-1] + theta_p_max_vel * delta_t
                    
                #hvis theta_p skal ændres hurtigere end den må (falende i grader)
                elif (theta_p_arr[n] < theta_p_arr[n-1] - theta_p_max_vel * delta_t):
                    theta_p_arr[n] = theta_p_arr[n-1] - theta_p_max_vel * delta_t
                    
                #theta_p må max være = theta_p_max_ang
                if (theta_p_arr[n] > theta_p_max_ang):
                    theta_p_arr[n] = theta_p_max_ang

                #theta_p må min være = theta_p_min_ang
                elif (theta_p_arr[n] < theta_p_min_ang):
                    theta_p_arr[n] = theta_p_min_ang
                    
                #update omega
                omega_arr[n] = omega_arr[n-1] + ((M_r - M_g)/ I_rotor) * delta_t
            
        # Returning the time array, loads, power and thrust
        return time_arr, pt_arr, pn_arr, P_arr, T_arr


def tm_yaw_tilt_roll(theta_yaw, theta_tilt):
    
    """Transformation matrix for yaw, tilt and roll.
    Used to transform coordinates from system 1 to system 2.

    Parameters
    ----------
    theta_yaw : float
        Yaw angle of the turbine in radians.
    theta_tilt : float
        Tilt angle of the turbine nacelle in radians. 
    
    Returns
    -------
    ndarray
        Returns the transformation matrix.
    """
    
    # Yaw
    a1 = np.array([[1, 0, 0],
                [0, np.cos(theta_yaw), np.sin(theta_yaw)],
                [0, -np.sin(theta_yaw), np.cos(theta_yaw)]])
    
    # Tilt
    a2 = np.array([[np.cos(theta_tilt), 0, -np.sin(theta_tilt)],
                [0,1,0],
                [np.sin(theta_tilt),0, np.cos(theta_tilt)]])
    
    # Roll: assuming no roll
    a3 = np.array([[1,0,0],
                [0,1,0],
                [0,0,1]])
    
    return a3@a2@a1

def rotate_blades(i, n, theta_blade_arr, omega_arr, delta_t): 
    
    """Rotates the blades according to the angular velocity of the rotor.

    Parameters
    ----------
    i : int
        Blade number.
    n : int
        Current time.
    theta_blade_arr : ndarray
        Azimuthal position of the blades.
    omega_arr : ndarray
        Angular velocity of the rotor.
    delta_t : float
        Time step.
    
    Returns
    -------
    theta_blade : float
        The new azimuthal position of the blade.
    """
    
    # Blade 1
    if i == 0:
        theta_blade = theta_blade_arr[0, n-1] + omega_arr[n-1] * delta_t
    
    # Blade 2
    elif i == 1:
        theta_blade = theta_blade_arr[0, n] + omega_arr[n-1] * delta_t + 0.666 * np.pi
    
    # Blade 3
    elif i == 2:
        theta_blade = theta_blade_arr[0, n] + omega_arr[n-1] * delta_t + 1.333 * np.pi
        
    return theta_blade

def load_force_coeff_files():
        
    """Creates arrays with the force coefficients for the airfoils.

    Returns
    -------
    aoa_tab : ndarray
        1D array which contains angle of attack.
    cl_stat_tab : ndarray
        2D array which contains the lift coefficient for the airfoils.
        Rows correspond to angle of attack and columns correspond to different
        ratios of thickness to chord length (rows: aoa, columns: tc).
    cd_stat_tab : ndarray
        2D array which contains the drag coefficient for the airfoils.
        Rows: aoa, columns: tc
    cm_stat_tab : ndarray
        2D array which contains the momentum coefficient for the airfoils.
        Rows: aoa, columns: tc
    f_stat_tab : ndarray
        2D array which contains the data for the seperation function for the airfoils.
        Rows: aoa, columns: tc
    cl_inv_tab : ndarray
        2D array which contains the lift coefficient for the inviscid flow.
        Rows: aoa, columns: tc
    cl_fs_tab : ndarray
        2D array which contains the the lift coefficient for fully separated flow.
        Rows: aoa, columns: tc
    """    
    
    # Thickness divided by chord length for the airfoils
    tcs = [241, 301, 360, 480, 600]
    
    # Creating a list of the files
    files = [f'input/FFA-W3-{tc}.txt' for tc in tcs]
    
    # Adding the cylinder file (root of the blades)
    files.append('input/cylinder.txt')
    
    # Loading one file to get the length of the file which is used for
    # initialization of the force coeff tables
    first_airfoil = np.loadtxt(files[0])
    
    # Creating tables for the force coefficients
    cl_stat_tab = np.zeros([len(first_airfoil), len(files)])
    cd_stat_tab = np.zeros(cl_stat_tab.shape)
    cm_stat_tab = np.zeros(cl_stat_tab.shape)
    f_stat_tab = np.zeros(cl_stat_tab.shape)
    cl_inv_tab = np.zeros(cl_stat_tab.shape)
    cl_fs_tab = np.zeros(cl_stat_tab.shape)
    
    # Loading the files
    for i, f in enumerate(files):
        (aoa_tab, cl_stat_tab[:, i], cd_stat_tab[:, i], cm_stat_tab[:,i],
        f_stat_tab[:, i], cl_inv_tab[:, i], cl_fs_tab[:, i]) = np.loadtxt(f, skiprows=0).T
    
    return (aoa_tab, cl_stat_tab, cd_stat_tab,
            cm_stat_tab, f_stat_tab, cl_inv_tab, cl_fs_tab)


def interp_force_coeffs(angle_of_attack, thick, aoa_tab, cl_tab,
                      cd_tab, cm_tab,  f_stat_tab, cl_inv_tab,
                      cl_fs_tab): 
    
    """Interpolates the force coefficients for the airfoils based on angle of attack
    and thickness divided by chord length.

    Parameters
    ----------
    angle_of_attack : float
        Current angle of attack.
    thick : float
        Current thickness divided by chord length.
    aoa_tab : ndarray
        1D array which contains angle of attack.
    cl_stat_tab : ndarray
        2D array which contains the lift coefficient for the airfoils.
        Rows correspond to angle of attack and columns correspond to different
        ratios of thickness to chord length (rows: aoa, columns: tc).
    cd_stat_tab : ndarray
        2D array which contains the drag coefficient for the airfoils.
        Rows: aoa, columns: tc
    cm_stat_tab : ndarray
        2D array which contains the momentum coefficient for the airfoils.
        Rows: aoa, columns: tc
    f_stat_tab : ndarray
        2D array which contains the data for the seperation function for the airfoils.
        Rows: aoa, columns: tc
    cl_inv_tab : ndarray
        2D array which contains the lift coefficient for the inviscid flow.
        Rows: aoa, columns: tc
    cl_fs_tab : ndarray
        2D array which contains the the lift coefficient for fully separated flow.
        Rows: aoa, columns: tc

    Returns
    -------
    cl : float
        Interpolated lift coefficient.
    cd : float
        Interpolated drag coefficient.
    cm : float
        Interpolated momentum coefficient.
    f_stat : float
        Interpolated seperation function.
    cl_inv : float
        Interpolated lift coefficient for inviscid flow.
    cl_fs : float
        Interpolated lift coefficient for fully separated flow.
    """
    
    # Defining thick profiles
    thick_prof = np.array([24.1, 30.1, 36.0, 48.0, 60.0, 100.0])
    
    # Initializing arrays
    cl_aoa =  np.zeros(len(thick_prof))
    cd_aoa =  np.zeros(cl_aoa.shape)
    cm_aoa =  np.zeros(cl_aoa.shape)
    f_stat_aoa = np.zeros(cl_aoa.shape)
    cl_inv_aoa = np.zeros(cl_aoa.shape)
    cl_fs_aoa = np.zeros(cl_aoa.shape)
    
    
    # Interpolating to current angle of attack:
    for i in range(np.size(thick_prof)):
        cl_aoa[i] =  np.interp(angle_of_attack, aoa_tab, cl_tab[:, i])
        cd_aoa[i] =  np.interp(angle_of_attack, aoa_tab, cd_tab[:, i])
        cm_aoa[i] =  np.interp(angle_of_attack, aoa_tab, cm_tab[:, i])
        f_stat_aoa[i] =  np.interp(angle_of_attack, aoa_tab, f_stat_tab[:, i])
        cl_inv_aoa[i] =  np.interp(angle_of_attack, aoa_tab, cl_inv_tab[:, i])
        cl_fs_aoa[i] =  np.interp(angle_of_attack, aoa_tab, cl_fs_tab[:, i])
    
    # Interpolating to current thickness:
    cl = np.interp(thick, thick_prof, cl_aoa)
    cd = np.interp(thick, thick_prof, cd_aoa)
    cm = np.interp(thick, thick_prof, cm_aoa)
    f_stat = np.interp(thick, thick_prof, f_stat_aoa)
    cl_inv = np.interp(thick, thick_prof, cl_inv_aoa)
    cl_fs = np.interp(thick, thick_prof, cl_fs_aoa)

    return cl, cd, cm, f_stat, cl_inv, cl_fs

def write_mann_input(n1, n2, n3, Lx, Ly, Lz, H, z_0, V_0):
    """Writes the input file for the Mann turbulence simulation.

    Parameters
    ----------
    n1 : int
        Number of spatial dimensions.
    n2 : int
        Number of velocity components.
    n3 : int
        Number of grid points in flow direction.
    H : float
        Hub height [m].
    z_0 : float
        Roughness length [m].
    V_0 : float
        Mean wind speed [m/s].
    """
    
    # Define input parameters to Mann turbulence simulation
    lines = ['3', # Number of spatial dimensions
            '3', # Number of velocity components
            str(n1), # Number of grid points in flow direction
            str(n2), # Number of grid points in horizontal direction
            str(n3), # Number of grid points in vertical direction
            str(Lx), # Physical length [m] in flow direction
            str(Ly), # Physical length [m] in horizontal direction
            str(Lz), # Physical length [m] in vertical direction
            'land', # Defines the spectre (in this case land)
            str(V_0), # Mean wind speed [m/s]
            str(H), # Hub height [m]
            str(z_0), # Roughness length [m]
            '0', # Spectrum type
            '-5', # Seed
            'sim1.bin', # Wind speed fluctuations in flow [m/s]
            'sim2.bin', # Wind speed fluctuations in horizontal [m/s]
            'sim3.bin'] # Wind speed fluctuations [m/s]

    # Write input parameters to file
    with open('input/turbulence/inputEx3.INP', 'w') as f:
        f.write('\n'.join(lines))
    
    return
    


def load_turb_box(filename, N=(32, 32)):
    """NB: We did NOT make this function, it was provided in DTU course 46310: "Wind Turbine Aeroelasticity".
    Load mann turbulence box.

    Parameters
    ----------
    filename : str
        Filename of turbulence box
    N : tuple, (ny,nz) or (nx,ny,nz)
        Number of grid points

    Returns
    -------
    turbulence_box : nd_array

    Examples
    --------
    >>> u = load('turb_u.dat')
    """
    data = np.fromfile(filename, np.dtype('<f'), -1)
    if len(N) == 2:
        ny, nz = N
        nx = len(data) / (ny * nz)
        assert nx == int(nx), "Size of turbulence box (%d) does not match ny x nz (%d), nx=%.2f" % (
            len(data), ny * nz, nx)
        nx = int(nx)
    else:
        nx, ny, nz = N
        assert len(data) == nx * ny * \
            nz, "Size of turbulence box (%d) does not match nx x ny x nz (%d)" % (len(data), nx * ny * nz)
    return data.reshape(nx, ny * nz)


# Function that converts rpm to radians per second
def rpm2rad(rpm):
    return rpm*2*np.pi/60


#%% Main   

if __name__ == '__main__':
    
    turbine = DtuTurbine()
    
    # turbine.visualize_turbine()
    
    # turbine.plot_airfoil_data()
    
    t_arr, _, _, P_arr, T_arr = turbine.bem(windspeed=20)
    
    # Plotting turbine power
    plt.figure()
    plt.title('Turbine power')
    plt.axhline(turbine.P_rated/10**6, color='r', linestyle='--')
    plt.plot(t_arr, P_arr/10**6)
    plt.xlabel('Time [s]')
    plt.ylabel('Power [MW]')
    plt.show()
    
    # Plotting turbine thrust
    plt.figure()
    plt.title('Turbine thrust')
    plt.plot(t_arr, T_arr)
    plt.xlabel('Time [s]')
    plt.ylabel('Thrust [N]')
    plt.show()
    


# %%

def divide(x, y):
    """_summary_

    Parameters
    ----------
    x : _type_
        _description_
    y : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """     
    
    return x/y
