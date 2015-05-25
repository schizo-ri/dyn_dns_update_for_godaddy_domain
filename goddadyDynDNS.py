from pygodaddy import GoDaddyClient
import pif
import logging

logging.basicConfig(filename='/path/to/file.log', \
    format='%(asctime)s %(message)s', level=logging.INFO)
    
GODADDY_USERNAME="username"
GODADDY_PASSWORD="pasword"
client = GoDaddyClient()

domain = 'domain'
public_ip = pif.get_public_ip()

# this file contains current ip address of your server
ip_file_value = open('/path/to/ip_file', 'r').read()

if ip_file_value == public_ip:
    exit(0)
else:
    if client.login(GODADDY_USERNAME, GODADDY_PASSWORD):
        hostnames = []
        
        # update IP for every A record
        for i in range(len(client.find_dns_records(domain))):        
            hostnames.append(client.find_dns_records(domain)[i].hostname)
            client.update_dns_record(hostnames[i]+"."+domain, public_ip)
        
        logging.info("Success! IP = '{0}'".format(public_ip))
        
        # write a new IP to file
        ip_file = open('/path/to/ip_file', 'w')
        ip_file.write(public_ip)
        ip_file.close()

    else:
        logging.info("Login failed".format())
