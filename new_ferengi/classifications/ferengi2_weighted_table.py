#Kind of hard-coded...
#Counts votes according to user weights. Run 3 times.
#Zeroth run: all weights = 1
#1st run: apply weights based on ferengi2_user_weights_table
#Second run: same as second run. 

import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
import datetime

from collections import Counter


from astropy.io import fits as pyfits
from astropy.io.fits import Column
from astropy.io import ascii

print 'reading file...'
#raw classifications
data = ascii.read("data/2017-02-19_galaxy_zoo_ferengi_2_classifications.csv")

run=2

#comment out these lines if 0th run
weights=pyfits.open('data/ferengi2_user_weights_%s.fits'%run)
weight_data=weights[1].data

print 'organizing subjects...'
subjects = set(data['subject_id'])
    
print 'Creating columns for vote fractions...'
    
    # Create column of integer zeros and float zeros
intcolumn = np.zeros(len(subjects),dtype=int)
floatcolumn = np.zeros(len(subjects),dtype=float)
strcolumn = np.array([' ']*len(subjects),dtype='S24')
   #S24=24 character string 
    #c01 = Column(name='num_classifications', format='J', array=intcolumn)          # c05 = c01, by definition

#format for Columns: D = double precision floating point, J = integer
c01 = Column(name='subject_id', format='A24', array=strcolumn)          # c05 = c01, by definition

c02 = Column(name='t00_smooth_or_features_a0_smooth_frac_weighted_%s'%run, format='D', array=floatcolumn)
c03 = Column(name='t00_smooth_or_features_a1_features_frac_weighted_%s'%run, format='D', array=floatcolumn)
c04 = Column(name='t00_smooth_or_features_a2_artifact_frac_weighted_%s'%run, format='D', array=floatcolumn)
c05 = Column(name='t00_smooth_or_features_count_weighted_%s'%run, format='D', array=floatcolumn)

c06 = Column(name='t01_rounded_a0_completely_round_frac_weighted_%s'%run, format='D', array=floatcolumn)
c07 = Column(name='t01_rounded_a1_in_between_frac_weighted_%s'%run, format='D', array=floatcolumn)
c08 = Column(name='t01_rounded_a2_cigar_shaped_frac_weighted_%s'%run, format='D', array=floatcolumn)
c09 = Column(name='t01_rounded_count_weighted_%s'%run, format='D', array=floatcolumn)

c10 = Column(name='t02_clumps_a0_yes_frac_weighted_%s'%run, format='D', array=floatcolumn)
c11 = Column(name='t02_clumps_a1_no_frac_weighted_%s'%run, format='D', array=floatcolumn)
c12 = Column(name='t02_clumps_count_weighted_%s'%run, format='D', array=floatcolumn)

c13 = Column(name='t03_clumps_number_a0_1_frac_weighted_%s'%run, format='D', array=floatcolumn)
c14 = Column(name='t03_clumps_number_a1_2_frac_weighted_%s'%run, format='D', array=floatcolumn)
c15 = Column(name='t03_clumps_number_a2_3_frac_weighted_%s'%run, format='D', array=floatcolumn)
c16 = Column(name='t03_clumps_number_a3_4_frac_weighted_%s'%run, format='D', array=floatcolumn)
c17 = Column(name='t03_clumps_number_a4_more_than_4_frac_weighted_%s'%run, format='D', array=floatcolumn)
c18 = Column(name='t03_clumps_number_a5_cant_tell_frac_weighted_%s'%run, format='D', array=floatcolumn)
c19 = Column(name='t03_clumps_number_count_weighted_%s'%run, format='D', array=floatcolumn)

