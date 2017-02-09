#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from overtherepy import OverthereHostSession
import re


def to_map(stdout):
    _data = {}
    for s in response.stdout:
        if 'export' in s:
            info = s.replace('export ', ' ').replace('"', ' ').strip().split('=')
            _data[str(info[0])] = str(info[1]).strip()
    return _data


def machine_name(ci):
    if ci.machineName is not None:
        return ci.machineName
    else:
        return ci.name

def read_pem_file_to_string(path,pemfilename):
    pem_full_path="{0}/{1}".format(path,pemfilename)
    print "read {0}.....".format(pem_full_path)
    pem_file = open(pem_full_path,'r')
    content = pem_file.read()
    pem_file.close()
    return content


target_host = target.container.host
session = OverthereHostSession(target_host)
command_line = "docker-machine env %s " % machine_name(target)
print "Executing '%s'...." % command_line
response = session.execute(command_line)
data = to_map(response.stdout)
ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', data['DOCKER_HOST'])
if len(ip) == 1:
    data['address'] = ip[0]
print "IP Address is %s " % data['address']
print "--------------------"
print data
print "--------------------"

session.close_conn()

deployed.docker_host_address = data['address']
deployed.docker_host = data['DOCKER_HOST']
deployed.docker_cert_path = data['DOCKER_CERT_PATH']
if data['DOCKER_TLS_VERIFY'] == '1':
    deployed.docker_tls_verify = True
else:
    deployed.docker_tls_verify = False

if deployed.machineName is None:
    deployed.machineName = deployed.name
deployed.docker_certPem = read_pem_file_to_string(deployed.docker_cert_path,'cert.pem')
deployed.docker_keyPem = read_pem_file_to_string(deployed.docker_cert_path,'key.pem')
deployed.docker_caPem = read_pem_file_to_string(deployed.docker_cert_path,'ca.pem')


print "done"