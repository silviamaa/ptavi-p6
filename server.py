#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor SIP
"""
import sys
import SocketServer
import os


try:
    UA = sys.argv[0] = 'server.py'
    IP = sys.argv[1]
    PUERTO = int(sys.argv[2])
    FICHERO = sys.argv[3]
except IndexError:
    sys.exit("Usage: python server.py IP port audio_file")


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break
            Metod = line.split(' ')[0]
            print "El cliente nos manda " + line
            if not Metod in Metodos:
                self.wfile.write('SIP/2.0 405 Method Not Allowed' + '\r\n\r\n')
            elif Metod == 'INVITE':
                rcv_invite = 'SIP/2.0 100 Trying' + '\r\n\r\n'
                rcv_invite += 'SIP/2.0 180 Ringing' + '\r\n\r\n'
                rcv_invite += 'SIP/2.0 200 OK' + '\r\n\r\n'
                self.wfile.write(rcv_invite)
            elif Metod == 'ACK':
                aAejecutar = './mp32rtp -i 127.0.0.1 -p 23032 < ' + FICHERO
                print 'Vamos a ejecutar', aAejecutar
                os.system(aAejecutar)
                print 'Ejecutado', '\r\n\r\n'
            elif Metod == 'BYE':
                self.wfile.write('SIP/2.0 200 OK' + '\r\n\r\n')
                print 'Terminando conversación...'
            else:
                self.wfile.write('SIP/2.0 400 Bad Request' + '\r\n\r\n')

if __name__ == "__main__":
    """
    Lanzando servidor SIP
    """
    Metodos = ['INVITE', 'ACK', 'BYE']
    serv = SocketServer.UDPServer(("", PUERTO), EchoHandler)
    print "Listening..."
    serv.serve_forever()
