#!/usr/bin/expect

set timeout 3600

spawn /bin/sh -c "rsync -LCravzp /var/www/tcd.config tcd_offline@server2.megamidia.com.br:/home/redes/<rede>/ /var/www/"
expect {
    timeout {
        exit 1
    }
    -re "lost" {
        exit 1
    }
    -re "No route to host" {
        exit 1
    }
    -re "continue connecting" {
    	send "yes\r"
        exp_continue
        exit 0
    }
    -re "tcd_offline@server2.megamidia.com.br's password:" {
        send "Tre453m3g4\r"
        exp_continue
        exit 0
    }
}