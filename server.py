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
        client_ip = str(self.client_address[0])
        client_port = str(self.client_address[1])
        print "IP cliente: " + client_ip + "| Puerto cliente: " + client_port

        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()

            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break
            else:
                # Evaluación de los parámetros que nos envía el cliente
                print "Recibido:\n" + line
                parameters = line.split()
                method = parameters[0]
                user = parameters[1].split(':')[1]
                version = parameters[2]

                # Evaluación del método que nos envía el cliente
                if method == 'INVITE':
                    response = version + " 100 Trying\r\n\r\n"
                    response += version + " 180 Ring\r\n\r\n"
                    response += version + " 200 OK\r\n\r\n"
                    self.wfile.write(response)
                elif method == 'BYE':
                    self.wfile.write(version + " 200 OK\r\n\r\n")
                elif method == 'ACK':
                    # --------------------- Envío RTP -------------------------
                    toRun = "./mp32rtp -i 127.0.0.1 -p 23032 < " + AUDIO_FILE
                    print "Enviando contenido RTP al cliente..."
                    os.system(toRun)
                    print "Finalizado envío RTP"
                else:
                    self.wfile.write(version +
                                     " 405 Method Not Allowed\r\n\r\n")


if __name__ == "__main__":

    # Evaluación de parámetros de la línea de comandos
    try:
        SERVER_IP = sys.argv[1]
        SERVER_PORT = int(sys.argv[2])
        AUDIO_FILE = sys.argv[3]
        if not os.path.isfile(AUDIO_FILE):
            sys.exit("Usage: python server.py IP port audio_file")
    except:
        print ("Usage: python server.py IP port audio_file")
        raise SystemExit

    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", SERVER_PORT), EchoHandler)
    print "Listening..."
    serv.serve_forever()
