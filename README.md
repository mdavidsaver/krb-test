# Testing kerberos instance

**Warning:** This is an example/testing environment only!

Default `secret` passwords are bad bad practice.

## Build

```sh
git clone https://github.com/mdavidsaver/krb-test
cd krb-test

podman build -t krb-test .
```

## Run

```sh
podman run -ti --rm --net host krb-test
```

`Ctrl+c` to stop

## Authenticating with builtin user

```sh
$ cd krb-test
$ KRB5_CONFIG=$PWD/krb5.conf \
  KRB5CCNAME=$PWD/krb5cc \
  kinit user

$ klist ./krb5cc
Ticket cache: FILE:./krb5cc
Default principal: user@LOCAL

Valid starting       Expires              Service principal
01/22/2025 18:31:34  01/23/2025 18:31:34  krbtgt/LOCAL@LOCAL
```

## Create a service keytab

```sh
$ cd krb-test
$ KRB5_CONFIG=$PWD/krb5.conf \
  kadmin -p root/admin@LOCAL
kadmin: addprinc -nokey host/localhost
Principal "host/localhost@LOCAL" created.
kadmin:  ktadd -k localhost.keytab host/localhost
...
kadmin: exit

$ klist -k localhost.keytab
Keytab name: FILE:localhost.keytab
KVNO Principal
---- --------------------------------------------------------------------------
   1 host/localhost@LOCAL
   1 host/localhost@LOCAL
```

## Testing

```sh
sudo apt-get install python3-gssapi
```

```sh
$ cd krb-test
$ KRB5_CONFIG=$PWD/krb5.conf \
  KRB5CCNAME=$PWD/krb5cc \
  KRB5_KTNAME=$PWD/localhost.keytab \
   python test.py
Server completes
Client completes
Server: client user@LOCAL is valid for 82637 sec
Client: server host/localhost@LOCAL is valid for 82337 sec
Success!
```
