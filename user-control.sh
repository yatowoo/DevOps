#!/bin/bash -

# Script for user control
# Option: add, del, unlock, ps

if [ -n "$1" ]  && [ -n "$2" ];then
  set -v
  USER_NAME=$2
  USER_HOME=$(getent passwd "$USER_NAME" | cut -d':' -f6)
  case $1 in
    del)
      echo '[-] Check user id'
      id $USER_NAME;
      echo '[-] Lock user password'
      passwd -l $USER_NAME;
      echo '[-] Backup home dir. : '$USER_HOME;
      echo "tar -zcf /root/backup/$USER_home.tar.gz $USER_HOME";
      echo '[-] Check running process owned by '$USER_NAME
      pgrep -u $USER_NAME
      ps -fp $(pgrep -u $USER_NAME)
      echo '[-] KILL all process owned by '$USER_NAME
      echo "killall -KILL -u $USER_NAME"
      echo '[-] Delete crontab jobs owned by '$USER_NAME
      echo "crontab -r -u $USER_NAME"
      echo '[-] Delete user : '$USER_NAME
      echo "userdel -r $USER_NAME";;
  esac
  set +v
fi