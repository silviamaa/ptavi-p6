#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""
import sys
import socket


try:
    UA = sys.argv[0] = 'client.py'
    METOD = sys.argv[1]
    RECEPTOR = sys.argv[2].split('@')[0]
    IP_R = sys.argv[2].split('@')[1].split(':')[0]
    PUERTO_R = int(sys.argv[2].split('@')[1].split(':')[1])
except IndexError:
    sys.exit("Usage: python client.py method receiver@IP:SIPport")

# Contenido que vamos a enviar
LINE = METOD + ' sip:' + RECEPTOR + '@' + IP_R + ' SIP/2.0\r\n\r\n'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP_R, PUERTO_R))

print '\r\n\r\n' + "Enviando: " + LINE
my_socket.send(LINE)
try:
    data = my_socket.recv(1024)
except socket.error:
    sys.exit("Error:No server listening at " + IP_R + " port " + str(PUERTO_R))

print data
rcv_invite = data.split('\r\n\r\n')[0:-1]
if rcv_invite == ['SIP/2.0 100 Trying', 'SIP/2.0 180 Ringing',
                  'SIP/2.0 200 OK']:
    METOD = 'ACK'
    NEWLINE = METOD + ' sip:' + RECEPTOR + '@' + IP_R + ' SIP/2.0\r\n\r\n'
    print '\r\n\r\n' + "Enviando: " + NEWLINE
    my_socket.send(NEWLINE)
    data = my_socket.recv(1024)
    print data

# Cerramos todo
my_socket.close()
