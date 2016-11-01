;+
; NAME:
;   make_hdf_jpeg
; BUGS:
;   everything hard wired
;-
pro make_jpeg,i_file,v_file,outfile

; set parameters
scales= [7.9065, 7.48945, 7.0724] * 5.0
;scales= [1.0000,1.0500, 1.3000] * 40.0
nonlinearity= 2.0
resizefactor= 1.0 

;path='/home/user1/galloway/new_ferengi/'

;i_file=path+'imout_I_03.fits'
;v_file=path+'imout_V_03.fits'
;outfile=path+'test_0_3.jpg'

; read data
rim= mrdfits(i_file)
bim= mrdfits(v_file)
gim= (rim+bim)/2.00

tmp= size(rim,/dimensions)
nx= tmp[0]
ny= tmp[1]
RGBim= fltarr(nx,ny,3)
RGBim[*,*,0]= rim
RGBim[*,*,1]= gim
RGBim[*,*,2]= bim

;divide by maximum value of RGB - make_egs_jpegs doesn't even have this....
if max(RGBim) gt 1 then RGBim/=max(RGBim)

; scale and set colors
RGBim = nw_scale_rgb(RGBim,scales=scales)
RGBim = nw_arcsinh_fit(RGBim,nonlinearity=nonlinearity)
RGBim = nw_fit_to_box(RGBim,origin=origin)

; convolving by 1.3 gaussian
RGBim[*,*,0]=filter_image(RGBim[*,*,0], FWHM_GAUSSIAN=[1.33,1.33],/all)
RGBim[*,*,1]=filter_image(RGBim[*,*,1], FWHM_GAUSSIAN=[1.33,1.33],/all)
RGBim[*,*,2]=filter_image(RGBim[*,*,2], FWHM_GAUSSIAN=[1.33,1.33],/all)


; convert float to byte
RGBim = nw_float_to_byte(RGBim)



; rebin and resize
newsize = long(nx*resizefactor)

RGBim= congrid(RGBim,newsize,newsize,3)





; write
WRITE_JPEG,outfile,RGBim,TRUE=3,QUALITY=100
return
end
