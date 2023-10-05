#
#	Functions for FRB polarization analysis
#
#								AB, April 2023

#	Import modules

import os
import numpy as np
import rmheald.rm_heald as rmh
from rmnest.fit_RM import RMNest
from RMtools_1D.do_RMsynth_1D import run_rmsynth
from RMtools_1D.do_RMclean_1D import run_rmclean
from scipy.optimize import curve_fit
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

#	---------------------------------------------------------------------------------

def pangdiffdeg(ang, ang0):
	ang			=	np.deg2rad(ang)
	ang0		=	np.deg2rad(ang0)
	dpang		=	np.rad2deg(np.arcsin(np.sin(ang-ang0)))
	return(dpang)

#	---------------------------------------------------------------------------------

def rm_synth_clean(fghz, iqu, diqu, phirange, dphi, cleancutoff):
	'''
	Function to determine RM using RM synthesis and RM cleaning
	Uses RM code by Heald et al. 
	
	Inputs	-	Frequencies in GHz
				I Q U spectrum
				I Q U noise spectrum
				range of phi
				resolution in phi
				clean cut-off	
	'''

	p 			=	rmh.PolObservation(fghz*1.0e9, iqu, IQUerr=diqu)
	phi_axis 	= 	np.arange(-phirange, phirange+dphi/2.0, dphi)
	
	print("\n **************** Messages from RM synthesis *******************\n")
	p.rmsynthesis(phi_axis)	
	p.rmclean(cutoff=cleancutoff)	
	p.plot_fdf()	
	p.get_fdf_peak()
	p.print_rmstats()
	print("\n ***************************************************************\n")	
	
	#print(p.fdf_peak,p.fdf_peak_rm,p.fdf_peak_rm_err,p.pa)
	#print(p.cln_fdf_peak,p.cln_fdf_peak_rm,p.cln_fdf_peak_rm_err,p.cln_pa)
	
	fdfpeak	=	(p.fdf_peak, p.cln_fdf_peak)
	peakrm	=	(p.fdf_peak_rm, p.cln_fdf_peak_rm)
	epeakrm	=	(p.fdf_peak_rm_err, p.cln_fdf_peak_rm_err)
	peakpa	=	(p.pa, p.cln_pa)
		
	return(fdfpeak, peakrm, epeakrm, peakpa)
	
#	---------------------------------------------------------------------------------

def fr_rmenst(fghz, f0ghz, iquv, diquv):
	'''
	Function to determine RM using RM fitting by RMNEST
	
	Inputs	-	Frequencies in GHz
				Central frequency in GHz
				I Q U spectrum
				I Q U noise spectrum					
	'''
	os.system("mkdir junk")
	rmn		=	RMNest(freqs=fghz*1.0e3, freq_cen = f0ghz*1.0e3, s_q = iquv[1], s_u = iquv[2], s_v = iquv[3], rms_q = diquv[1], rms_u = diquv[2], rms_v = diquv[3])
	rmn.fit(gfr=False, outdir='junk')
	rmn.print_summary()
		
	return(0)	

#	---------------------------------------------------------------------------------

def fr_rmtool(fghz, iquv, diquv):
	'''
	Function to determine RM using RM synthesis with RMtool
	
	Inputs	-	Frequencies in GHz
				I Q U spectrum
				I Q U noise spectrum					
	'''
	
	rmtdata	=	np.array([fghz*1.0e9, iquv[0], iquv[1], iquv[2], diquv[0], diquv[1], diquv[2]])
	
	rmd,rmad=	run_rmsynth(rmtdata, polyOrd=3, phiMax_radm2=1.0e3, dPhi_radm2=1.0, nSamples=100.0, weightType='variance', fitRMSF=False, noStokesI=False, phiNoise_radm2=1000000.0, \
						nBits=32, showPlots=True, debug=False, verbose=False, log=print, units='Jy/beam', prefixOut='prefixOut', saveFigures=None,fit_function='log')
	
	rmc		=	run_rmclean(rmd, rmad, 0.1, maxIter=1000, gain=0.1, nBits=32, showPlots=False, verbose=False, log=print)
	
	print(rmc[0])
	
	res		=	[rmc[0]['phiPeakPIfit_rm2'], rmc[0]['dPhiPeakPIfit_rm2'], rmc[0]['polAngle0Fit_deg'], rmc[0]['dPolAngle0Fit_deg']]
	
	return(res)	

#	---------------------------------------------------------------------------------




























































