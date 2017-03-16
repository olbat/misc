# Create a CA using OpenSSL

## Generate the CA certificate
* Generate fake CA (self-signed) certificate for testing purpose
```bash
openssl req -new -x509 -newkey rsa:4096 -nodes -keyout ca.key -out ca.crt -subj '/C=FR/O=TestCA' -extensions v3_ca -batch
```
* (Check the certificate)
```bash
openssl x509 -in ca.crt -text -noout
```

## Generate and sign new ceritificates
* Generate domain's certificate signing request (CSR)
```bash
openssl req -new -newkey rsa:4096 -nodes -keyout domain.key -out domain.csr -subj '/C=FR/O=TestCorp/CN=domain.tld' -batch
```
* (Check the CSR)
```bash
openssl req -in domain.csr -text -noout
```
* Sign the CSR with the key of the CA's certificate
```bash
openssl x509 -req -CA ca.crt -CAkey ca.key -CAcreateserial -in domain.csr -out domain.crt
```
* (Check the certificate)
```bash
openssl x509 -in domain.crt -text -noout
```
* Sign the CSR of another domain ...
```bash
openssl x509 -req -CA ca.crt -CAkey ca.key -CAserial ca.srl -in another-domain.csr -out another-domain.crt
```

## Validation
* Verify the chain of trust
```bash
cat ca.crt domain.crt | openssl verify -CAfile ca.crt
```
* Test the certificate
```bash
openssl s_server -CAfile ca.crt -cert domain.crt -key domain.key -accept 12345
openssl s_client -connect 127.0.0.1:12345 -CAfile ca.crt < /dev/null
```
