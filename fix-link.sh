#!/bin/bash -

# Fix broken links from copy on Windows NTFS
# Input generated from:
#   ls -l `find -P [*/*/bin,lib/*so*,lib64/*so*] -size -100c | grep -v latest` \
#     | grep -v " -> " | cut -d' ' -f9 | sort
# Format: LINK_PATH

if [ $# -gt 0 ];then
  exec 0<$1;
fi

DIR=0
while read LINK || [ -n "$LINK" ]
do
  lib_dir=$(dirname $LINK)
  if [ $DIR != $lib_dir ];then
    DIR=$lib_dir;
    echo -e "\n------> "$DIR;
  fi
  LINK_NAME=$(basename $LINK);
  cd $DIR;
  # Find lib with longest name
  LEN=0 
  for name in $(ls $LINK_NAME*);
  do
    len=${#name};
    if [ $LEN -lt $len ];then
      LIB_NAME=$name
      LEN=$len
    fi
  done
  # End - Got lib name
  if [ $LIB_NAME != $LINK_NAME ];then
    ln -s -f $LIB_NAME $LINK_NAME
    echo $LIB_NAME $LINK_NAME
  else
    echo "[X] Error - Illegal lib name : "$DIR/$LIB_NAME
  fi
  cd $OLDPWD
done
