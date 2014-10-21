import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("requests").setLevel(100)
logging.getLogger("urllib3.connectionpool").setLevel(100)

nxt_start_command = "cd ~/compile/nxt-1.3.1 && ./clean_db_and_start.sh"
nxt_stop_command = "killall -9 java"

coordinator_host = "127.0.0.1"
coordinator_port = 6666

name = "native"
