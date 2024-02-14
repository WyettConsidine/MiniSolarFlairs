import netCDF4 as nc
import numpy as np
import cftime
import matplotlib.pyplot as plt
from datetime import datetime
import os
import requests


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

def plot_xrsa_flux(ff, datetime0, platform, make_plot= True, num_vars= 2):
    var_name = ["xrsa_flux", "xrsb_flux"]
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

print("Done.\n")


def main():
    print('plotting data')
    ###NOTE: this may change depending on what directory you are in. Start with dir path outside MiniSolarFlairs
    dir0 = 'MiniSolarFlairs\\data\\'
    file0 =  'sci_xrsf-l2-avg1m_g16_d20200601_v2-2-0.nc'
    ff = grabData(dir0,file0)
    datetime0 = getDateTime0(file0, ff)
    platform = getPlatform(ff)
    plot_xrsa_flux(ff,datetime0,platform)
    
print("Hello")
main()