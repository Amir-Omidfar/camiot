raspivid -w 640 -h 480 --nopreview -t 0 -o - | nc 192.168.1.108 8200

