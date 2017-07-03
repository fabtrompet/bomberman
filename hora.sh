num=1
sem=3
for x in `ls Dados/`;
do
if [ $sem == 7 ];
then
   sem=0
fi
for i in `ls Dados/$x | sed "s/.csv//g"`;
do
	if [ $x != 20170423 ] && [ $x != 20170424 ];
	then
	sed -n $num'p;' dadosgrande.csv | sed 's/$/;'$x' '$i'/g' | sed 's/$/;'$sem'/g' | sed "s/'//g" >> dadoscomdata2.csv
	num=`expr $num + 1`
	fi
done
sem=`expr $sem + 1`
done
