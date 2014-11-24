#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor y envía mensajes SIP
"""

import socket
import sys


# Protocolo y versión
PROTOCOL = "sip"
VERSION = "SIP/2.0"

# Parámetros del usuario.
try:
    method = sys.argv[1].upper()
    parameters = sys.argv[2]

    ADDRESS = parameters.split(':')[0]
    IP = ADDRESS.split('@')[1]
    PORT = int(parameters.split(':')[1])
except:
    print ("Usage: python client.py method receiver@IP:SIPport")
    raise SystemExit

# Contenido que vamos a enviar
request = method + " " + PROTOCOL + ":" + ADDRESS + " " + VERSION + "\r\n\r\n"

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, PORT))

# Enviamos solicitud y recibimos respuesta
my_socket.send(request)
print "Enviado:\n" + request
try:
    data = my_socket.recv(1024)
except socket.error:
    print ("Error: No server listening at " + IP + " port " + str(PORT))
    raise SystemExit

print 'Recibido:\n' + data

# Si recibimos confirmación de INVITE envíamos ACK
response1 = "SIP/1.0 100 Trying\r\n\r\n" + "SIP/1.0 180 Ringing\r\n\r\n"\
          + "SIP/1.0 200 OK\r\n\r\n"
response2 = "SIP/2.0 100 Trying\r\n\r\n" + "SIP/2.0 180 Ringing\r\n\r\n"\
          + "SIP/2.0 200 OK\r\n\r\n"
if data == response1 or data == response2:
    method = 'ACK'
    request = method + " " + PROTOCOL + ":" + ADDRESS + " " + VERSION\
              + "\r\n\r\n"
    my_socket.send(request)
    print "Enviado:\n" + request

print "Finalizando socket..."

# Cerramos todo
my_socket.close()
print "Socket finalizado."
