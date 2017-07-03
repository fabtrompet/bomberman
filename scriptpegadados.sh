#!/bin/bash
for i in {2..1};
do
wget http://www.bicicletar.com.br/mapaestacao.aspx
diames=`date +%G%m%d`
hora=`date +%T`
cat mapaestacao.aspx | grep beaches | sed "s/var beaches = \[//g" | sed "s/,];//g" | sed "s/]]>//g" | sed "s/setMarkers(map, beaches);//g" | sed "s/]/]+/g" | tr "+" "\n" | sed 's/\/\///g' | tr -s "\n" | sed "s/\,\[//g" | sed "s/\[//g" | sed "s/\]//g" | sed "s/',/\';/g" | sed "s/,-/;-/g" | sed "s/,'/;'/g" > $hora.csv
sed -i 82d $hora.csv
sed -i 81d $hora.csv
if [ -d TCC/Dados/$diames ];
then
 mv $hora.csv TCC/Dados/$diames/;
else
 mkdir -p TCC/Dados/$diames;
 mv $hora.csv TCC/Dados/$diames/;
fi
rm mapaestacao.aspx
if [ $i == 2 ];
then
	sleep 30
fi
done