c20 = Column(name='t04_clump_arrangement_a0_straight_line_frac_weighted_%s'%run, format='D', array=floatcolumn)
c21 = Column(name='t04_clump_arrangement_a1_chain_frac_weighted_%s'%run, format='D', array=floatcolumn)
c22 = Column(name='t04_clump_arrangement_a2_cluster_irregular_frac_weighted_%s'%run, format='D', array=floatcolumn)
c23 = Column(name='t04_clump_arrangement_a3_spiral_frac_weighted_%s'%run, format='D', array=floatcolumn)
c24 = Column(name='t04_clump_arrangement_count_weighted_%s'%run, format='D', array=floatcolumn)

c25 = Column(name='t05_bright_clump_a0_yes_frac_weighted_%s'%run, format='D', array=floatcolumn)
c26 = Column(name='t05_bright_clump_a1_no_frac_weighted_%s'%run, format='D', array=floatcolumn)
c27 = Column(name='t05_bright_clump_count_weighted_%s'%run, format='D', array=floatcolumn)

c28 = Column(name='t06_bright_clump_central_a0_yes_frac_weighted_%s'%run, format='D', array=floatcolumn)
c29 = Column(name='t06_bright_clump_central_a1_no_frac_weighted_%s'%run, format='D', array=floatcolumn)
c30 = Column(name='t06_bright_clump_central_count_weighted_%s'%run, format='D', array=floatcolumn)

c31 = Column(name='t07_clump_symmetrical_a0_yes_frac_weighted_%s'%run, format='D', array=floatcolumn)
c32 = Column(name='t07_clump_symmetrical_a1_no_frac_weighted_%s'%run, format='D', array=floatcolumn)
c33 = Column(name='t07_clump_symmetrical_count_weighted_%s'%run, format='D', array=floatcolumn)

c34 = Column(name='t08_clump_embedded_a0_yes_frac_weighted_%s'%run, format='D', array=floatcolumn)
c35 = Column(name='t08_clump_embedded_a1_no_frac_weighted_%s'%run, format='D', array=floatcolumn)
c36 = Column(name='t08_clump_embedded_count_weighted_%s'%run, format='D', array=floatcolumn)

c37 = Column(name='t09_disk_edge_on_a0_yes_frac_weighted_%s'%run, format='D', array=floatcolumn)
c38 = Column(name='t09_disk_edge_on_a1_no_frac_weighted_%s'%run, format='D', array=floatcolumn)
c39 = Column(name='t09_disk_edge_on_count_weighted_%s'%run, format='D', array=floatcolumn)

c40 = Column(name='t10_bulge_shape_a0_rounded_frac_weighted_%s'%run, format='D', array=floatcolumn)
c41 = Column(name='t10_bulge_shape_a1_boxy_frac_weighted_%s'%run, format='D', array=floatcolumn)
c42 = Column(name='t10_bulge_shape_a2_no_bulge_frac_weighted_%s'%run, format='D', array=floatcolumn)
c43 = Column(name='t10_bulge_shape_count_weighted_%s'%run, format='D', array=floatcolumn)

c44 = Column(name='t11_bar_a0_bar_frac_weighted_%s'%run, format='D', array=floatcolumn)
c45 = Column(name='t11_bar_a1_no_bar_frac_weighted_%s'%run, format='D', array=floatcolumn)
c46 = Column(name='t11_bar_count_weighted_%s'%run, format='D', array=floatcolumn)

c47 = Column(name='t12_spiral_a0_spiral_frac_weighted_%s'%run, format='D', array=floatcolumn)
c48 = Column(name='t12_spiral_a1_no_spiral_frac_weighted_%s'%run, format='D', array=floatcolumn)
c49 = Column(name='t12_spiral_count_weighted_%s'%run, format='D', array=floatcolumn)

c50 = Column(name='t13_arms_winding_a0_tight_frac_weighted_%s'%run, format='D', array=floatcolumn)
c51 = Column(name='t13_arms_winding_a1_medium_frac_weighted_%s'%run, format='D', array=floatcolumn)
c52 = Column(name='t13_arms_winding_a2_loose_frac_weighted_%s'%run, format='D', array=floatcolumn)
c53 = Column(name='t13_arms_winding_count_weighted_%s'%run, format='D', array=floatcolumn)

