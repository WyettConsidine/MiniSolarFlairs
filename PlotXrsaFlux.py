import netCDF4 as nc
import numpy as np
import cftime
import matplotlib.pyplot as plt
from datetime import datetime
import xarray as xr
import math
from scipy.optimize import curve_fit


def grabData(dir0, file0):
    ff = nc.Dataset(dir0 + file0)
    return ff

def getDateTime0(file0 ,ff):
    datetime0 = cftime.num2pydate(ff.variables["time"][:], ff["time"].units)
    print("Filename:  ", file0)
    print("start time in file [{}]: {}".format(ff["time"].units, ff.variables["time"][0]))
    print("start and end times:", datetime0[0], datetime0[-1])
    return datetime0

def getPlatform(ff):
    platform = getattr(ff, "platform")
    print("satellite: ", platform)
    return platform

def plot_xrsb_flux(ff, datetime0, platform, make_plot= True, num_vars= 1):
    var_name = ["xrsb_flux"]
    if make_plot:
        chan_color = ["mediumorchid", "green", "darkviolet", "indigo", "b",
                    "darkcyan", "greenyellow", "yellow", "gold", "orange",
                    "orangered", "darkred"][0:num_vars]
        plt.figure(0, figsize=[10, 7])
        for ii in range(num_vars):
            plt.plot(
                datetime0[:],
                ff.variables[var_name[ii]][:],
                linewidth=1,
                color=chan_color[ii],
                label="{} {}".format(platform, var_name[ii]),
            )
        plt.yscale("log")
        plt.legend(loc="upper right", prop={"size": 12})
        plt.xlabel("Time [UT]")
        plt.ylabel("X-Ray Flux [{}]".format(ff[var_name[0]].units))
        plt.show()

def explData(ff):
    print("ff type: " + str(type(ff)))
    print(ff.variables.keys())

def ncDatasetToDF(dir0, file0):
    Warning("Note: in transition from nc type to dataframe, meta-data is lost.")
    ds = xr.open_dataset(dir0+file0)
    df = ds.to_dataframe()
    return df

#take parameters, and output f(x) applied to input series t
def flareShape(t,A,B,C,D):
    const1 = .5 * math.pow(math.pi,.5) * A * C
    output = []
    for i in t:
        partialfunc1 = lambda t : math.exp((D * (B-t)) + ((math.pow(C,2) * math.pow(D,2))/4))
        Z = (2*B + math.pow(C,2) * D)/(2*C) 
        partialfunc2 = lambda t: math.erf(Z) - math.erf(Z - (t/C))
        completeFunc = lambda t : const1 * partialfunc1(t) * partialfunc2(t)
        output.append(completeFunc(i))
    return output

def Gaussian(t,a,b,c):
    output = []
    for i in t:
        compfunc = lambda t: a * math.exp(-math.pow(t-b, 2) / math.pow(c,2))
        output.append(compfunc(i))
    return output

#fit single flare to input data
def fitData(xData, yData, flareShape):
    popt, pcov = curve_fit(flareShape, xData, yData)
    return popt




def main():

    #d20170804 decient
    #print('plotting data')
    ###NOTE: this may change depending on what directory you are in. Start with dir path outside MiniSolarFlairs
    dir0 = 'data\\'
    day = 7
    file0 =  f'sci_xrsf-l2-avg1m_g16_d2017090{day}_v2-2-0.nc'
    ff = grabData(dir0,file0)
    
    # ### original set
    # datetime0 = getDateTime0(file0, ff)
    # platform = getPlatform(ff)
    # plot_xrsb_flux(ff,datetime0[:],platform)
    # #explData(ff)
    # print(getDateTime0(file0,ff))
    # print(datetime0[:], ff.variables["xrsb_flux"][:])


    #avg1min
    dataDF = ncDatasetToDF(dir0,file0)
    #print(dataDF.index)
    dataDF['time'] = [ind[0] for ind in dataDF.index]
    #print(dataDF.columns)
    timeFrame = (dataDF['time'] > f'2017-09-{day} 12:00:00' ) & (dataDF['time'] < f'2017-09-{day} 18:00:00')
    #print(dataDF[timeFrame])
    # plt.plot(dataDF[timeFrame]['time'],dataDF[timeFrame]['xrsb_flux'])
    # plt.show()

    # #fitting Flare
    x = [x for x in range(len(dataDF[timeFrame]['time']))]
    print(x)
    popt = fitData(x,dataDF[timeFrame]['xrsb_flux'],flareShape)
    print(popt)
    pred = flareShape(range(len(dataDF[timeFrame]['time'])), *popt)
    
    #pred = [EfOfT(x) for x in range(len(dataDF[timeFrame]['time']))]
    #print(pred)
    #plt.plot(range(len(dataDF[timeFrame]['time'])),dataDF[timeFrame]['xrsb_flux'])
    plt.plot(x,pred,c='b')
    plt.plot(x, dataDF[timeFrame]['xrsb_flux'], c= 'r')
    plt.show()

    # #resids
    # residuals = dataDF[timeFrame]['xrsb_flux']- pred
    # plt.plot(range(len(dataDF[timeFrame]['time'])),residuals, c= 'g')
    # plt.show()


    #G fit for sanity
    #x = [x/100 for x in range(0,1400)]
    #print(x)
    # #Param 1: amplitude, 2: mean, 3:sharpness/sd?, 4: expDecay rate, 5&6 background.
    #params = [1/1000,6.5,-.2,1.5]
    # y = flareShape(x,*params)
    # print(y)
    # plt.plot(x,y)
    # plt.show()

    # print('complete')



main()