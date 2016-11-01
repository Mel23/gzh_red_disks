pro ferengify_1, q

path = '/data/lucifer1.1/users/galloway/new_ferengi/'

; stuff that doesn't change:
sdss_exposure_times=fltarr(5)+53.907456

fits_read,'sky.fit',sky
 
fits_read,'aegis_psfi.fits',aegis_psfi
aegis_psfi=aegis_psfi/total(aegis_psfi)
 
fits_read,'aegis_psfv.fits',aegis_psfv
aegis_psfv=aegis_psfv/total(aegis_psfv)

; path to galaxy files:
ugriz_path = path +'input/ugriz_cutouts/'
psf_path= path + 'input/psf_files/'
tsf_path= path + 'input/tsf_files/'

;path for results to be stored:

out_path = path+ 'output/'

; loop through 20 galaxies!


    ;this galaxy's objid, row, col, redshift:
a=mrdfits(path+'input/remaining_ferengi_subjects.fits',1,row=[q]) 
objid=a.dr12objid 
row=a.rowc_r
col=a.colc_r 
z_lo=a.redshift 

tsf_filename=tsf_path+strtrim(objid,1)+'_tsf.fits' 
tsf=mrdfits(tsf_filename,1)
zeropoints=-1*tsf.aa 


; read in files 
fits_read,ugriz_path+strtrim(objid,1)+'_u.fits',u 
fits_read,ugriz_path+strtrim(objid,1)+'_g.fits',g
fits_read,ugriz_path+strtrim(objid,1)+'_r.fits',r 
fits_read,ugriz_path+strtrim(objid,1)+'_i.fits',i
fits_read,ugriz_path+strtrim(objid,1)+'_z.fits',z

im = [[[u]],[[g]],[[r]],[[i]],[[z]]]

imuerr = sqrt( (u + tsf.sky[0])/tsf.gain[0] + tsf.dark_variance[0] + tsf.skyErr[0]) 
imgerr = sqrt( (g + tsf.sky[1])/tsf.gain[1] + tsf.dark_variance[1] + tsf.skyErr[1]) 
imrerr = sqrt( (r + tsf.sky[2])/tsf.gain[2] + tsf.dark_variance[2] + tsf.skyErr[2]) 
imierr = sqrt( (i + tsf.sky[3])/tsf.gain[3] + tsf.dark_variance[3] + tsf.skyErr[3]) 
imzerr = sqrt( (z + tsf.sky[4])/tsf.gain[4] + tsf.dark_variance[4] + tsf.skyErr[4]) 

imerr = [[[imuerr]],[[imgerr]],[[imrerr]],[[imierr]],[[imzerr]]] 
delvar, u,imuerr,g,imgerr,r,imrerr,i,imierr,z,imzerr 
  ;  imerr = sqrt(abs(im)) & $

psf_filename=psf_path+strtrim(objid,1)+'_psf.fits' 

;find smallest psf
psfinfo = mrdfits(psf_filename,6) 
min_fwhm = min(psfinfo.psf_width,min_fwhm_index) 
IF (min_fwhm_index=0) THEN BEGIN 
    p=mrdfits(psf_filename,0) 
    p=sdss_psfrec(p,row,col) 
    p=p/total(p) 
    psflo = [[[p]],[[p]],[[p]],[[p]],[[p]]] 
ENDIF ELSE IF (min_fwhm_index=1) THEN BEGIN 
    p=mrdfits(psf_filename,1) 
    p=sdss_psfrec(p,row,col) 
    p=p/total(p) 
    psflo = [[[p]],[[p]],[[p]],[[p]],[[p]]] 
ENDIF ELSE IF (min_fwhm_index=2) THEN BEGIN 
    p=mrdfits(psf_filename,2)
    p=sdss_psfrec(p,row,col) 
    p=p/total(p) 
    psflo = [[[p]],[[p]],[[p]],[[p]],[[p]]] 
ENDIF ELSE IF (min_fwhm_index=3) THEN BEGIN 
    p=mrdfits(psf_filename,3) 
    p=sdss_psfrec(p,row,col) 
    p=p/total(p) 
    psflo = [[[p]],[[p]],[[p]],[[p]],[[p]]] 
ENDIF ELSE IF (min_fwhm_index=4) THEN BEGIN 
    p=mrdfits(psf_filename,4) 
    p=sdss_psfrec(p,row,col) 
    p=p/total(p) 
    psflo = [[[p]],[[p]],[[p]],[[p]],[[p]]] 
ENDIF

delvar, p  ; remove psf component variable

; Ferengify from z=0.3 to 1
evo = 1 
FOR k=3,10 DO BEGIN 
    simz=strtrim(k,1) 
    evo_str=strtrim(evo,1) 

    i_file = out_path + 'fits_files/'+strtrim(objid,1)+'_imout_I_simz_' + simz + '_evo_' + evo_str + '.fits' 
    i_psf_file = out_path +'psf_files/'+strtrim(objid,1)+'_psfout_I_simz_' + simz + '_evo_' + evo_str + '.fits' 
    v_file = out_path +'fits_files/'+strtrim(objid,1)+'_imout_V_simz_' + simz +  '_evo_' + evo_str + '.fits' 
    v_psf_file = out_path +'psf_files/'+strtrim(objid,1)+ '_psfout_V_simz_' + simz + '_evo_' + evo_str +  '.fits' 
    outfile = out_path +'images/'+strtrim(objid,1) + '_simz_' + simz +  '_evo_' + evo_str + '.jpg' 

;I band
    ferengi, sky, im, imerr, psflo, [.05,.02,.02,.02,.03],aegis_psfi, [3561.,4718,6185,7501,8962],    ['sdss_u0.par','sdss_g0.par','sdss_r0.par','sdss_i0.par','sdss_z0.par'],z_lo,.396,zeropoints,sdss_exposure_times,8140.,'clash_acs_f814w.par',k/10.,.03,25.937,2100.,i_file,i_psf_file,evo=-1*evo 

;V band
    ferengi, sky, im, imerr, psflo, [.05,.02,.02,.02,.03],aegis_psfv, [3561.,4718,6185,7501,8962],    ['sdss_u0.par','sdss_g0.par','sdss_r0.par','sdss_i0.par','sdss_z0.par'],z_lo,.396,zeropoints,sdss_exposure_times,6060.,'clash_acs_f606w.par',k/10.,.03,26.486,22600.,v_file,v_psf_file,evo=-1*evo 

;make images

    make_jpeg, i_file, v_file, outfile
    ENDFOR
END

