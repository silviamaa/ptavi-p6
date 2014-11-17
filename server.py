#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys
import os


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        """
        Método para recibir en el manejador y establecer comunicación SIP
        """
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()

            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break
            else:
                print "El cliente nos manda " + line
                parameters = line.split()
                method = parameters[0]
                user = parameters[1].split(':')[1]
                version = parameters[2]
                
                if method == 'INVITE':
                    print method
                elif method == 'BYE':
                    print method

if __name__ == "__main__":
    try:
        IP = sys.argv[1]
        PORT = int(sys.argv[2])
        AUDIO_FILE = sys.argv[3]
        if not os.path.isfile(AUDIO_FILE):
            raise IndexError
    except IndexError:
        print ("Usage: python server.py IP port audio_file")
        raise SystemExit

    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PORT), EchoHandler)
    print "Listening..."
    serv.serve_forever()
