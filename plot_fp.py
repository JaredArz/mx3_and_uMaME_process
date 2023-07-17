import sys
import defs
sys.path.append(defs.func_dir)
sys.path.append(defs.out_dir)
import matplotlib.pyplot as plt
import numpy as np
import generic_functions as gf
import plotting_functions as pfunc
from pathlib import Path
from dataclasses import dataclass
from itertools import repeat


@dataclass
class comp:
    vals  : np.ndarray
    color : str
    label : str

class data_set:
    def __init__(self,name,x,y,z):
        self.name = name
        self.x = comp(x.vals,x.color,x.label)
        self.y = comp(y.vals,y.color,y.label)
        self.z = comp(z.vals,z.color,z.label)
        
iters = 1000
T = [val for val in range(80,190,10)]
uB_file = "10m_b_np.txt"
uM_file = "10m_mag_np.txt"
mB_file = "mx3_0612_b_np.txt"
mM_file = "mx3_0612_m_np.txt"
avg_col = lambda i,c : np.average(c[i,:],axis=0)

def main():
    ############################  x and y declare ###########################
    print("enter data dir")
    data_dir = input()
    print("remeber to hardcode data files and temp")

    mM,mB,uM,uB = load_data(data_dir)
    mM_avg = data_set('mM avg',
                      comp(np.array(list(map(avg_col,[i for i in range(11)],repeat(mM.x.vals)))), 'red',   'mx3 avg mx'),
                      comp(np.array(list(map(avg_col,[i for i in range(11)],repeat(mM.y.vals)))), 'green', 'mx3 avg my'),
                      comp(np.array(list(map(avg_col,[i for i in range(11)],repeat(mM.z.vals)))), 'blue',  'mx3 avg mz'))

    uM_avg = data_set('uM avg',
                      comp(np.array(list(map(avg_col,[i for i in range(11)],repeat(uM.x.vals)))), 'red',   'u avg mx'),
                      comp(np.array(list(map(avg_col,[i for i in range(11)],repeat(uM.y.vals)))), 'green', 'u avg my'),
                      comp(np.array(list(map(avg_col,[i for i in range(11)],repeat(uM.z.vals)))), 'blue',  'u avg mz'))

    ratioMx = pfunc.get_ratio(uM_avg.x.vals, mM_avg.x.vals )
    ratioMy = pfunc.get_ratio(uM_avg.y.vals, mM_avg.y.vals )
    ratioMz = pfunc.get_ratio(uM_avg.z.vals, mM_avg.z.vals )
    ################### create fig and axs object ################################

    fig = plt.figure()
    gs = fig.add_gridspec(2, 3, hspace=0, wspace=0)
    (ax1, ax2, ax3), (ax4, ax5, ax6) = gs.subplots(sharex='col', sharey='row')

    fig2 = plt.figure()
    gs2 = fig2.add_gridspec(2, 3, hspace=0, wspace=0)
    (max1, max2, max3), (max4, max5, max6) = gs2.subplots(sharex='col')

    fig3, rax = plt.subplots()

    ##################### plot x's and y's ##########################
    _ = [uB.x, uB.y, uB.z, mB.x, mB.y, mB.z]
    for i in range(len(fig.get_axes())):
        curr_ax = list(fig.get_axes())[i]
        curr_ax.grid(visible=True,which='both',axis='both')
        curr_data_set = _[i]
        curr_ax.label_outer()
        for j in range(iters):
            curr_y = curr_data_set.vals[:,j]
            curr_ax.scatter(T, curr_y, color=curr_data_set.color, label = curr_data_set.label, alpha = 0.01, s=8)

    _ = [uM.x, uM.y, uM.z, mM.x, mM.y, mM.z]
    for i in range(len(fig2.get_axes())):
        curr_ax = list(fig2.get_axes())[i]
        curr_ax.grid(visible=True,which='both',axis='both')
        curr_ax.label_outer()
        curr_data_set = _[i]
        for j in range(iters):
            curr_y = curr_data_set.vals[:,j]
            curr_ax.scatter(T, curr_y, color=curr_data_set.color, label = curr_data_set.label, alpha = 0.01, s=8)

    max4.plot(T, mM_avg.x.vals, color=mM_avg.x.color, label = mM_avg.x.label, alpha = 1)
    max1.plot(T, uM_avg.x.vals, color=uM_avg.x.color, label = uM_avg.x.label, alpha = 1)

    rax.plot(T, ratioMx,color='tab:red', label =   "x"  )

    ############### format axs ########################
    ax1.set_ylim([-0.01,0.01])
    ax2.set_ylim([-0.01,0.01])
    ax3.set_ylim([-0.01,0.01])
    ax4.set_ylim([-0.01,0.01])
    ax5.set_ylim([-0.01,0.01])
    ax6.set_ylim([-0.01,0.01])
    ax1.set_xlim([70,190])
    ax2.set_xlim([70,190])
    ax3.set_xlim([70,190])
    ax4.set_xlim([70,190])
    ax5.set_xlim([70,190])
    ax6.set_xlim([70,190])

    max2.set_ylim([-0.05,0.05])
    max3.set_ylim([-0.05,0.05])
    max5.set_ylim([-0.05,0.05])
    max6.set_ylim([-0.05,0.05])
    max3.secondary_yaxis('right')
    max6.secondary_yaxis('right')
    max1.set_ylim([-0.1,1.1])
    max4.set_ylim([-0.1,1.1])
    max3.set_xlim([70,190])
    max6.set_xlim([70,190])

    rax.legend(prop={'size':7}, loc='lower right')
    rax.set_ylim(-2,2)
    rax.set_title('M u / M mx3')
    rax.set_xlabel('Temp (K)')

    fig.suptitle('umame & mx3 Bx,By,Bz')
    fig2.suptitle('umame & mx3 Mx,My,Mz')
    plt.style.use('classic')
    plt.show()
    input()
    fig.savefig('./output/png/F1.png',format='png', dpi=1200)
    fig2.savefig('./output/png/F2.png',format='png', dpi=1200)
    fig3.savefig('./output/png/Fr.png',format='png', dpi=1200)


