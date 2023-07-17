import numpy
import math

def get_ratio(list_a, list_b):
    ratio_ab = []
    for i in range(len(list_a)):
        if (list_a[i] == 0 or list_b[i] == 0):
            ratio_ab.append(0)
        else:
            ratio = list_a[i]/list_b[i]
            ratio_ab.append(ratio)
    return(ratio_ab)



'''Dated
def simulateTheoreticalB(x_array):
    max_array = []
    eta = numpy.random.normal(loc = 0.0, scale = 1.0, size = (pow(26,2) , 1) ) 
    sum = 0
    for i in range(pow(26,2)):
        sum += eta[i]
    avg_eta = sum/len(eta)
            

    for x in x_array:
        max_array.append( pow( ( 2 * rvar.mu_not * rvar.alpha * rvar.kb * x )/(rvar.Msat * (rvar.gamma) * rvar.volume * rvar.t_step) ,1/2) )
    min_array = [ elem * -1 for elem in max_array]

    return max_array, min_array
'''

'''lambda function better
def get_inv_kelvin(list_temp):
    return ([ 0 if temp==0 else 1.0/temp  for temp in list_temp])
'''
'''better to use np.average
def avg_data(ordered_data):
    averaged = []
    sum=0
    for i in range(0,11):
        for j in range(0,1000):
            sum+=float(ordered_data[j][i])
        averaged.append(sum/1000)
        sum=0
    return averaged
'''
def list_to_float(arr):
    try: 
        return ([float(elem) for elem in arr])
    except(TypeError):
        return ( [[float(elem) for elem in nested_arr ] for nested_arr in arr ] )
