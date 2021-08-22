# Overview

These scripts can be used to target the client and server produced by
<https://github.com/tyranid/ExampleChatApplication>.

parser.py can be used independently by feeding it a file with a raw byte dump
from a packet capture using something such as Wireshark.

proxy.py can be used to feed live traffic to parser.py.

## parser.py

```console
$ python parser.py ~/Downloads/client.bin
conn: b'BINX'
 13 |  1339 | syn | b'test' | b'computer'
 14 |  1060 | msg | b'test' | b'test123'
 17 |  1168 | msg | b'test' | b'test 4 5 6'
 21 |  1677 | bye | b"I'm going away now!"
$ python parser.py ~/Downloads/server.bin
  2 |     1 | ack
 44 |  3788 | bye | b"Don't let the door hit you on the way out!"
$ python parser.py ~/Downloads/full.bin
conn: b'BINX'
 13 |  1339 | syn | b'test' | b'computer'
  2 |     1 | ack
 14 |  1060 | msg | b'test' | b'test123'
 17 |  1168 | msg | b'test' | b'test 4 5 6'
 21 |  1677 | bye | b"I'm going away now!"
 44 |  3788 | bye | b"Don't let the door hit you on the way out!"
$
```

## proxy.py

Start the server:

```console
$ dotnet exec ChatServer/bin/Release/netcoreapp5.0/ChatServer.dll --c ChatServer/server.pfx
ChatServer (c) 2017 James Forshaw
WARNING: Don't use this for a real chat system!!!
Running server on port 12345 Global Bind False
```

Start the proxy:

```console
$ python proxy.py
[proxy]  listening on  0.0.0.0:3333
[proxy]  forwarding to 127.0.0.1:12345
[proxy]  0: setting up
[proxy]  0: connection established
[proxy]  1: setting up
```

Start the client:

```console
$ dotnet exec ChatClient/bin/Release/netcoreapp5.0/ChatClient.dll test 127.0.0.1 --port 3333
ChatClient (c) 2017 James Forshaw
WARNING: Don't use this for a real chat system!!!
Connecting to 127.0.0.1:3333
> hello world
> the quick brown fox jumps over the lazy dog
> /quit
> Server: Don't let the door hit you on the way out!
$
```

Sample client and proxy output:

```console
$ python proxy.py
[proxy]  listening on  0.0.0.0:3333
[proxy]  forwarding to 127.0.0.1:12345
[proxy]  0: setting up
[proxy]  0: connection established
[proxy]  1: setting up
[client] pkt: conn: b'BINX'
[client] pkt:  13 |  1339 | syn | b'test' | b'computer'
[server] pkt:   2 |     1 | ack
[client] pkt:  18 |  1582 | msg | b'test' | b'hello world'
[client] pkt:  50 |  4587 | msg | b'test' | b'the quick brown fox jumps over the lazy dog'
[client] pkt:  21 |  1677 | bye | b"I'm going away now!"
[server] pkt:  44 |  3788 | bye | b"Don't let the door hit you on the way out!"
```
