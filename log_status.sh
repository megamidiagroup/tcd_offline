#!/bin/bash
servidor=`cat /etc/servermm.conf | grep servidor | cut -d "=" -f2`
loja=`cat /etc/servermm.conf | grep loja | cut -d "=" -f2`
datacenter=`cat /etc/servermm.conf | grep datacenter | cut -d "=" -f2`
rede=`cat /etc/servermm.conf | grep rede | cut -d "=" -f2`
locate="/var/log/tcd"

# Cria o arquivo de log de status da CPU
echo Equipe de Tecnologia - MegaMidia Group > ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log

echo "====[ Setup da Maquina ]====" >> ${locate}/${rede}_${loja}_status.log
echo "Servidor	== ${servidor} " >> ${locate}/${rede}_${loja}_status.log
echo "Rede		== ${rede} "  >> ${locate}/${rede}_${loja}_status.log
echo "Loja		== ${loja} "  >> ${locate}/${rede}_${loja}_status.log
echo "Datacenter	== ${datacenter} "  >> ${locate}/${rede}_${loja}_status.log
echo "Diretorio Logs	== ${locate} "  >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log

echo "====[  espaco em Disco ]====" >> ${locate}/${rede}_${loja}_status.log
df -H | grep sda >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log

echo "====[  Rede ]====" >> ${locate}/${rede}_${loja}_status.log
ifconfig >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log

echo "====[  IP Externo ]====" >> ${locate}/${rede}_${loja}_status.log
externo=`curl ifconfig.me`
echo "IP_Externo	= ${externo} " >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log

echo "====[  Data ]====" >> ${locate}/${rede}_${loja}_status.log
date >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log

echo "====[  Memoria ]====" >> ${locate}/${rede}_${loja}_status.log
free -m >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log

echo "====[  Videos Ausentes ]====" >> ${locate}/${rede}_${loja}_status.log
(cd /var/www; ls -R1 media > producao2.txt)
diff /var/www/producao.txt /var/www/producao2.txt >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log

echo "====[  Crontab ]====" >> ${locate}/${rede}_${loja}_status.log
cat /etc/crontab >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log

echo "====[  Tempo de Vida ]====" >> ${locate}/${rede}_${loja}_status.log
uptime >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log

echo "====[  Diretorio Scripts ]====" >> ${locate}/${rede}_${loja}_status.log
ls -la /usr/local/scripts >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log
ls -la /usr/local/bin/ >> ${locate}/${rede}_${loja}_status.log 
echo "" >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log

echo "====[  Espaco /home ]====" >> ${locate}/${rede}_${loja}_status.log
(cd /home/${rede}; du -sh >> ${locate}/${rede}_${loja}_status.log )
echo "" >> ${locate}/${rede}_${loja}_status.log
echo "" >> ${locate}/${rede}_${loja}_status.log


# Compacta o arquivo de log recem criado
zip -qj ${locate}/${rede}_${loja}_status ${locate}/${rede}_${loja}_status.log
#
## Envia o arquivo de log para o server
verifica=`cat /etc/servermm.conf | grep datacenter | cut -d "=" -f2`
echo $verifica
if [ "$verifica" == "10.0.1.226" ]
    then
#        # Apaga as informacoes de chaves de criptografia (known_hosts) do ssh
        rm -rf /root/.ssh
       rsync -aq --timeout=180 --password-file=/etc/tcd.update ${locate}/*.zip rsync://${rede}@${datacenter}:/${rede}_logs
else
      # Envia o arquivo recem criado para o server
       rsync -aq --timeout=180 --password-file=/etc/tcd.update ${locate}/*.zip rsync://${rede}@${datacenter}:/${rede}_logs
fi
# Exclui os arquivos que estao no diretorio de log
rm -f ${locate}/*.zip
