#!/usr/bin/expect

# Equipe Tecnologia 2.0 - Megamidia Group - 07/2012.
# Atualiza TCD - OFFLINE

set timeout 120

spawn /bin/sh -c "rsync -LCravzp radiob@server2.megamidia.com.br:/home/redes/centauro/ /var/www/"
expect {
    timeout {
        exit 1
    }
    -re "lost" {
        exit 1
    }
    -re "radiob@server2.megamidia.com.br's password:" {
        send "radiob\r"
        exp_continue
        exit 0
    }
}
