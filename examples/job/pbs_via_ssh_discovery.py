#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''This examples shows how to submit a job to a PBS 
   jobmanager via ssh using a custom security context.

   If something doesn't work as expected, try to set 
   SAGA_VERBOSE=3 in your environment before you run the
   script in order to get some debug output.

   If you think you have encountered a defect, please 
   report it at: https://github.com/oweidner/bliss/issues
'''

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga as saga

def main():
    
    try:
        # list of resource that are potentially 
        # available 
        machines = {
          'xray'    : 'pbs+ssh://xray.futuregrid.org',
          'india'   : 'pbs+ssh://india.futuregrid.org',
          'alamo'   : 'pbs+ssh://alamo.futuregrid.org',
          'louie'   : 'pbs+ssh://louie.loni.org',
          'queenbee': 'pbs+ssh://queenbee.loni.org'
        }

        jobs = [] # create 100 job templates
        for i in range(100):
            jobs.append("/bin/sleep 60")
        
        # set up the security contet:
        # if no security context is defined, the PBS
        # plugin will pick up the default set of ssh 
        # credentials of the user, i.e., ~/.ssh/id_rsa
        ctx = saga.Context()
        ctx.type = saga.Context.SSH
        ctx.userid  = 'oweidner' # like 'ssh username@host ...'
        ctx.usercert = '/Users/oweidner/.ssh/id_rsa_fg' # like ssh -i ...'

        # get some infos about the machines in our 
        # list, like number of waiting jobs, architecture, etc... 
        for key in machines:
            print "\nResource: %s" % (key)
            # create a discoverer and retrieve a list
            # of available serivces 
            sdd = saga.sd.Discoverer(machines[key])
            sdd.session.contexts.append(ctx)
            services = sdd.list_services()

            for service in services:
                # for each service, get some key metrics via the
                # service data object
                data = service.get_data()

                print "  * Serivce: '%s', type: '%s', url: '%s'" \
                  % (service.name, service.type, service.url)
                print "    |- Running Jobs         : %s" \
                  % (data.get_attribute("GlueCEStateRunningJobs"))      
                print "    |- Waiting Jobs         : %s" \
                  % (data.get_attribute("GlueCEStateWaitingJobs"))      
                print "    |- Main Memory Size     : %s" \
                  % (data.get_attribute("GlueHostProcessorModel"))      
<<<<<<< HEAD
                #print "    GlueHostProcessorModel      : %s" \
                #  % (data.get_attribute("GlueHostProcessorModel"))      
                #print "    GlueHostProcessorClockSpeed : %s" \
                #  % (data.get_attribute("GlueHostProcessorClockSpeed"))      
                #print "    GlueHostArchitectureSMPSize : %s" \
                #  % (data.get_attribute("GlueHostArchitectureSMPSize"))      
=======
                print "    |- Processor Model      : %s" \
                  % (data.get_attribute("GlueHostProcessorModel"))      
                print "    |- Processor Speed      : %s" \
                  % (data.get_attribute("GlueHostProcessorClockSpeed"))      
                print "    '- CPUs/Host (SMP Size) : %s" \
                  % (data.get_attribute("GlueHostArchitectureSMPSize"))      
>>>>>>> 2f47efb6a12d75b5ca259832763529bfd8e9437d

    except saga.Exception, ex:
        print "Oh, snap! An error occured: %s" % (str(ex))

if __name__ == "__main__":
    main()

# INFO: The PBS script generated behind the scenes by the  
#       plugin looks like this (SAGA_VERBOSE=6 shows it):
#       
#         #!/bin/bash 
#         #PBS -N bliss_job 
#         #PBS -V     
#         #PBS -o bliss_pbssh_job.stdout 
#         #PBS -e bliss_pbssh_job.stderr 
#         #PBS -l walltime=0:05:00 
#         #PBS -v SLEEP_TIME=10, 
#       
#         /bin/sleep $SLEEP_TIME 
