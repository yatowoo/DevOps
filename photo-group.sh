#!/usr/bin/bash -

# Sort photos by Camera/manufacturer

let "start=$1*40"

exif_script="./photo-exif.py"
if [ -e $2 ];then
  exif_script=$2
fi

for no in {1..40};
do
  let "no=$no+$start";
  dir=recup_dir.$no; # Generated by PhotoRec
  if [ -e $dir ];then
    echo $dir;
    for fp in $(find $dir -name "*.jpg" -type f);do
      #cam=$(file Photo/$fp | grep -o -E "manufacturer=.*?," | cut -d',' -f1 | cut -d'=' -f2);
      cam=$($exif_script $fp)
      if [[ $cam != "" ]];then
        echo "+"$fp" "$cam;
        mkdir -p "$cam";
        mv $fp "$cam/";
      fi
    done
  else
    exit;
  fi
done