c54 = Column(name='t14_arms_number_a0_1_frac_weighted_%s'%run, format='D', array=floatcolumn)
c55 = Column(name='t14_arms_number_a1_2_frac_weighted_%s'%run, format='D', array=floatcolumn)
c56 = Column(name='t14_arms_number_a2_3_frac_weighted_%s'%run, format='D', array=floatcolumn)
c57 = Column(name='t14_arms_number_a3_4_frac_weighted_%s'%run, format='D', array=floatcolumn)
c58 = Column(name='t14_arms_number_a4_more_than_4_frac_weighted_%s'%run, format='D', array=floatcolumn)
c59 = Column(name='t14_arms_number_a5_cant_tell_frac_weighted_%s'%run, format='D', array=floatcolumn)
c60 = Column(name='t14_arms_number_count_weighted_%s'%run, format='D', array=floatcolumn)

c61 = Column(name='t15_bulge_prominence_a0_no_bulge_frac_weighted_%s'%run, format='D', array=floatcolumn)
c62 = Column(name='t15_bulge_prominence_a1_obvious_frac_weighted_%s'%run, format='D', array=floatcolumn)
c63 = Column(name='t15_bulge_prominence_a2_dominant_frac_weighted_%s'%run, format='D', array=floatcolumn)
c64 = Column(name='t15_bulge_prominence_count_weighted_%s'%run, format='D', array=floatcolumn)

c65 = Column(name='t16_discuss_a0_yes_frac_weighted_%s'%run, format='D', array=floatcolumn)
c66 = Column(name='t16_discuss_a1_no_frac_weighted_%s'%run, format='D', array=floatcolumn)
c67 = Column(name='t16_discuss_count_weighted_%s'%run, format='D', array=floatcolumn)

c68 = Column(name='t17_odd_a0_yes_frac_weighted_%s'%run, format='D', array=floatcolumn)
c69 = Column(name='t17_odd_a1_no_frac_weighted_%s'%run, format='D', array=floatcolumn)
c70 = Column(name='t17_odd_count_weighted_%s'%run, format='D', array=floatcolumn)

