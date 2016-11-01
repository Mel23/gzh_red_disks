## Documentation for how I (Mel G) created a second sample of Ferengi images to put into Galaxy Zoo in 2016. This sample was created as close as possible to the original set classified in GZ in 2013. 

Assuming you have a set of galaxies you want to ferengify, you'll need to start with their positions (ra/dec) OR their SDSS field, camcol, run, and rerun info. Relevant data needed later will include redshift and some radius for determining the size of your cutouts (I used petrorad_r90_r for mine.) 

## 1) Step 1: Downloading fits images, psf images, and tsf files
My method is outlined in the notebook python/wget_tiles.ipynb. It describes how I downloaded the fits images in the ugriz bands, psf files, and tsf files using the field/camcol/run/rerun information. If you are smart you can probably figure out how to log into SciServer and grab them without having to download them, but I am not that clever. That is for you to learn, grasshopper.


## 2) Step 2: Create cutouts of your subjects from the fits images
My script for doing this is python/ferengi_cutouts.py. Most (1194) of my original 1435 subjects could have cutouts created using a size of 2.5 * petror90_r. I then decreased the size a little to 2.0 * petror90_r to get 78 more galaxies. The rest were close to the edge of the fits frame, and it is not in my code how one might splice together multiple frames to get good images of these. That is a task for a future grasshopper. 


## 3) Step 3: Ferengify!

Once all of the cutouts have been prepped you should be all set to ferengify. Everything I used to run Ferengi is in the folder run_ferengi/. The files are as follows:

### ferengi.pro 
This is almost 100% identical to the original ferengi code which can be downloaded here http://www.mpia.de/FERENGI/

The only change came from Edmond who altered the original script in the following way: (copy/paste from an e-mail):

The only thing (I think) that I changed in the FERENGI code is the addition of poisson noise to the artificially redshifted images (instead of a assuming a normal distribution). So there is this function called "ferengi_convolve_plus_noise" within the ferengi.pro file, and the last lines are: 

;the output image is in counts/sec, and so is the sky image
   IF NOT keyword_set(nonoise) THEN $
    out += sky[0:sz_out[0]-1, 0:sz_out[1]-1]+ $
           sqrt(abs(out*exptime))*randomn(1, sz_out[0], sz_out[1])/exptime
   return, out
END

I replaced the line that starts with "out+=" with this: 

out += poidev(sky[0:sz_out[0]-1, 0:sz_out[1]-1]*exptime)/exptime +$
             poidev(out*exptime)/exptime
"

### make_jpeg.pro
Ferengi (as I ran it) outputs AEGIS equivalent I and V band fits files. make_jpeg uses those as input to output an RGB image. 

### ferengify.pro
This is the main script to read in all of the inputs required for ferengi and loop through all galaxies and redshifts desired. 

#### aegis_psfi.fits, aegis_psfv.fits, sky.fits
These are files I got from Edmond that are AEGIS psfs in I and V band and a random AEGIS sky background that are inputs in the ferengi code.

#### getstamps_color.pro, nw_arcsinh_fit.pro, nw_fit_to_box.pro
I don't know the details of these functions, but they are called in the make_jpeg.pro script and are needed to run it. 

#### sdss_psfrec.pro 
This is a script for deconstructing the sdss psfs. It's described sort of here http://www.sdss.org/dr12/algorithms/read_psf/


