#create cutouts for ferengi galaxies
#hardcode - manually enter data file with list of subjects to be cutout

import numpy as np
from astropy.table import Table,Column,join
from astropy.io import fits
import matplotlib.pyplot as plt
import bz2
import pdb
import warnings
import os.path
from matplotlib.colors import LogNorm
import matplotlib.gridspec as gridspec
from astropy import wcs

#filenames of field, psf, and tsf files for a given band, field, camcol, and run number
def field_name(r,c,f,bnd):
    fname = 'ugriz_bulk_images/frame-'+bnd+'-'+'{:06d}'.format(r)+'-'+'{:1d}'.format(c)+'-'+'{:04d}'.format(f)+'.fits.bz2'
    return fname
def psf_name(r,c,f):
    fname = 'psField_files/psField-'+'{:06d}'.format(r)+'-'+'{:1d}'.format(c)+'-'+'{:04d}'.format(f)+'.fit'
    return fname
def tsf_name_40(r,c,f):
    fname = 'tsField_files/tsField-'+'{:06d}'.format(r)+'-'+'{:1d}'.format(c)+'-'+'40-'+'{:04d}'.format(f)+'.fit'
    return fname
def tsf_name_41(r,c,f):
    fname = 'tsField_files/tsField-'+'{:06d}'.format(r)+'-'+'{:1d}'.format(c)+'-'+'41-'+'{:04d}'.format(f)+'.fit'
    return fname
def tsf_name_44(r,c,f):
    fname = 'tsField_files/tsField-'+'{:06d}'.format(r)+'-'+'{:1d}'.format(c)+'-'+'44-'+'{:04d}'.format(f)+'.fit'
    return fname

#list of subjects to be cut out. needs objid, ra, dec, field, run, camcol, redshift
data = Table.read('../input/not_edge_galaxies_2_radius_78.fits')


bands = ['u','g','r','i','z']

for i,gal in enumerate(data):
    f = gal['field']
    c = gal['camcol']
    r = gal['run']
    objid = gal['dr12objid']
    rad = gal['petror90_r']/0.396 #[pixels] #set sized based on r band radius
    ra = gal['RA']
    dec = gal['DEC']

	#write psf file (really just renaming for convenience later)

    hdu_psfname = psf_name(r,c,f)
    this_psf= fits.open(hdu_psfname)
 
    psf_out_name = '../input/psf_files/{:d}_psf.fits'.format(objid)
    this_psf.writeto(psf_out_name,clobber=True)
	
	#write tsf file (also just really renaming)
    hdu_tsfname_40 = tsf_name_40(r,c,f)
    hdu_tsfname_41 = tsf_name_41(r,c,f)
    hdu_tsfname_44 = tsf_name_44(r,c,f)
        
    if os.path.isfile(hdu_tsfname_40)==True:
        this_tsf = fits.open(hdu_tsfname_40)
    elif os.path.isfile(hdu_tsfname_41)==True:
        this_tsf = fits.open(hdu_tsfname_41)
    elif os.path.isfile(hdu_tsfname_44)==True:
        this_tsf = fits.open(hdu_tsfname_44)

    tsf_out_name = '../input/tsf_files/{:d}_tsf.fits'.format(objid)
    this_tsf.writeto(tsf_out_name,clobber=True)

	#now create the cutouts for each band
    for band in bands:
        hdu_fieldname = field_name(r,c,f,band) #name of file containing sdss tile for that band
        #decompress 
        decompressed_file = bz2.BZ2File(hdu_fieldname)
        hdulist = fits.open(decompressed_file)

        #convert from nanomaggies to counts
        conversion_factor = 1./hdulist[0].header['NMGY']    
        hdulist[0].data=hdulist[0].data*conversion_factor
        
        img = hdulist[0].data
        hdr = hdulist[0].header

		#get coordinates of subject
        w = wcs.WCS(hdr)
        pix = w.wcs_world2pix(ra, dec,1)
        row, col = int(pix[1]), int(pix[0])
	    
        #size = 2.5*radius
        size=2.5
        extents = [int(row-size*rad), int(row+size*rad), int(col-size*rad), int(col+size*rad)] 

    
        #now create the stamp!
        cutout = img[extents[0]:extents[1], extents[2]:extents[3]]

        # convert the array into a FITS image
        cutout_image = fits.ImageHDU(data=cutout, header=hdr)
        
        #write cutout to file
        name = '../input/ugriz_cutouts/{:d}_{:s}.fits'.format(objid,band)
        cutout_image.writeto(name,clobber=True)
	
    #keep track of some shit:
    if i % 10==0:
        print '{:1d} galaxies are done,yo'.format(i)

