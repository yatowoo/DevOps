#!/bin/bash -

# Script to locate user by IP with QQwry database

if [ $# -gt 0 ];then
	exec 0<$1;
	#判断是否传入参数：文件名，如果传入，将该文件绑定到标准输入
fi
	 
i=0
while read line || [ -n "$line" ]
do
	ip=$(echo $line | grep -E -o "([0-9]+\.){3}[0-9]+");
	if [ -n "$ip" ] && [ "$ip" != "0.0.0.0" ] ;then
		geo=$(python2.7 $QQWry_HOME/qqwry.py -f $QQWry_DATA -q $ip | tail -1 | awk '{print $2}');
		echo $line" | "$geo;
	fi
	let "i++";
done <&0;
#通过标准输入循环读取内容
exec 0>&-;
#解除标准输入绑定
