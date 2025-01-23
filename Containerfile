FROM docker.io/library/debian:12

RUN apt-get update \
 && apt-get -y install --no-install-recommends krb5-admin-server krb5-kdc supervisor \
 && rm -rf /var/lib/apt/lists /var/cache/apt

COPY krb5.conf supervisord.conf /etc/

COPY kadm5.acl kdc.conf badpass.txt /etc/krb5kdc/

# ick. hard coded password!!!
RUN kdb5_util create -s -P secret \
 && kadmin.local -q 'addprinc -pw secret -allow_svr root/admin' \
 && kadmin.local -q 'addprinc -pw secret -allow_svr user'

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisord.conf"]

EXPOSE 6464 6688 6749
