cat mapaestacao.aspx | grep beaches | sed "s/var beaches = \[//g" | sed "s/,];//g" | sed "s/]]>//g" | sed "s/setMarkers(map, beaches);//g" | tr "]" "\n" | awk -F "[" '{print $2}'
