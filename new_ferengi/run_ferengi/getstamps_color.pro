
readcol, 'agn_morph_photz.txt', id, ra, dec, zz, hmag   ; id, ACSTILE, ACSID,  XCENTER, YCENTER
dx = 150  ; 150 x 150 pixel cutouts 
dy = 150

bigbfile = '../ers/gds_acs_f850w_60mas_drz.trim.fits'
biggfile = '../ers/goods_wfc3_f125w_60mas_drz.trim.fits'
bigrfile = '../ers/goods_wfc3_f160w_60mas_drz.trim.fits'

   
fits_read, bigbfile, bigbim
fits_read, biggfile, biggim
fits_read, bigrfile, bigrim, hdr   


; set parameters
scales= [1.3, 1, 3.6] * 20.0   ;  relative scaling of RGB images x brightness factor
nonlinearity= 2.0
resizefactor= 1.0 

n = N_ELEMENTS(id)
for i=0, n-1 do begin
    print, 'starting galaxy ', id[i]
    galfile = 'gal'+ string(id[i], format='(I0)') + '_' + string(zz[i], format='(F5.2)') +  '.fits'
    outfile = string(id[i], format='(I0)') + '.jpg'
    openr, 1, outfile, error=err

    if (err ne 0) then begin 

       adxy, hdr, ra[i], dec[i], xc, yc

       xmin = long(xc - dx/2.)
       xmax = xmin + dx
       ymin = long(yc - dy/2.)
       ymax = ymin + dy
  
   ;  seg = bigseg[xmin:xmax,ymin:ymax]
       bim = bigbim[xmin:xmax,ymin:ymax]
       rim = bigrim[xmin:xmax,ymin:ymax]
       gim = biggim[xmin:xmax,ymin:ymax]

       dim= size(rim, /dimensions)
       npix = dim[0]

       tmp= size(rim,/dimensions)
       nx= tmp[0]
       ny= tmp[1]
       RGBim= fltarr(nx,ny,3)
       RGBim[*,*,0]= rim
       RGBim[*,*,1]= gim
       RGBim[*,*,2]= bim
; rebin
       newsize = long(nx*resizefactor)

       RGBim= congrid(RGBim,newsize,newsize,3)

; scale and set colors
       RGBim = nw_scale_rgb(RGBim,scales=scales)
       RGBim = nw_arcsinh_fit(RGBim,nonlinearity=nonlinearity)
       RGBim = nw_fit_to_box(RGBim,origin=origin)
       RGBim = nw_float_to_byte(RGBim)

; write
       WRITE_JPEG,outfile,RGBim,TRUE=3,QUALITY=100
    endif
    close, 1

 endfor


end
