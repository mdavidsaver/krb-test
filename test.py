#!/usr/bin/env python3

from gssapi import Credentials, Name, NameType, SecurityContext

client_cred = Credentials.acquire(
    Name("user@LOCAL", NameType.kerberos_principal), usage="initiate"
)

server_cred = Credentials.acquire(
    Name("host/localhost@LOCAL", NameType.kerberos_principal), usage="accept"
)

client_ctx = SecurityContext(name=server_cred.creds.name, usage="initiate")

server_ctx = SecurityContext(creds=server_cred.creds, usage="accept")

from_server = None # client initiates handshake

while not (client_ctx.complete and server_ctx.complete):
    assert not client_ctx.complete
    from_client = client_ctx.step(from_server)
    if from_client is None:
        assert server_ctx.complete
        print('Client completes')
        break
    assert not server_ctx.complete
    from_server = server_ctx.step(from_client)
    assert from_server is not None
    if server_ctx.complete:
        print('Server completes')

assert client_ctx.complete and server_ctx.complete, (
    client_ctx.complete,
    server_ctx.complete,
)


print(f'Server: client {server_ctx.initiator_name} is valid for {server_ctx.lifetime} sec')
print(f'Client: server {client_ctx.target_name} is valid for {client_ctx.lifetime} sec')

msg = b'client provides CCR'
server_ctx.verify_signature(msg, client_ctx.get_signature(msg))

msg = b'server replies with CERT'
client_ctx.verify_signature(msg, server_ctx.get_signature(msg))

print("Success!")