def load_data(data_dir):
    _ = Path(defs.out_dir)
    mM = data_set("mx3 M",
                   comp(np.loadtxt(_/data_dir/mM_file,comments='#',skiprows=1,max_rows=11)  ,  "red",  'mx3 mx' ),
                   comp(np.loadtxt(_/data_dir/mM_file,comments='#',skiprows=12,max_rows=11) ,  "green",'mx3 my' ),
                   comp(np.loadtxt(_/data_dir/mM_file,comments='#',skiprows=24,max_rows=11) ,  "blue", 'mx3 mz' ))
    mB = data_set("mumax B therm",
                   comp( np.loadtxt(_/data_dir/mB_file,comments='#',skiprows=1,max_rows=11)  ,  "red",  'mx3 bx' ),  
                   comp( np.loadtxt(_/data_dir/mB_file,comments='#',skiprows=12,max_rows=11) ,  "green",'mx3 by' ),
                   comp( np.loadtxt(_/data_dir/mB_file,comments='#',skiprows=24,max_rows=11) ,  "blue", 'mx3 bz' ))
    uM = data_set("umame M",
                   comp( np.loadtxt(_/data_dir/uM_file,comments='#',skiprows=1,max_rows=11) ,  "red",  'u mx' ),
                   comp( np.loadtxt(_/data_dir/uM_file,comments='#',skiprows=12,max_rows=11),  "green",'u my' ),
                   comp( np.loadtxt(_/data_dir/uM_file,comments='#',skiprows=24,max_rows=11),  "blue", 'u mz' ))
    uB  = data_set("umame B therm",
                   comp( np.loadtxt(_/data_dir/uB_file,comments='#',skiprows=1,max_rows=11) ,  "red",  'u bx'  ),
                   comp( np.loadtxt(_/data_dir/uB_file,comments='#',skiprows=12,max_rows=11) ,  "green",'u by' ),
                   comp( np.loadtxt(_/data_dir/uB_file,comments='#',skiprows=24,max_rows=11) ,  "blue", 'u bz' ))
    return mM,mB,uM,uB


def avg_data(mM,uM):
    mM_avg = data_set("mumax3 M avg",
                    comp( np.average(mM.x.vals, 0), "red", 'mx3 avg mx'),
                    comp( np.average(mM.y.vals, 0), "red", 'mx3 avg my'),
                    comp( np.average(mM.z.vals, 0), "red", 'mx3 avg mz'))
    uM_avg = data_set("umame M avg",
                    comp( np.average(uM.x.vals, 0), "red", 'u avg mx'),
                    comp( np.average(uM.y.vals, 0), "red", 'u avg my'),
                    comp( np.average(uM.z.vals, 0), "red", 'u avg mz'))
    return mM_avg,uM_avg

if __name__ == "__main__":
    main()
