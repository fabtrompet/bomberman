#!/bin/bash
tempo=1
diames=`date +%G%m%d`
mod=`stat TCC/Dados/$diames | grep Modify`
mudanca="1"
while :
do
sleep $tempo
tempo=1
diames=`date +%G%m%d`
mod2=`stat TCC/Dados/$diames | grep Modify`
if [ "$mod" != "$mod2" ]; then
	clear
	tempo=20
	mod=$mod2;
	arquivo1=`ls TCC/Dados/$diames/ | tail -2 | head -1`;
	arquivo2=`ls TCC/Dados/$diames/ | tail -1`;
	echo $arquivo1,$arquivo2
	diff TCC/Dados/$diames/$arquivo1 TCC/Dados/$diames/$arquivo2
fi
done
