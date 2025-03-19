## 2.1
#### python simpleWebServer.py

## 2.2
#### python client.py -i 127.0.0.1 -p 8000 -f index.html 

## 3
#### python tcpserver-multi.py
#### python client.py -i 127.0.0.1 -p 8000 -f index.html 

## 4
#### sudo python3 simpleWebServer.py
#### tcpdump -i r2-eth1 -tttt -w traces.pcap
#### sudo python3 client.py -i 10.0.1.2 -p 8000 -f index.html 