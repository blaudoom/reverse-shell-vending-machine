
"""
    if args.shell:
        open_shellfile()
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

    open_shellfile()

    if args.outfile:
        outfile = open(options['outfile'], 'w+')
        outfile.write(payload)
    else:
        print(payload)
    if args.httpServer:
        listener(args.httpPort)
"""