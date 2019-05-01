#!/bin/bash -

traffic_log=kingss-traffic.log;
ping_log=kingss-ping.log
history=kingss-history.log

# Check ss traffic usage
echo '====== Check traffic usage of kingss'
echo '>>>>>> ' `date` > $traffic_log;
echo "--> Traffic usage" >> $history;
./kingss.py | grep --color=auto '已用' >> $traffic_log;
cat $traffic_log >> $history
cat $traffic_log;

# Check latency of servers by ping
echo '====== Check ping latency of kingss'
echo '>>>>>> ' `date` > $ping_log;
echo "--> Ping latency" >> $history;

sub=$(grep "server" ../private-db.json  | sed 's/[,"]/ /g' | sed 's/.*\[\(.*\)\]/\1/g')
for srv in ${sub[@]};
do
{
	i=${srv%.*}
	i=${i%.*}
	export delay_$i=`/bin/ping -c 10 $srv | tail -n1 | cut -d' ' -f4`
	eval echo -e $i'\\t'\$delay_$i ms >> $ping_log
	eval unset delay_$i
	echo '[-]INFO - Done for ' $i
} &
done
wait
cat $ping_log | tee -a $history

unset i
unset srv
unset sub
unset traffic_log
unset ping_log
unset history

echo '====== All is done!'