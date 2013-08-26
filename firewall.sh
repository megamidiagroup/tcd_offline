#!/bin/bash
# Apaga todas as regras definidas anteriormente

MOD="/sbin/modprobe"
IPT6="/sbin/ip6tables"
IPT="/sbin/iptables"

stop(){
        # Limpar Regras
        $IPT -F -t filter
        $IPT -F -t nat
        $IPT -F -t mangle

        # Apagar cadeias definidas por usuarios
        $IPT -X -t filter
        $IPT -X -t nat
        $IPT -X -t mangle

        # Definir politica default para ACCEPT
        $IPT -P INPUT ACCEPT
        $IPT -P OUTPUT ACCEPT
        $IPT -P FORWARD ACCEPT

        $IPT6 -P INPUT ACCEPT
        $IPT6 -P OUTPUT ACCEPT
        $IPT6 -P FORWARD ACCEPT

        $IPT -t nat -P PREROUTING ACCEPT
        $IPT -t nat -P POSTROUTING ACCEPT
        $IPT -t nat -P OUTPUT ACCEPT

        $IPT -t mangle -P PREROUTING ACCEPT
        $IPT -t mangle -P POSTROUTING ACCEPT
        $IPT -t mangle -P INPUT ACCEPT
        $IPT -t mangle -P FORWARD ACCEPT
        $IPT -t mangle -P OUTPUT ACCEPT
}

start(){
        stop
        $MOD nf_nat_ftp
        $MOD ip6_tables

iptables -F
#Bloqueia todo o trafego antes de finalizar a configuração
iptables -A INPUT -j DROP
iptables -A OUTPUT -j DROP
iptables -A FORWARD -j DROP

# Seta as politicas padrao
iptables -P INPUT DROP
iptables -P OUTPUT ACCEPT
iptables -P FORWARD DROP

# Regras especificas para interface lo (localhost)
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Regras bloqueio wifi
iptables -A INPUT -i wlan0 -j DROP
iptables -A OUTPUT -o wlan0 -j DROP

# Regras de input especificas para o protocolo ICMP [eth0]
iptables -A INPUT -p icmp -s 10.0.1.81/32 -i eth0 -j ACCEPT
iptables -A INPUT -p icmp -i eth0 -j DROP

# Tratamento FTP
iptables -A OUTPUT -p tcp --dport 21 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT  -p tcp --sport 21 -m state --state ESTABLISHED,RELATED -j ACCEPT

iptables -A INPUT -p tcp --sport 20 -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -p tcp --dport 20 -m state --state ESTABLISHED -j ACCEPT


iptables -A INPUT -p tcp --sport 1024: --dport 1024: -m state --state ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp --sport 1024: --dport 1024: -m state --state ESTABLISHED,RELATED -j ACCEPT


# Regras gerais de input [eth0]
# Recusa pacotes de localhost, broadcast e multicast
iptables -A INPUT -s 127.0.0.0/8 -i eth0 -j DROP
iptables -A INPUT -s 255.0.0.0/8 -i eth0 -j DROP
iptables -A INPUT -s 224.0.0.0/3 -i eth0 -j DROP

# Aceita pacotes para a porta 22 - SSH
iptables -A INPUT -p tcp --dport 22 -s 200.195.168.2/32 -i eth0 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -s 10.0.1.81/32 -i eth0 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -s 10.0.1.95/32 -i eth0 -j ACCEPT


# Acessa o RSYNC *.megamidia.com.br
iptables -A OUTPUT -p tcp --dport 873 -d 10.0.1.226/32 -o eth0 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 873 -d 200.195.168.2/32 -o eth0 -j ACCEPT


# Recusa pacotes para a porta 80 - http
iptables -A OUTPUT -p tcp --dport 80 -d 64.251.30.49 -o eth0 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 443 -d 64.251.30.49 -o eth0 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 80 -o eth0 -j DROP
iptables -A OUTPUT -p tcp --dport 443 -o eth0 -j DROP

# Aceita pacotes de conexoes ja estabelecidas e/ou relacionados indiretamente a uma conexao
iptables -A INPUT -m state --state ESTABLISHED,RELATED -i eth0 -j ACCEPT


# Remove as primeiras regras (regras de bloqueio)
iptables -D INPUT 1
iptables -D OUTPUT 1
iptables -D FORWARD 1
}

case "$1" in
  start)
        echo -n "INICIANDO FIREWALL... "
        start
        echo "ok"
  ;;

  stop)
        echo -n "PARANDO FIREWALL... "
        stop
        echo "ok"
  ;;

  status)
        echo "*************** KERNEL CONFS ***************"
        echo -n "IP FORWARD = "
        cat /proc/sys/net/ipv4/ip_forward
        echo -n "IP DYNADDR = "
        cat /proc/sys/net/ipv4/ip_dynaddr
        echo "ACCEPT REDIRECTS = "
        cat /proc/sys/net/ipv4/conf/*/accept_redirects
        echo "SEND REDIRECTS = "
        cat /proc/sys/net/ipv4/conf/*/accept_redirects
        echo "*************** TABELA FILTER ***************"
        $IPT -L
        echo "*************** TABELA NAT ***************"
        $IPT -t nat -L
        echo "*************** TABELA MANGLE ***************"
        $IPT -t mangle -L
  ;;
  status-no-name)
        echo "*************** KERNEL CONFS ***************"
        echo -n "IP FORWARD = "
        cat /proc/sys/net/ipv4/ip_forward
        echo -n "IP DYNADDR = "
        cat /proc/sys/net/ipv4/ip_dynaddr
        echo "ACCEPT REDIRECTS = "
        cat /proc/sys/net/ipv4/conf/*/accept_redirects
        echo "SEND REDIRECTS = "
        cat /proc/sys/net/ipv4/conf/*/accept_redirects
        echo "*************** TABELA FILTER ***************"
        $IPT -L -n
        echo "*************** TABELA NAT ***************"
        $IPT -t nat -L -n
        echo "*************** TABELA MANGLE ***************"
        $IPT -t mangle -L -n
  ;;

  restart)
        echo -n "REINICIALIZANDO FIREWALL... "
        stop
        start
        echo "OK"
  ;;

  *)
        echo $"USE: $0 {start|stop|restart|status|status-no-name}"
        exit 1
esac

exit 0
