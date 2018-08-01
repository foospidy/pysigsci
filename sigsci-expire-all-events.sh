#!/usr/bin/env bash
###################
# Signal Sciences helper script:
# sigsci-expire-all-events.sh
# For a given site, the script will expire all flagged ip events.
# Requires:
# - pysigsci (https://pypi.org/project/pysigsci/)
# - jq (https://stedolan.github.io/jq/)

if [ -z $1 ];
then
	echo "usage: ./sigsci-expire-all-events.sh <site_name>"
	exit;
fi

for identifier in `pysigsci --get events --status active --limit 1000 --site ${1} | jq ".data[] | .id"`;
do
	id=`echo ${identifier} | tr '"' '\ '`
	pysigsci --expire-event --site ${1} --id ${id} | jq '.id + " expires " + .expires'
done;
