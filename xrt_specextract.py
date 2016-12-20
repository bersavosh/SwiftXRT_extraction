import glob, os, sys
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

file_names = glob.glob('sw*po_cl.evt')
print 'Will analyse the following observations:'
print file_names
for i in range(len(file_names)):
    evt_fits = fits.open(file_names[i])
    obs_id = evt_fits[1].header['OBS_ID']
    obs_mode = evt_fits[1].header['DATAMODE']
    obs_lc = fits.open(file_names[i].replace('_cl.evt', 'sr.lc'))[1].data
    print '==========================='
    print 'obs_id:', obs_id
    print 'Data mode:', obs_mode
    print 'Number of GTIs in the observation:', len(evt_fits['GTI'].data)
    print 'Ploting lightcurve'
    print 'Average count rate:', np.average(obs_lc['RATE'])

    pileup_flag = False
    if np.average(obs_lc['RATE']) > 0.4 and obs_mode == 'PHOTON':
        print 'Warning: Pile up possible'
        pileup_flag = True

    plt_lc = raw_input('Plot lightcurve?(y/n)[n]')
    if plt_lc == 'y':
        plt.errorbar(obs_lc['TIME'], obs_lc['RATE'], yerr=obs_lc['ERROR'], fmt='.k')
        plt.show()

    extr = raw_input('Extract spectrum?(y/n)[y]')
    extr_flag = True if extr == 'y' or extr == '' else False

    splt = 'n'
    if len(evt_fits['GTI'].data) > 1:
        splt = raw_input('split observation based on GTIs?(y/n)[n]')
    splt_flag = True if splt == 'y' else False

    grade_flag = False
    rmf_file = 'NONE'

    if extr_flag is True:
        if splt_flag is False:
            print 'I will extract spectrum without splitting'
            print 'Create and save source and backgroud regions'
            print 'Format: '+file_names[i].replace('cl.evt', 'src.reg')
            print 'Format: '+file_names[i].replace('cl.evt', 'bkg.reg')
            os.system('ds9 '+file_names[i]+' &')
            ch = raw_input('continue?')
            if ch == 'n':
                sys.exit(1)

            print 'Writing the extraction script: spec_extract_'+obs_id+'.xco'
            f = open('spec_extract_'+obs_id+'.xco', 'w')
            f.write(obs_id+'\n')
            f.write('read event\n')
            f.write('.\n')
            f.write(file_names[i]+'\n')
            f.write('yes\n')
            if obs_mode == 'WINDOWED':
                print 'Observatin in WT mode, extracting grade 0 spectrum only.'
                grade_flag = True
                f.write('filter grade 0\n')
            f.write('filter region '+file_names[i].replace('cl.evt', 'src.reg')+'\n')
            f.write('extract spectrum\n')
            f.write('save spectrum '+file_names[i].replace('cl.evt', 'spec_src.pha')+'\n')
            f.write('clear region\n')
            f.write('filter region '+file_names[i].replace('cl.evt', 'bkg.reg')+'\n')
            f.write('extract spectrum\n')
            f.write('save spectrum '+file_names[i].replace('cl.evt', 'spec_bkg.pha')+'\n')
            f.write('exit\nno')
            f.close()

            print 'Extracting spectra'
            os.system('xselect @'+'spec_extract_'+obs_id+'.xco')

            print 'Running xrtmkarf'
            print 'xrtmkarf outfile='+ file_names[i].replace('cl.evt', 'spec.arf') + ' phafile='+file_names[i].replace('cl.evt', 'spec_src.pha')+' expofile='+file_names[i].replace('cl.evt', 'ex.img') +' srcx=-1 srcy=-1 psfflag=yes'
            os.system('xrtmkarf outfile='+ file_names[i].replace('cl.evt', 'spec.arf') + 
                ' phafile='+file_names[i].replace('cl.evt', 'spec_src.pha') + 
                ' expofile='+file_names[i].replace('cl.evt', 'ex.img') + 
                ' srcx=-1 srcy=-1 psfflag=yes')

            print 'Checking for RMF:'
            if obs_mode == 'WINDOWED':
                if grade_flag == True:
                    rmf_file = 'swxwt0s6_20131212v015.rmf'
                    if os.path.isfile('swxwt0s6_20131212v015.rmf') is False:
                        print 'Downloading WT grade 0 RMF'
                        os.system('wget http://heasarc.gsfc.nasa.gov/FTP/caldb/data/swift/xrt/cpf/rmf/swxwt0s6_20131212v015.rmf')
                    else: 
                        print 'WT grade 0 RMF already exists'
                if grade_flag == False:
                    rmf_file = 'swxwt0to2s6_20131212v015.rmf'
                    if os.path.isfile('swxwt0to2s6_20131212v015.rmf') is False:
                        print 'Downloading WT grade 0-2 RMF'
                        os.system('wget http://heasarc.gsfc.nasa.gov/FTP/caldb/data/swift/xrt/cpf/rmf/swxwt0to2s6_20131212v015.rmf')
                    else: 
                        print 'WT grade 0-2 RMF already exists'
            elif obs_mode == 'PHOTON':
                rmf_file = 'swxpc0to12s6_20130101v014.rmf'
                if os.path.isfile('swxpc0to12s6_20130101v014.rmf') is False:
                    print 'Downloading PC grade 0-12 RMF'
                    os.system('wget http://heasarc.gsfc.nasa.gov/FTP/caldb/data/swift/xrt/cpf/rmf/swxpc0to12s6_20130101v014.rmf')
                else: 
                    print 'PC grade 0-12 RMF already exists'

            print 'Spectral binning:'
            spec_bin = raw_input('Number of counts per bin? ')
            print 'Creating binned spectrum'
            os.system('grppha ' + file_names[i].replace('cl.evt', 'spec_src.pha ') +
                file_names[i].replace('cl.evt', 'spec_src_bin'+str(spec_bin)+'.pha ') +
                'comm="bad 0-29 & group min ' + str(spec_bin) +
                ' & chkey backfile ' + file_names[i].replace('cl.evt', 'spec_bkg.pha') +
                ' & chkey ancrfile ' + file_names[i].replace('cl.evt', 'spec.arf') +
                ' & chkey respfile ' + rmf_file +
                ' & exit" ')
            print 'Spectrum extracted for ' + obs_id
            print '==========================='

        if splt_flag is True:
            print 'I will Extract spectrum with splitting'
            for j in range(len(evt_fits['GTI'].data)):
                print 'Writing the event splitting script'
                f = open('evt_splt_'+obs_id+'_seg'+str(j+1)+'.xco', 'w')
                f.write(obs_id+'_seg'+str(j+1)+'\n')
                f.write('read event\n')
                f.write('.\n')
                f.write(file_names[i]+'\n')
                f.write('yes\n')   
                f.write('filter time scc\n')
                f.write(str(evt_fits['GTI'].data[j][0])+','+str(evt_fits['GTI'].data[j][1])+'\n')
                f.write('x\n')
                f.write('extract event\n')
                f.write('save events '+file_names[i].replace('.evt', '_seg'+str(j+1)+'.evt\n'))
                f.write('yes\n')
                f.write('exit\nno')
                f.close()

                print 'Extracting events in segment ',j+1
                os.system('xselect @'+'evt_splt_'+obs_id+'_seg'+str(j+1)+'.xco')

                print 'Create and save source and backgroud regions for seg.',j+1
                print 'Format: '+file_names[i].replace('cl.evt', 'seg'+str(j+1)+'_src.reg')
                print 'Format: '+file_names[i].replace('cl.evt', 'seg'+str(j+1)+'_bkg.reg')
                os.system('ds9 '+file_names[i].replace('.evt', '_seg'+str(j+1)+'.evt')+' &')
                ch = raw_input('continue?')
                if ch == 'n':
                    sys.exit(1)

                print 'Writing the extraction script: spec_extract_'+obs_id+'_seg'+str(j+1)+'.xco'
                f = open('spec_extract_'+obs_id+'_seg'+str(j+1)+'.xco', 'w')
                f.write(obs_id+'_seg'+str(j+1)+'\n')
                f.write('read event\n')
                f.write('.\n')
                f.write(file_names[i].replace('.evt', '_seg'+str(j+1)+'.evt')+'\n')
                f.write('yes\n')
                if obs_mode == 'WINDOWED':
                    print 'Observatin in WT mode, extracting grade 0 spectrum only.'
                    grade_flag = True
                    f.write('filter grade 0\n')
                f.write('filter region '+file_names[i].replace('cl.evt', 'seg'+str(j+1)+'_src.reg')+'\n')
                f.write('extract spectrum\n')
                f.write('save spectrum '+file_names[i].replace('.evt', '_seg'+str(j+1)+'_spec_src.pha')+'\n')
                f.write('clear region\n')
                f.write('filter region '+file_names[i].replace('cl.evt', 'seg'+str(j+1)+'_bkg.reg')+'\n')
                f.write('extract spectrum\n')
                f.write('save spectrum '+file_names[i].replace('.evt', '_seg'+str(j+1)+'_spec_bkg.pha')+'\n')
                f.write('exit\nno')
                f.close()

                print 'Extracting spectra'
                os.system('xselect @'+'spec_extract_'+obs_id+'_seg'+str(j+1)+'.xco')

                print 'Warning: Need to create new exposure map. To be implemented.'
                sys.exit(1)
            print '==========================='
