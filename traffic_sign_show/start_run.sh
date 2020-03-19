#!/usr/bin/env bash

workdir=$(cd $(dirname $0); pwd)

#filename='/main.sh'
filename='/start.py'

echo $workdir$filename

#$(pkexec $workdir$filename)
$(sudo python3 $workdir$filename)
