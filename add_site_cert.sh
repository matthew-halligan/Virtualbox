#!/bin/sh

HOSTNAME=$1
PORT=$2

TRUST_CERT_FILE_LOC=/etc/ssl/certs/ca-certificates.crt

sudo bash -c "echo -n | openssl s_client -showcerts -connect ${HOSTNAME}:${PORT} \
2>/dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' \
>> ${TRUST_CERT_FILE_LOC}"
