# CoinBoy

:warning: This is a proof-of-concept so the scripts aren't secured very tightly! Don't use this in production! Also we use the Bitcoin testnet! :warning:

## Installation:

* Install Bitcoin Server (bitcoind) (see useful resources for helpful links)
* Install Ligthning Server (lnd)
* Have a running matrix creator or some other ROS Topic which you can trigger with a lightning payment as an example we used the MatrixCreator LEDS.
* Install the Eclair Testnet wallet on a Smartphone
* Fund and open a Lightning channel between your Smartphone and your Node or if your node is connected to others to the network in general

## Start:

* Start the MatrixCreator
```bash
ssh into raspberry pi with the matrix creator
roslaunch led_control leds.launch
```
* Start the Bitcoin Node
```bash
bitcoind -testnet -txindex -server -zmqpubrawblock=tcp://127.0.0.1:28332 -zmqpubrawtx=tcp://127.0.0.1:28333 -rpcuser=roboy -rpcpassword=roboynorth
```

* Start the Lightning Node
```bash
lnd --bitcoin.active --bitcoin.testnet --debuglevel=debug --bitcoin.node=bitcoind --bitcoind.rpcuser=roboy --bitcoind.rpcpass=roboynorth --bitcoind.zmqpubrawblock=tcp://127.0.0.1:28332 --bitcoind.zmqpubrawtx=tcp://127.0.0.1:28333 --nat --rpclisten=localhost:10009 --no-macaroons
lncli -network testnet unlock
```

* Start the Webserver
```bash
cd source-of-the-webserver
python3 manage.py runserver 0.0.0.0:8000
```

* Start the "invoice watcher" script
```bash
cd source-of-the-webserver
python3 check_payment.py
```

## Sources:

bitcoind
https://github.com/bitcoin/bitcoin

lnd
https://github.com/lightningnetwork/lnd

Webserver
https://github.com/dprog-philippe-docourt/django-qr-code

## useful resources/tipps:
Bitcoin Node Full setup guide
https://bitcoin.org/en/full-node

Lightning first steps and setup guide
https://dev.lightning.community/tutorial/

Lightning API
https://api.lightning.community/

Lightning API and how to access it from python
https://github.com/lightningnetwork/lnd/blob/master/docs/grpc/python.md

Added a special bashrc file on the matrix creator as the standard bashrc isn't loaded in interactive sessions this ludwigbashrc just contains the stuff needed for ROS to work.
