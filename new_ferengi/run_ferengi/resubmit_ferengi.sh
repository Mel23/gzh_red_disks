#!/bin/bash

COMMAND="/local/site/pkg/itt/idl/idl81/bin/idl"
ARGUMENTS="-e \"ferengify,$1,6\""
SUBMITCOMMAND="condor_submit -a \"executable=${COMMAND}\" -a \"arguments=${ARGUMENTS}\" -a \"output=log/ferengi$i.out\" -a \"error=log/ferengi$i.error\" -a \"log=log/ferengi$i.log\" -a \"getenv=true\" ferengi.submit"
eval "${SUBMITCOMMAND}"

