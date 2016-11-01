#!/bin/bash

for i in {0..1095}; do
    COMMAND="/local/site/pkg/itt/idl/idl81/bin/idl"
    ARGUMENTS="-e \"ferengify_1,$i\""
    SUBMITCOMMAND="condor_submit -a \"executable=${COMMAND}\" -a \"arguments=${ARGUMENTS}\" -a \"output=log/ferengi$i.out\" -a \"error=log/ferengi$i.error\" -a \"log=log/ferengi$i.log\" -a \"getenv=true\" ferengi.submit"
    eval "${SUBMITCOMMAND}"
    #echo "module load idl/8.1 && ${SUBMITCOMMAND}"
done
