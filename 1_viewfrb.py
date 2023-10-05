#
#	Script for FRB polarization analysis
#
#								AB, April 2023

#	--------------------------	Import modules	---------------------------

import os, sys
import numpy as np
from globalpars import *
from htrfns.dynamic_fns import *
from htrfns.scintillation_fns import *
from htrfns.burstfns import *

def print_instructions():

	#	Print instructions to terminal
	
	print("\n            You probably need some assistance here!\n")
	print("\n Arguments are       --- <FRB name string> <number of channels> <f_avg> <t_avg> <t_baseline/ms>\n")	
	
	print("\n            Now let's try again!\n")
	
	return(0)

#	--------------------------	Read inputs	-------------------------------
if(len(sys.argv)<6):
	print_instructions()
	sys.exit()

frbname		=	sys.argv[1]					#	FRB name string (YYMMDDx)
nchan		=	int(sys.argv[2])			#	Number of fequency channels
ffac		=	int(sys.argv[3])			#	Averaging factor along frequency
tavgfac		=	int(sys.argv[4])			#	Averaging factor along time
tbasems		=	float(sys.argv[5])			#	Time baseline in ms

#	-------------------------	Do steps	-------------------------------

frbdm		=	-1.0
frblocms	=	-1
fmhz0		=	-1.0
	
frblist 	=	np.genfromtxt(frbcat)
for ifrb in frblist:
	if(str(int(ifrb[0]))==frbname):
		fmhz0		=	ifrb[1]
		frbdm		=	str(ifrb[3])
		frblocms	=	int(ifrb[4])		

print("FRB {} F0 = {:.2f} MHz DM = {} location = {} ms".format(frbname, fmhz0, frbdm, frblocms))

#	[Step 0]	Calculate FRB width
print("\n[Step 0] Calculating width at time resolution = {:.6f} ms".format(tavgfac*nchan*Raw_time_res_ms))
(tpeak,eqwms,w95ms,lw95ms,rw95ms,wms,lwms,rwms) = cal_width(frbname, frbdm, nchan, ffac, tavgfac,tbasems)
print("\n we = {:.3f} ms \n w = {:.3f} ms start = {:.3f} ms end = {:.3f} ms\n w95 = {:.3f} ms start95 = {:.3f} ms end95 = {:.3f} ms\n".format(eqwms,wms,lwms,rwms,w95ms,lw95ms,rw95ms))




















































