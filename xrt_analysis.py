import numpy as np
from xspec import *
import glob
from astropy.io import fits, ascii
from astropy.table import Table, vstack

#import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)
rc('font', family='serif')

Xset.abund = "wilm"
Xset.xsect = "vern"
Fit.query = "yes"
Fit.nIterations = 100
Plot.device = "/xs"
Plot.xAxis = "KeV"

datalist=glob.glob('sw*bin*')

obs_id = []
mjd = []
obs_exp = []
pw_nh = []
pw_nh_ler = []
pw_nh_uer = []
pw_gamma = []
pw_gamma_ler = []
pw_gamma_uer = []
pw_flx = []
pw_flx_ler = []
pw_flx_uer = []
fit_chi2 = []
fit_dof = []

Xset.openLog("fit_log.txt")
for i in range(len(datalist)):
    hdulist = fits.open(datalist[i])
    obs_id.append(hdulist[0].header['OBS_ID'])
    mjd.append(hdulist[0].header['MJD-OBS'])
    obs_exp.append(hdulist[0].header['EXPOSURE'])
    
    AllData(datalist[i])
    AllData.ignore('bad')
    AllData.ignore('*:10.0-**')
    if datalist[i].find('xpc') > 0:
        AllData.ignore('*:**-0.3')
    else:
        AllData.ignore('*:**-0.5')
    
    m = Model('tbabs*pegpwrlw')
    AllModels(1)(3).values = [0.5]
    AllModels(1)(3).frozen = True
    Fit.perform()
    Plot('lda del')
    pw_nh.append(AllModels(1)(1).values[0]*1e22)
    pw_gamma.append(AllModels(1)(2).values[0])
    pw_flx.append(AllModels(1)(5).values[0]*1e-12)
    fit_chi2.append(Fit.statistic/Fit.dof)
    fit_dof.append(Fit.dof)
    Fit.error('maximum 3 1-5')
    pw_nh_ler.append((AllModels(1)(1).values[0]-AllModels(1)(1).error[0])*1e22)
    pw_nh_uer.append((AllModels(1)(1).error[1]-AllModels(1)(1).values[0])*1e22)
    pw_gamma_ler.append(AllModels(1)(2).values[0]-AllModels(1)(2).error[0])
    pw_gamma_uer.append(AllModels(1)(2).error[1]-AllModels(1)(2).values[0])
    pw_flx_ler.append((AllModels(1)(5).values[0]-AllModels(1)(5).error[0])*1e-12)
    pw_flx_uer.append((AllModels(1)(5).error[1]-AllModels(1)(5).values[0])*1e-12)
Xset.closeLog()

result=Table(data=[obs_id,mjd,pw_nh,pw_nh_ler,pw_nh_uer,pw_gamma,pw_gamma_ler,pw_gamma_uer,
                   pw_flx,pw_flx_ler,pw_flx_uer,fit_chi2,fit_dof],
             names=['Obs.ID','MJD','NH','NH_err-','NH_err+','gamma','gamma_err-','gamma_err+',
                    'flux','flux_err-','flux_err+','red_chi2','d.o.f'])

result.sort('MJD')
result.write('swift_xrt_monitoring.txt', format='ascii.tab')