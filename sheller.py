import argparse

shells = ['bash', 'perl']

def printShells():
    print('Available shells:')
    for shell in shells:
        print(shell)

parser = argparse.ArgumentParser(description='A script to generate reverse shells on various languages.')
parser.add_argument('shell', metavar='shellLanguage', type=str,
                    help='Language to identify the shell to be built. Use -s to see available shells.')

parser.add_argument('-i', dest='localAddr', help='Address to connect back to')
parser.add_argument('-p', dest='localPort', help='Port to connect back to')
parser.add_argument('-o', dest='outfile', help='File to write the reverse shell to')
parser.add_argument('-s', dest='shells', help='Print list of avalable shells languages.', const=printShells, default=printShells)

args = parser.parse_args()

if args.shell not in shells:
    print('ERROR: Unregognized shell type\n')
    printShells()
    parser.print_help()
    exit()

shellFile = open(args.shell+'.txt', 'r')
shellContents = shellFile.read()
shellContents = shellContents.replace('[LIP]', args.localAddr).replace('[LP]', args.localPort)

print (shellContents)