c71 = Column(name='t18_odd_feature_x0_ring_frac_weighted_%s'%run, format='D', array=floatcolumn)
c72 = Column(name='t18_odd_feature_x1_lens_frac_weighted_%s'%run, format='D', array=floatcolumn)
c73 = Column(name='t18_odd_feature_x2_disturbed_frac_weighted_%s'%run, format='D', array=floatcolumn)
c74 = Column(name='t18_odd_feature_x3_irregular_frac_weighted_%s'%run, format='D', array=floatcolumn)
c75 = Column(name='t18_odd_feature_x4_other_frac_weighted_%s'%run, format='D', array=floatcolumn)
c76 = Column(name='t18_odd_feature_x5_merger_frac_weighted_%s'%run, format='D', array=floatcolumn)
c77 = Column(name='t18_odd_feature_x6_dustlane_frac_weighted_%s'%run, format='D', array=floatcolumn)
c78 = Column(name='t18_odd_feature_a0_discuss_frac_weighted_%s'%run, format='D', array=floatcolumn)
c79 = Column(name='t18_odd_feature_count_weighted_%s'%run, format='D', array=floatcolumn)

    
frac_dict = {
        'ferengi-0':{
            'a-0':'t00_smooth_or_features_a0_smooth_frac_weighted_%s'%run,
            'a-1':'t00_smooth_or_features_a1_features_frac_weighted_%s'%run,
            'a-2':'t00_smooth_or_features_a2_artifact_frac_weighted_%s'%run,
            'count':'t00_smooth_or_features_count_weighted_%s'%run
         }
        ,
        'ferengi-1':{
            'a-0':'t01_rounded_a0_completely_round_frac_weighted_%s'%run,
            'a-1':'t01_rounded_a1_in_between_frac_weighted_%s'%run,
            'a-2':'t01_rounded_a2_cigar_shaped_frac_weighted_%s'%run,
            'count':'t01_rounded_count_weighted_%s'%run
        }
	,
        'ferengi-2':{
            'a-0':'t02_clumps_a0_yes_frac_weighted_%s'%run,
            'a-1':'t02_clumps_a1_no_frac_weighted_%s'%run,
            'count':'t02_clumps_count_weighted_%s'%run
        }
        ,
        'ferengi-3':{
            'a-0':'t03_clumps_number_a0_1_frac_weighted_%s'%run,
            'a-1':'t03_clumps_number_a1_2_frac_weighted_%s'%run,
            'a-2':'t03_clumps_number_a2_3_frac_weighted_%s'%run,
            'a-3':'t03_clumps_number_a3_4_frac_weighted_%s'%run,
            'a-4':'t03_clumps_number_a4_more_than_4_frac_weighted_%s'%run,
            'a-5':'t03_clumps_number_a5_cant_tell_frac_weighted_%s'%run,
            'count':'t03_clumps_number_count_weighted_%s'%run
        }
        ,
        'ferengi-4':{
            'a-0':'t04_clump_arrangement_a0_straight_line_frac_weighted_%s'%run,
            'a-1':'t04_clump_arrangement_a1_chain_frac_weighted_%s'%run,
            'a-2':'t04_clump_arrangement_a2_cluster_irregular_frac_weighted_%s'%run,
            'a-3':'t04_clump_arrangement_a3_spiral_frac_weighted_%s'%run,
            'count':'t04_clump_arrangement_count_weighted_%s'%run
        }
        ,
        'ferengi-5':{
            'a-0':'t05_bright_clump_a0_yes_frac_weighted_%s'%run,
            'a-1':'t05_bright_clump_a1_no_frac_weighted_%s'%run,
            'count':'t05_bright_clump_count_weighted_%s'%run
        }
        ,
        'ferengi-6':{
            'a-0':'t06_bright_clump_central_a0_yes_frac_weighted_%s'%run,
            'a-1':'t06_bright_clump_central_a1_no_frac_weighted_%s'%run,
            'count':'t06_bright_clump_central_count_weighted_%s'%run
        }
        ,
        'ferengi-7':{
            'a-0':'t07_clump_symmetrical_a0_yes_frac_weighted_%s'%run,
            'a-1':'t07_clump_symmetrical_a1_no_frac_weighted_%s'%run,
            'count':'t07_clump_symmetrical_count_weighted_%s'%run
        }
        ,
        'ferengi-8':{
            'a-0':'t08_clump_embedded_a0_yes_frac_weighted_%s'%run,
            'a-1':'t08_clump_embedded_a1_no_frac_weighted_%s'%run,
            'count':'t08_clump_embedded_count_weighted_%s'%run
        }
        ,
        'ferengi-9':{
            'a-0':'t09_disk_edge_on_a0_yes_frac_weighted_%s'%run,
            'a-1':'t09_disk_edge_on_a1_no_frac_weighted_%s'%run,
            'count':'t09_disk_edge_on_count_weighted_%s'%run
        }
        ,
        'ferengi-10':{
            'a-0':'t10_bulge_shape_a0_rounded_frac_weighted_%s'%run,
            'a-1':'t10_bulge_shape_a1_boxy_frac_weighted_%s'%run,
            'a-2':'t10_bulge_shape_a2_no_bulge_frac_weighted_%s'%run,
            'count':'t10_bulge_shape_count_weighted_%s'%run
        }
        ,
        'ferengi-11':{
            'a-0':'t11_bar_a0_bar_frac_weighted_%s'%run,
            'a-1':'t11_bar_a1_no_bar_frac_weighted_%s'%run,
            'count':'t11_bar_count_weighted_%s'%run
        }
        ,
        'ferengi-12':{
            'a-0':'t12_spiral_a0_spiral_frac_weighted_%s'%run,
            'a-1':'t12_spiral_a1_no_spiral_frac_weighted_%s'%run,
            'count':'t12_spiral_count_weighted_%s'%run
        }
        ,
        'ferengi-13':{
            'a-0':'t13_arms_winding_a0_tight_frac_weighted_%s'%run,
            'a-1':'t13_arms_winding_a1_medium_frac_weighted_%s'%run,
            'a-2':'t13_arms_winding_a2_loose_frac_weighted_%s'%run,
            'count':'t13_arms_winding_count_weighted_%s'%run
        }
	,
        'ferengi-14':{
            'a-0':'t14_arms_number_a0_1_frac_weighted_%s'%run,
            'a-1':'t14_arms_number_a1_2_frac_weighted_%s'%run,
            'a-2':'t14_arms_number_a2_3_frac_weighted_%s'%run,
            'a-3':'t14_arms_number_a3_4_frac_weighted_%s'%run,
            'a-4':'t14_arms_number_a4_more_than_4_frac_weighted_%s'%run,
            'a-5':'t14_arms_number_a5_cant_tell_frac_weighted_%s'%run,
            'count':'t14_arms_number_count_weighted_%s'%run
        }
	,
        'ferengi-15':{
            'a-0':'t15_bulge_prominence_a0_no_bulge_frac_weighted_%s'%run,
            'a-1':'t15_bulge_prominence_a1_just_noticeable_frac_weighted_%s'%run,
            'a-2':'t15_bulge_prominence_a2_obvious_frac_weighted_%s'%run,
            'a-3':'t15_bulge_prominence_a3_dominant_frac_weighted_%s'%run,
            'count':'t15_bulge_prominence_count_weighted_%s'%run
        }
        ,
        'ferengi-16':{
            'a-0':'t16_discuss_a0_yes_frac_weighted_%s'%run,
            'a-1':'t16_discuss_a1_no_frac_weighted_%s'%run,
            'count':'t16_discuss_count_weighted_%s'%run
        }
	,
        'ferengi-17':{
            'a-0':'t17_odd_a0_yes_frac_weighted_%s'%run,
            'a-1':'t17_odd_a1_no_frac_weighted_%s'%run,
            'count':'t17_odd_count_weighted_%s'%run
        }
        ,
        'ferengi-18':{
            'x-0':'t18_odd_feature_x0_ring_frac_weighted_%s'%run,
            'x-1':'t18_odd_feature_x1_lens_frac_weighted_%s'%run,
            'x-2':'t18_odd_feature_x2_disturbed_frac_weighted_%s'%run,
            'x-3':'t18_odd_feature_x3_irregular_frac_weighted_%s'%run,
            'x-4':'t18_odd_feature_x4_other_frac_weighted_%s'%run,
            'x-5':'t18_odd_feature_x5_merger_frac_weighted_%s'%run,
            'x-6':'t18_odd_feature_x6_dustlane_frac_weighted_%s'%run,
            'a-0':'t18_odd_feature_a0_discuss_frac_weighted_%s'%run,
            'count':'t18_odd_feature_count_weighted_%s'%run
        }
}
    
    
classifications = pyfits.new_table([c01,c02,c03,c04,c05,c06,c07,c08,c09,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29,c30,c31,c32,c33,c34,c35,c36,c37,c38,c39,c40,c41,c42,c43,c44,c45,c46,c47,c48,c49,c50,c51,c52,c53,c54,c55,c56,c57,c58,c59,c60,c61,c62,c63,c64,c65,c66,c67,c68,c69,c70,c71,c72,c73,c74,c75,c76,c77,c78,c79])

