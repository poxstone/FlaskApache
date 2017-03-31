# -*- coding: utf-8 -*-
import subprocess
import re
import logging

def executeCommand(commmand_array):
    command = commmand_array.split()
    output = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    out, err = output.communicate()

    if out:
        logging.info(out)

    if err:
        logging.error(commmand_array + " >>>>>> " + err)

    return {"out": out, "error": err}


def addNat(addnat_sip, routing_port, client_host, client_port):
    command = "iptables -t nat -A PREROUTING -d {addnat_sip} -p tcp --dport {routing_port} -j DNAT --to-destination \
          {client_host}:{client_port}".format(addnat_sip=addnat_sip, routing_port=routing_port,
                                              client_host=client_host, client_port=client_port)
    return executeCommand(command)


def dropNat(addnat_sip, routing_port, client_host, client_port):
    command = "iptables -t nat -D PREROUTING -d {addnat_sip} -p tcp --dport {routing_port} -j DNAT --to-destination \
              {client_host}:{client_port}".format(addnat_sip=addnat_sip, routing_port=routing_port,
                                                  client_host=client_host, client_port=client_port)
    return executeCommand(command)


def checkPort(routing_port):
    command = "iptables -t nat -nL PREROUTING"
    table = executeCommand(command)
    """
        #RETURN Example:
        Chain PREROUTING (policy ACCEPT)
        target     prot opt source               destination
        DNAT       tcp  --  0.0.0.0/0            192.168.122.107      tcp dpt:50100 to:190.248.152.50:636
        DNAT       tcp  --  0.0.0.0/0            192.168.122.107      tcp dpt:50101 to:190.146.239.210:389
    """
    table = table["out"].split('\n')
    ports_found = []

    for index_row, row in enumerate(table):
        if index_row >= 2 and row:
            destination = row.split()[4]
            port = row.split()[6]

            if port == "dpt:" + routing_port:
                port = port.split(':')[1]
                ports_found.append({"port": port, "host": destination})

    return ports_found


def cleanPort(addnat_sip, routing_port, client_host, client_port):
    host_ports = checkPort(routing_port)

    for host_port in host_ports:
        dropNat(host_port["host"], host_port["port"], client_host, client_port)

    return host_ports

def getIp():
    network_interface = executeCommand("ifconfig eth0")["out"]

    if not network_interface:
        network_interface = executeCommand("ifconfig wlp4s0")["out"]

    if not network_interface:
        network_interface = executeCommand("ifconfig enp5s0f1")["out"]

    if network_interface:
        network_interface = re.search("addr:[0-9.]+", network_interface)

        if network_interface:
            network_interface = network_interface.group(0).split(":")[1]

            return network_interface

    return "0.0.0.0"


def udpadeNAT(nats):
    addnat_sip = getIp()

    for nat in nats:
        routing_port = nat['routingPort']
        client_host = nat['clientHost']
        client_port = nat['clientPort']

        clean_port = cleanPort(addnat_sip, routing_port, client_host, client_port)
        addNat(addnat_sip, routing_port, client_host, client_port)

    return nats




