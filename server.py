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
        ip = str(self.client_address[0])
        port = str(self.client_address[1])
        print "IP del cliente: " + ip + "| Puerto del cliente: " + port
        
        methods = ('CANCEL', 'OPTIONS', 'REGISTER', 'PRACK', 'SUBSCRIBE',
                   'NOTIFY', 'PUBLISH', 'INFO', 'REFER', 'MESSAGE', 'UPDATE')

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

                not_allowed = 0
                for m in methods:
                    if method == m:
                        not_allowed = 1

                if method == 'INVITE':
                    # Enviamos respuesta en una línea para simplificar
                    response = version + " 100 Trying\r\n\r\n"
                    response += version + " 180 Ring\r\n\r\n"
                    response += version + " 200 OK\r\n\r\n"
                    self.wfile.write(response)
                elif method == 'BYE':
                    self.wfile.write(version + " 200 OK\r\n\r\n")
                elif method == 'ACK':
                    pass # --------------------------------------------------- Falta implementar
                elif not_allowed:
                    self.wfile.write(version +
                                     " 405 Method Not Allowed\r\n\r\n")
                else:
                    self.wfile.write(version + " 400 Bad Request\r\n\r\n")

if __name__ == "__main__":

    if len(sys.argv) != 4 or not os.path.isfile(sys.argv[3]):
        sys.exit("Usage: python server.py IP port audio_file")
    else:
        IP = sys.argv[1]
        PORT = int(sys.argv[2])
        AUDIO_FILE = sys.argv[3]

    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PORT), EchoHandler)
    print "Listening..."
    serv.serve_forever()