subjDB = pyfits.new_table(classifications.columns)
questions = ['ferengi-%i' % j for j in np.arange(len(frac_dict))]
questions.remove('ferengi-18')
dupsubjects=[] #get list of subjects which have duplicates for reference

#open csv file for checking on status of code

for idx,s in enumerate(subjects):
	#record every 1000th iteration in ferengi_status.csv
    if idx % 1000 == 0:
	with open('ferengi_status.csv','w') as fp:
		a=csv.writer(fp,delimiter=',')
		a.writerow([idx])

        # Find each classification for this subject
    this_subj = (data['subject_id'] == s)

    subjDB.data.field('subject_id')[idx] = s

    #Find duplicates (cases where the same user classifies a subject more than once)
    users=[]
    dup=[]
#create list of users for each subject
    for row in data[this_subj]:
        users.append(row[2])
#determine if a user appears twice
    for person in set(users):
        if users.count(person)>1:
            dup.append(person)
#redefine data[this_subj] because reasons
    data_this_subj=data[this_subj]
#if any duplicates are found, mask data from user's ealier classification(s)
    if len(dup)>0:
        dupsubjects.append(s)
        for person in dup:
            dates=(data_this_subj['user']==person)
            latestdate=max(data_this_subj[dates]['created_at'])
            for i,row in enumerate(data_this_subj):
                #if the user is a duplicate person *and* the classification date is not the latest date option, mask the row
                if row['user']==person and row['created_at']<latestdate:
                    data_this_subj.remove_row(i)
    
        # Loop over each question in the tree and record count, vote fractions
    for q in questions:
        ctr=Counter(data_this_subj[q].compressed())
        N_total=0
        for row in data_this_subj:
            answer=str(row[q])
            if answer!='--':#if question was answered
                if run==0:
                    N_total+=1.0
                else:#apply weights to total
                    thisuserweight=(weight_data['user']==row['user'])
                    N_total+=weight_data[thisuserweight]['weight'][0] # calculate weighted total votes for questions q
                for key in ctr.keys(): #calculate weighted vote 
                    if row[q]==key:
                        try:
                            if run==0:
                                subjDB.data.field(frac_dict[q][key])[idx] += 1.0
                            else: #apply weight
                                subjDB.data.field(frac_dict[q][key])[idx] += weight_data[thisuserweight]['weight'][0]
                        except KeyError:
                            pass
        subjDB.data.field(frac_dict[q]['count'])[idx] = N_total
        for key in ctr.keys():
            try: #last divide total votes by N_total to get fraction
                subjDB.data.field(frac_dict[q][key])[idx] = subjDB.data.field(frac_dict[q][key])[idx]/float(N_total) if N_total > 0 else 0.
            except KeyError:
                pass
     #    Question 18 (odd features) is treated differently, since more than one answer can be selected
    N_total=0
    for row in data_this_subj: #check each user
    	if str(row['ferengi-18'])!='--': #see if this user answered question 18
            if run==0: #no user weighting
                N_total+=1
            else: #apply weighting
                thisuserweight=(weight_data['user']==row['user'])
                N_total+=weight_data[thisuserweight]['weight'][0] # calculate weighted total votes for question 18
            answers = str(row['ferengi-18'])
            split_answers=answers.split(';')
            for sk in split_answers: #check each of the answers found for 18
                try:
                    if run==0: #no weighting
                        subjDB.data.field(frac_dict['ferengi-18'][sk])[idx] += 1.0
                    else: #apply weight
                        subjDB.data.field(frac_dict['ferengi-18'][sk])[idx] += weight_data[thisuserweight]['weight'][0]
                except KeyError:
                    pass
    subjDB.data.field(frac_dict['ferengi-18']['count'])[idx] = N_total
    for sk in split_answers: #last divide by N_total
    	try:
    		subjDB.data.field(frac_dict['ferengi-18'][sk])[idx] = subjDB.data.field(frac_dict['ferengi-18'][sk])[idx]/float(N_total) if N_total > 0 else 0.
        except KeyError:
            pass

print 'Finished looping over classifications'
    
    # Write final data to FITS file
subjDB.writeto('data/ferengi2_combined_votes_weighted_%s.fits'%run,clobber=True)
