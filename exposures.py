import math
from re import I
# get exposure times based off of T1 and T2
def get_exposures(x,Te,Tr,T1,T2,fstop):
    #Tes for each scan
    #all values in miliseconds
    index=0
    for te in Te:
        tr=Tr[index]
        get_exposure_time(x,te,Tr[index],T1,T2,fstop)
        index +=1
        

#calculate exposure time for Te
def get_exposure_time(x,Te,Tr,T1,T2,fstop):
    #skipping the x for now
    if T1!=0 and T2!=0 :
        exposure_time=x*(1-math.exp(-Tr/T1))*math.exp(-Te/T2)
    else:
        exposure_time=0

    ev=get_ev(exposure_time, fstop)
    print(f"Calculating for params: T1={T1}ms, T2={T2}ms, Te={Te}ms, Tr={Tr}ms")
    print(f"Exposure time= {exposure_time}s")
    print(f"Calculated EV= {ev}")
    print('---------------------------------------')


def calculate_exposure(x,Te,Tr,T1,T2,fstop):
    #skipping the x for now
    if T1!=0 and T2!=0 :
        exposure_time=x*(1-math.exp(-Tr/T1))*math.exp(-Te/T2)
    else:
        exposure_time=0
    
    return exposure_time

#correct
#calculate ev based on time and f-stop
def get_ev(time,fstop):
    if time==0:
        return 0
    else:
        ev=math.log(((fstop**2)*time),2)
        return ev