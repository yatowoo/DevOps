#!/bin/bash -

# Fix symbolic link with original link info.
# Format: LINK_PATH TARGET

if [ $# -gt 0 ];then
  exec 0<$1;
fi

DIR=0
while read INPUT || [ -n "$INPUT" ]
do
  TARGET=${INPUT#* }
  LINK_PATH=${INPUT% *}
  LINK_NAME=$(basename $LINK_PATH);
  exec_dir=$(dirname $LINK_PATH)
  if [ $DIR != $exec_dir ];then
    DIR=$exec_dir;
    echo -e "\n------> "$DIR;
  fi
  cd $DIR
  ln -s -f $TARGET $LINK_NAME
  echo $TARGET $LINK_NAME
  cd $OLDPWD
done