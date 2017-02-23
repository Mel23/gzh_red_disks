import sys
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import datetime

from astropy.table import Table
from astropy.io.fits import Column
from astropy.io import fits as pyfits
from astropy.io import ascii

#Feb 21 2017 - Code to weight user's votes based on consistency in ferengi catalogue
#Input = table of raw classifications (.csv) and table of combined vote fracctions (.fits) 
#Output = table of user names and their weights 
print 'reading data...'

data = ascii.read("data/2017-02-19_galaxy_zoo_ferengi_2_classifications.csv")
vf=Table.read('data/ferengi2_combined_votes_weighted_1.fits')


#rename columns....k

oldnames=vf.colnames

print 'renaming columns...'

for i in range(1,4):
    vf.rename_column(oldnames[i],'ferengi-0;a-{}'.format(i-1))
for i in range(5,8):
    vf.rename_column(oldnames[i],'ferengi-1;a-{}'.format(i-5))
for i in range(9,11):
    vf.rename_column(oldnames[i],'ferengi-2;a-{}'.format(i-9))
for i in range(12,18):
    vf.rename_column(oldnames[i],'ferengi-3;a-{}'.format(i-12))
for i in range(19,23):
    vf.rename_column(oldnames[i],'ferengi-4;a-{}'.format(i-19))
for i in range(24,26):
    vf.rename_column(oldnames[i],'ferengi-5;a-{}'.format(i-24))
for i in range(27,29):
    vf.rename_column(oldnames[i],'ferengi-6;a-{}'.format(i-27))
for i in range(30,32):
    vf.rename_column(oldnames[i],'ferengi-7;a-{}'.format(i-30))
for i in range(33,35):
    vf.rename_column(oldnames[i],'ferengi-8;a-{}'.format(i-33))
for i in range(36,38):
    vf.rename_column(oldnames[i],'ferengi-9;a-{}'.format(i-36))
for i in range(39,42):
    vf.rename_column(oldnames[i],'ferengi-10;a-{}'.format(i-39))
for i in range(43,45):
    vf.rename_column(oldnames[i],'ferengi-11;a-{}'.format(i-43))
for i in range(46,48):
    vf.rename_column(oldnames[i],'ferengi-12;a-{}'.format(i-46))
for i in range(49,52):
    vf.rename_column(oldnames[i],'ferengi-13;a-{}'.format(i-49))
for i in range(53,59):
    vf.rename_column(oldnames[i],'ferengi-14;a-{}'.format(i-53))
for i in range(60,63):
    vf.rename_column(oldnames[i],'ferengi-15;a-{}'.format(i-60))
for i in range(64,66):
    vf.rename_column(oldnames[i],'ferengi-16;a-{}'.format(i-64))
for i in range(67,69):
    vf.rename_column(oldnames[i],'ferengi-17;a-{}'.format(i-67))
   

users=list(set(data['user']))

strcolumn=np.array([' ']*len(users),dtype='S50')
floatcolumn=np.zeros(len(users),dtype=float)

c1 = Column(name='user', format='A50', array=strcolumn)   
c2 = Column(name='kappa', format='D', array=floatcolumn)   
c3 = Column(name='weight', format='D', array=floatcolumn)   

weightcols=pyfits.new_table([c1,c2,c3])
weight_table=pyfits.new_table(weightcols.columns)

def get_kappa(usersanswer,allanswers,X,N_answers):
    kappa=[]
    for j in range(0,N_answers):
        if usersanswer=='a-%i' % j:
            kappa.append(allanswers['ferengi-%i;a-%i' % (X,j)][0])
        else:
            kappa.append(1-allanswers['ferengi-%i;a-%i' % (X,j)][0])
    return(sum(kappa)/len(kappa))


for i,u in enumerate(users):
    if i % 1000==0:
        print i, datetime.datetime.now().strftime('%H:%M:%S.%f')
    weight_table.data.field('user')[i]=u
    this_user=(data['user']==u)

#we don't consider ferengi-16 (asks the user if they want to discuss the object) or ferengi-18 (the odd feature question, since multiple responses may be entered.) 

    kappa_this_user=[]
    for row in data[this_user]:
        these_votes=(vf['subject_id']==row['subject_id'])
        vf_tv=vf[these_votes]
        if row['ferengi-0']!=' ':
            kappa_this_user.append(get_kappa(row['ferengi-0'],vf_tv,0,3))
        if row['ferengi-1']!=' ':                            
            kappa_this_user.append(get_kappa(row['ferengi-1'],vf_tv,1,3))
        if row['ferengi-2']!=' ':                            
            kappa_this_user.append(get_kappa(row['ferengi-2'],vf_tv,2,2))
        if row['ferengi-3']!=' ':                            
            kappa_this_user.append(get_kappa(row['ferengi-3'],vf_tv,3,6))
        if row['ferengi-4']!=' ':                            
            kappa_this_user.append(get_kappa(row['ferengi-4'],vf_tv,4,4))
        if row['ferengi-5']!=' ':                            
            kappa_this_user.append(get_kappa(row['ferengi-5'],vf_tv,5,2))
        if row['ferengi-6']!=' ':                            
            kappa_this_user.append(get_kappa(row['ferengi-6'],vf_tv,6,2))
        if row['ferengi-7']!=' ':                            
            kappa_this_user.append(get_kappa(row['ferengi-7'],vf_tv,7,2))
        if row['ferengi-8']!=' ':                            
            kappa_this_user.append(get_kappa(row['ferengi-8'],vf_tv,8,2))
        if row['ferengi-9']!=' ':                           
            kappa_this_user.append(get_kappa(row['ferengi-9'],vf_tv,9,2))
        if row['ferengi-10']!=' ':                           
            kappa_this_user.append(get_kappa(row['ferengi-10'],vf_tv,10,3))
        if row['ferengi-11']!=' ':                           
            kappa_this_user.append(get_kappa(row['ferengi-11'],vf_tv,11,2))
        if row['ferengi-12']!=' ':                           
            kappa_this_user.append(get_kappa(row['ferengi-12'],vf_tv,12,2))
        if row['ferengi-13']!=' ':                           
            kappa_this_user.append(get_kappa(row['ferengi-13'],vf_tv,13,3))
        if row['ferengi-14']!=' ':                           
            kappa_this_user.append(get_kappa(row['ferengi-14'],vf_tv,14,6))
        if row['ferengi-15']!=' ':                           
            kappa_this_user.append(get_kappa(row['ferengi-15'],vf_tv,15,3))
        if row['ferengi-17']!=' ':                           
            kappa_this_user.append(get_kappa(row['ferengi-17'],vf_tv,17,2))
	kappa=sum(kappa_this_user)/len(kappa_this_user)
  	try:
        	weight_table.data.field('kappa')[i]=sum(kappa_this_user)/len(kappa_this_user)
    	except ZeroDivisionError:
        	pass
    	weight_table.data.field('weight')[i]=min(1,(kappa/0.6)**8.5)
	
weight_table.writeto('data/ferengi_user_weights_2.fits',clobber=True)

	



