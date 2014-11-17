#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

# Dirección IP del servidor.
METODO = sys.argv[1]

#Partimos los argumentos
z = sys.argv[2].split(":")
login = z[-2]
a = sys.argv[2].split("@")
b = a[1].split(":")
IPreceptor = b[-2]
puertoSIP = b[-1]


# Contenido que vamos a enviar si es un INVITE
LINE =  METODO + " " + login

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IPreceptor, int(puertoSIP)))

if (METODO == "INVITE"):
	print "Enviando: " + LINE
	my_socket.send(LINE + '\r\n')
	data = my_socket.recv(1024)

	print 'Recibido -- \r\n\r\n', data


# Cerramos todo
my_socket.close()
print "Fin."

