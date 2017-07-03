teste=`find TCC/Dados`
for i in $teste;
do
	cat $i | grep "\[";
done
