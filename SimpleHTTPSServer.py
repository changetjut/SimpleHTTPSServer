import http.server
import os
import ssl
from socket import gethostname
from OpenSSL import crypto
from functools import partial
import sys
import getopt

CERT_PATH = "server.crt"
KEY_PATH = "server.key"
PEM_PATH = "server.pem"

def create_self_signed_cert(cert_path,key_path,pem_path):
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 1024)

    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = "UK"
    cert.get_subject().ST = "London"
    cert.get_subject().L = "London"
    cert.get_subject().O = "Dummy Company Ltd"
    cert.get_subject().OU = "Dummy Company Ltd"
    cert.get_subject().CN = gethostname()
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha1')
    if not os.path.exists(cert_path):
        open(cert_path, "wb").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    if not os.path.exists(key_path):
        open(key_path, "wb").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
    if not os.path.exists(pem_path):
        open(pem_path, "wb").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
        open(pem_path, "ab").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

def create_https_server(useHTTPS, port, webroot):
    server_address = ('0.0.0.0', port)
    try:
        pHandler = partial(http.server.SimpleHTTPRequestHandler, directory=webroot)
        httpd = http.server.HTTPServer(server_address, pHandler)
        if useHTTPS:
            httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile='server.pem', ssl_version=ssl.PROTOCOL_TLS)
    except:
        exit("[ERR] Port %d has been taken." % port)
    print("Serving HTTP[s] on 0.0.0.0:port %d..." % port)
    httpd.serve_forever()

if __name__ == "__main__":
    # 默认参数
    useHTTPS = 0
    port = 80
    webroot = "/tmp"

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hsp:d:", ["help", "useHTTPS", "port=", "dir="])
    except getopt.GetoptError:
        print('Usage: SimpleHTTPSServer.py -s -p <port> -d <webrootdir>')
        print('  -s, --useHTTPS\t use HTTPS')
        print('  -p, --port\t set listening port')
        print('  -d, --dir\t set web directory')
        sys.exit(2)

    # 处理 返回值options是以元组为元素的列表。
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('Usage: SimpleHTTPSServer.py -s -p <port> -d <webrootdir>')
            print('  -s, --useHTTPS\t use HTTPS')
            print('  -p, --port\t set listening port')
            print('  -d, --dir\t set web directory')
            sys.exit()
        elif opt in "-s":
            useHTTPS = 1
            port = 443
        elif opt in ("-p", "--port"):
            if str.isnumeric(arg):
                port = int(arg)
            else:
                print("Port error. Can only be a number!")
        elif opt in ("-d", "--dir"):
            webroot = arg

    if port > 65535:
        print("Port error. Port can not be larger than 65535 !")

    if useHTTPS:
        create_self_signed_cert(CERT_PATH,KEY_PATH,PEM_PATH)
    create_https_server(useHTTPS, port, webroot)
