#!/bin/sh
fping -aqg 100.64.0.0/24|xargs -n1 nslookup |grep 'name ='|awk '{print $4}'|awk -F'.' '{print $1}'|sort