import rpc_pb2 as ln
import rpc_pb2 as ln, rpc_pb2_grpc as lnrpc
import grpc, os
import codecs
import time
from paramiko.client import SSHClient
os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'
cert = open(os.path.expanduser('~/.lnd/tls.cert'), 'rb').read()
ssl_creds = grpc.ssl_channel_credentials(cert)
channel = grpc.secure_channel('localhost:10009', ssl_creds)
stub = lnrpc.LightningStub(channel)
request = ln.InvoiceSubscription()
for response in stub.SubscribeInvoices(request):
    if response.settled:
        #do something
        print('starting ssh call')
        client = SSHClient()
        client.load_system_host_keys()
        client.connect('192.168.0.104', username='pi', password='raspberry')
        stdin, stdout, stderr = client.exec_command('source ~/.ludwigsbashrc && rostopic pub /roboy/control/matrix/leds/mode/simple std_msgs/Int32 \"data: 2\" --once')
        time.sleep(10)
        stdin, stdout, stderr = client.exec_command('source ~/.ludwigsbashrc && rostopic pub /roboy/control/matrix/leds/mode/simple std_msgs/Int32 \"data: 0\" --once')
