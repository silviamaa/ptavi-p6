#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys

ip = sys.argv[1]
puerto = sys.argv[2]


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        #self.wfile.write("Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            line1 = line.split()
            if (line1[0] == "INVITE"):
            	print "El cliente nos manda su login " + line1[1]
            	self.wfile.write("100 TRYING\r\n\r\n" + "180 RING\r\n\r\n" +
            	"SIP/2.0 200 OK\r\n\r\n")

            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer((ip, int(puerto)), EchoHandler)
    print "Lanzando servidor UDP..."
    serv.serve_forever()
