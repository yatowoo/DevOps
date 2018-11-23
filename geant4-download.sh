#!/bin/bash - 

DATADIR=~/GEANT4/downloads
for url in $(cat G4DataList.txt);
do
{
	echo '[-] Check ' $(basename $url)
	echo '--> '$url
	if [ -e $DATADIR/$(basename $url) ] ; then
	  echo '--> File exists - nothing to do'	
		continue
	fi
	status=$(curl -s --head $url | head -n1 | cut -d' ' -f2)
	if [ $status -eq 200 ] ; then
		echo '--> Connection success, start downloading'
		curl -s $url -o $DATADIR/$(basename $url)
		echo '--> Download compelted.'
	else
		echo '[X] Error '$status' - Failed to connect source.'
		echo '-->'$url
	fi
} 
done
