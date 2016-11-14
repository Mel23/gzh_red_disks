import os
import sys
import numpy
import subprocess
from astropy.table import Table
from time import sleep

class JobTracker(object):


    def check_output_dir(self):
    
        path = '/data/lucifer1.1/users/galloway/new_ferengi/'
        data = Table.read(path + 'input/ferengi_candidates_stage_2_939.fits')
        #data = data[0:500]
        missing_index=[]
        for i,gal in enumerate(data):
            objid = gal['dr12objid']
            fname = path+'output/images/{}_simz_6_evo_1.jpg'.format(objid)
            if os.path.isfile(fname)==False:
                missing_index.append(i)

        return missing_index


    def grabCondorJobs(self):
        jobs = subprocess.Popen(['condor_q'],stdout=subprocess.PIPE)
        jobtmp, err = jobs.communicate()
        if jobtmp == None:
            return []
        else:
            jobinfo = jobtmp.rstrip().split('\n')[4:-2]
            joblist = [s.split(' ')[0] for s in jobinfo if s.split(' ')[3] == 'galloway']
            return joblist

    def jobIDtoIndex(self, jobID):
        #condout = subprocess.Popen(['condor_q','-l', '%s' %jobID],stdout=subprocess.PIPE)
        condout = subprocess.Popen(['condor_q','-l', '%s' %jobID],stdout=subprocess.PIPE)
        condtmp, err = condout.communicate()
        
        indices = condtmp.rstrip().split('\n')
        tmpline = [line for line in indices if 'Args' in line]
        index  = tmpline[0].split(',')[1][:-1] 
        #indtmp, err = indices.communicate()

        return index
     
    def resubmitJob(self,index):
        subout = subprocess.Popen(['sh','resubmit_ferengi.sh',str(index)],stdout=subprocess.PIPE)
        out, err = subout.communicate()


    def run(self):


        missing = self.check_output_dir()
        condor_running = self.grabCondorJobs()
    
        index_running = []
        
        for job in condor_running:
            index_running.append(self.jobIDtoIndex(job))
    
        #resubmit = list(set(missing) - set(index_running))
        print "Still missing %s jobs." % str(len(missing))
        if len(missing):
            resubmit = [m for m in missing if str(m) not in index_running]
            map(self.resubmitJob, resubmit)

        return len(missing)
    
def main():
    
    missing = 9
    while missing>0:
        Tracker = JobTracker()
        missing = Tracker.run()
        sleep(60*15) #check every 15 minutes

if __name__ == '__main__':
    main()
                                          
