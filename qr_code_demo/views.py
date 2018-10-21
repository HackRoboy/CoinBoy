from datetime import date
from django.shortcuts import render
import rpc_pb2 as ln
import rpc_pb2_grpc as lnrpc
import grpc
import os

def index(request):
    """
    Build the home page of this demo app.

    :param request:
    :return: HTTP response providing the home page of this demo app.
    """
    
    # Due to updated ECDSA generated tls.cert we need to let gprc know that
    # we need to use that cipher suite otherwise there will be a handhsake
    # error when we communicate with the lnd rpc server.
    os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'

    # Lnd cert is at ~/.lnd/tls.cert on Linux and
    # ~/Library/Application Support/Lnd/tls.cert on Mac
    cert = open(os.path.expanduser('~/.lnd/tls.cert'), 'rb').read()
    creds = grpc.ssl_channel_credentials(cert)
    channel = grpc.secure_channel('localhost:10009', creds)
    stub = lnrpc.LightningStub(channel)
    # Retrieve and display the wallet balance
    #response = stub.WalletBalance(ln.WalletBalanceRequest())
    m_request = ln.Invoice(
        value=100,
    )
    response = stub.AddInvoice(m_request)

    # Build context for rendering QR codes.
    context = dict(
        #invoice_id='lntb100u1pdukkecpp505wuvr8a9jujgh80a9nkl60kns0866y73f9ekr8rw5ff0xmmu4nqdqqcqzysxwtzpe8c9pufk5v7z7794247amqh43g43w43elfeea2lpdhj84jjm57desvjp443rvhcfl7x6y5vn0wu77wt2q6h2279dw7kcn6mu6gpuj4uw6',
	invoice_id= response.payment_request,
    )

    # Render the index page.
    return render(request, 'qr_code_demo/index.html', context=context)
