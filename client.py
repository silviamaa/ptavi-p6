#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor y envía mensajes SIP
"""

import socket
import sys

# Cliente SIP.

# Dirección IP del servidor.
SERVER = 'localhost'

# Parámetros del usuario.

if len(sys.argv) != 3:
    sys.exit("Usage: python client.py method receiver@IP:SIPport")
else:
    METHOD = sys.argv[1].upper()
    parameters = sys.argv[2]

USER = parameters.split(':')[0]
IP = USER.split('@')[1]
PORT = int(parameters.split(':')[1])

# Contenido que vamos a enviar
REQUEST = METHOD + " " + "sip:" + USER + " SIP/2.0\r\n"

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print "Enviando:\n" + REQUEST
my_socket.send(REQUEST)
try:
    data = my_socket.recv(1024)
except socket.error:
    print ("Error: No server listening at " + IP + " port " + str(PORT))
    raise SystemExit

print 'Recibido:\n' + data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
