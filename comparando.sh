
arquivos=`ls TCC/Dados/20170701/`
teste=0
teste2=0
vetor=()
for i in $arquivos;
do
	for x in $arquivos;
	do
		var=`expr $teste + 1`
		if [ "$teste2" == "$var" ];then
			echo $i,$x
			diff TCC/Dados/20170701/$i TCC/Dados/20170701/$x
		fi
		teste2=`expr $teste2 + 1`
	done
	teste2=0
	teste=`expr $teste + 1`
done
