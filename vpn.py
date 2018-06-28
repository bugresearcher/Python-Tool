import os
import ssl
import socket
import base64
import hashlib
import requests
import http.client


def get_proxy():

    # custom
    email = '09D3AE09-837D-42B2-BB80-1552248CBFF7@se0304.surfeasy.vpn'
    # must be sha1
    password = '427D88E5AA4DCF2F6BEFE53B7575A704798D095B'
    device_hash = '4BE7D6F1BD040DE45A371FD831167BC108554111'

    apikey = '3690AC1CE5B39E6DC67D9C2B46D3C79923C43F05527D4FFADCC860740E9E2B25'
    SEheaders = {'SE-Client-Type': 'se0304', 'SE-Client-API-Key': apikey}

    s = requests.session()

    if os.path.exists('secret'):
        device_id, device_password = open('secret').read().split()
    else:  # register
        j = s.post('https://api.surfeasy.com/v2/register_subscriber',
                   data=dict(email=email, password=password),
                   headers=SEheaders).json()
        assert '0' in j['return_code'], j

        j = s.post('https://api.surfeasy.com/v2/register_device',
                   data=dict(client_type='se0304', device_hash=device_hash,
                             device_name='Opera-Browser-Client'),
                   headers=SEheaders).json()
        assert '0' in j['return_code'], j

        d = j['data']
        device_id = hashlib.sha1(d['device_id'].encode('ascii')).hexdigest()
        device_password = d['device_password']
        with open('secret', 'w') as f:
            f.write(device_id + ' ' + device_password)

    auth = device_id + ":" + device_password
    basic_auth = base64.b64encode(auth.encode('ascii')).decode('ascii')

    # j = s.post('https://api.surfeasy.com/v2/subscriber_login',
    #            data={'login': email, 'password': password,
    #                  'client_type': 'se0304'},
    #            headers=SEheaders).json()
    # assert '0' in j['return_code'], j

    # j = s.post('https://api.surfeasy.com/v2/geo_list',
    #            data={'device_id': device_id}).json()
    # assert '0' in j['return_code'], j
    # geo = j['data']
    # print(geo)

    j = s.post('https://api.surfeasy.com/v2/discover',
               data={'serial_no': device_id, 'requested_geo': '"US"'}).json()
    assert j['return_code']['0'] == 'OK', j
    ips = j['data']['ips']
    # print(ips)
    proxy = ips[0]['ip']
    port = ips[0]['ports'][0]
    print('Proxy:', proxy, port)

    return basic_auth, proxy, port


class PatchedContext:

    def __init__(self, conn):
        conn._check_hostname = False
        conn._context.check_hostname = False
        self.ctx = conn._context

    def __getattr__(self, attr):
        if attr == 'wrap_socket':
            return lambda sock, server_hostname: self.ctx.wrap_socket(sock)
        return getattr(self.ctx, attr)

if __name__ == '__main__':
    basic_auth, proxy, port = get_proxy()
    req = 'GET {url} HTTP/1.0\nProxy-Authorization: BASIC {basic_auth}\n\n'.format(
        url='http://httpbin.org/ip', basic_auth=basic_auth)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = ssl.wrap_socket(sock)
    sock.connect((proxy, port))
    sock.send(req.encode('ascii'))
    print(sock.recv(1024))
    sock.close()

    # or with ugly monkey patch
    conn = http.client.HTTPSConnection(proxy, port)
    conn._context = PatchedContext(conn)
    conn.request("GET", "http://httpbin.org/ip",
                 headers={"Proxy-Authorization": "BASIC "+basic_auth})
    print(conn.getresponse().read())