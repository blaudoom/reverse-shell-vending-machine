import argparse
import shells

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

