#parse ovf files, calculate thermal switching rate, then plot inverse temperature against switching rate
#written by Jared Arzate — Jan 2023
import sys
import defs
sys.path.append(defs.func_dir)
sys.path.append(defs.out_dir)

import generic_functions as gf
import mx3_functions     as mf 
import umame_functions   as uf
import global_vars       as gvar

import math
from   pathlib import Path
from dataclasses import dataclass
from itertools import repeat
import matplotlib.pyplot as plt

@dataclass
class data_set:
    x     : list
    y     : list
    label : str
    color : str='0'

run_time = 1e-6
t_step   = 1e-12
alpha    = 0.1
ku1      = 1e4
Msat     = 1e6
volume   = 10e-9**3
get_sr            =  lambda norm : norm / run_time
norm_to_cell      =  lambda x,l: x/(l**2)
get_inv_temp      =  lambda t  :  0 if t==0 else 1.0/t
get_analytical_sr =  lambda x  :  0 if x == 0 else gvar.gamma*(alpha/(1+alpha**2))*(pow((8*(ku1**3)*volume) / \
                                 (2*gvar.pi*Msat**2*gvar.kb*(1/x)),1/2))*math.exp((-1*(ku1*volume))/(gvar.kb*(1/x)))
mumax512y = [131580000000.0, 131345000000.0, 131347000000.0, 130936000000.0, 129064000000.0, 126114000000.0, 117724000000.0, 106629000000.0,
             92630000000.0, 76508000000.0, 61394000000.0, 48053000000.0, 36877000000.0, 27497000000.0, 20471000000.0, 14664000000.0,
             10775000000.0, 7913000000.0, 5631000000.0, 4089000000.0, 2978000000.0, 1966000000.0, 1411000000.0, 1071000000.0, 732000000.0,
             525000000.0, 385000000.0, 260000000.0, 209000000.0, 155000000.0, 101000000.0, 64000000.0, 51000000.0, 35000000.0, 20000000.0,
             19000000.0, 11000000.0, 7000000.0, 12000000.0, 4000000.0, 4000000.0, 0.0, 2000000.0, 1000000.0, 0.0, 0.0, 0.0, 1000000.0,
             1000000.0, 0.0]
mumax512x = [0.005, 0.0055, 0.006, 0.0065, 0.007, 0.0075, 0.008, 0.0085, 0.009, 0.0095, 0.01, 0.0105, 0.011, 0.0115, 0.012, 0.0125,
             0.013, 0.0135, 0.014, 0.0145, 0.015, 0.0155, 0.016, 0.0165, 0.017, 0.0175, 0.018, 0.0185, 0.019, 0.0195, 0.02, 0.0205,
             0.021, 0.0215, 0.022, 0.0225, 0.023, 0.0235, 0.024, 0.0245, 0.025, 0.0255, 0.026, 0.0265, 0.027, 0.0275, 0.028, 0.0285,
             0.029, 0.0295]
#temps     = [80,90,100,110,120,130,140,150,160,170,180]
temps     = [10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160]
def main():
    print(f"using",defs.out_dir,"as output path.")
    print(f"and",defs.in_dir,"as input path.")
    print("remember to hardcode temperature array and run time\n")

    print("enter dir name: ")
    data_dir = input()

    print("enter filename to save plot as png: ")
    plot_f_name = input()

    data_label = uf.parse_filename_umame()
    path = Path(defs.in_dir) / data_dir
    cell_data_each_file = uf.get_switch_data_umame(data_label,path)
    switching_rates  = list(map(get_sr, gf.get_num_switches(cell_data_each_file)))
    print(switching_rates)
    input()
    inv_temps_kelvin = list(map(get_inv_temp, temps))

    umame  = data_set( inv_temps_kelvin, list(map(norm_to_cell,switching_rates,repeat(32))), "umame", 'tab:blue' )
    mx3    = data_set( mumax512x,        list(map(norm_to_cell,mumax512y, repeat(512))),     "mx3",   'tab:red'  )
    theory = data_set( mumax512x,        list(map(get_analytical_sr,mumax512x)),             "analytical", 'tab:green')

    plot_data_sets(umame,mx3,theory,plot_f_name)

def plot_data_sets(u,m,a,f_name):
    fig = plt.figure()
    ax  = fig.add_subplot(1, 1, 1)
    ax.set_ylim([1, 10000000.0])
    ax.set_xlim([0.004,0.02])
    ax.set_title('Thermal Switching rate')
    ax.set_xlabel('Inverse Temperature (K)')
    ax.set_ylabel('Switching Rate (s^-1)')
    ax.set_yscale("log")
    ax.grid(visible=True,which='both',axis='both')
    ax.legend()
    plt.style.use('classic')

    ax.scatter(u.x,u.y,label=u.label,color=u.color)
    ax.scatter(m.x,m.y,label=m.label,color=m.color,alpha=0.1)
    ax.plot(a.x,a.y,label=a.label,color=a.color)
    f_name = f_name + '.png'
    path = Path(defs.out_dir)/'png'/f_name
    plt.show()
    fig.savefig(path,format='png', dpi=1200)

if __name__ == "__main__":
    main()
