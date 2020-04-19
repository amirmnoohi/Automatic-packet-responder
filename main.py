from extra import *
import sys
import random
import argparse
import datetime


def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    return s.getsockname()[0]


def checksum(msg):
    s = 0
    # loop taking 2 characters at a time
    for counter in range(0, len(msg), 2):
        w = (msg[counter] << 8) + (msg[counter + 1])
        s = s + w

    s = (s >> 16) + (s & 0xffff)
    # s = s + (s >> 16);
    # complement and mask to 4 byte short
    s = ~s & 0xffff
    return s


def dedicate_local_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 0))
    return s.getsockname()[1]


class ARPPACKET:
    def __init__(self, dest_mac, src_mac, sha, spa, tha, tpa):
        # ------------------Ethernet Header----------------
        self.dest_mac = dest_mac
        self.src_mac = src_mac
        self.type = 0x0806
        # ------------------ARP Header----------------
        self.htype = 0x001
        self.ptype = 0x0800
        self.hlen = 0x0006
        self.plen = 0x0004
        self.oper = 0x0002
        self.sha = sha
        self.spa = spa
        self.tha = tha
        self.tpa = tpa
        self.packet = pack('!6s6sHHHBBH6s4s6s4s',
                           self.dest_mac, self.src_mac, self.type, self.htype, self.ptype, self.hlen, self.plen,
                           self.oper, self.sha, self.spa, self.tha, self.tpa
                           )
        self.ALL = [self.dest_mac,
                    self.src_mac, self.type, self.htype, self.ptype, self.hlen, self.plen, self.oper,
                    self.sha, socket.inet_ntoa(self.spa), self.tha, socket.inet_ntoa(self.tpa)]


class ICMPPACKET:
    def __init__(self, type, code, packet_id):
        self.type = type
        self.code = code
        self.checksum = 0
        self.packet_id = packet_id
        self.sequence = 1
        self.data = 'IM AMIR MASOUD NOOHI'
        self.packet = pack('!BBHHH', self.type, self.code, self.checksum, self.packet_id,
                           self.sequence)
        self.checksum = checksum(self.packet + bytes(self.data, 'utf8'))
        self.packet = pack('!BBHHH', self.type, self.code, self.checksum, self.packet_id,
                           self.sequence) + bytes(self.data, 'utf8')
        self.ALL = [self.type, self.code, self.checksum, self.packet_id, self.sequence,
                    self.data]


def arp_reply(mac):
    try:
        conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        conn.bind((mac, socket.SOCK_RAW))
        while True:
            raw_data, addr = conn.recvfrom(65535)
            ether_header = ether(raw_data)
            if ether_header[2] == hex(2054):
                if arp(ether_header[-1])[4] == 1:
                    print("---------------------------------")
                    print("REQUEST : Who has " + socket.inet_ntoa(
                        arp(ether_header[-1])[8]) + " ? Tell " + socket.inet_ntoa(arp(ether_header[-1])[6]))
                    print("Response sent : " + socket.inet_ntoa(arp(ether_header[-1])[8]) + \
                          " is at " + get_mac_addr(conn.getsockname()[4]))
                    packet = ARPPACKET(arp(ether_header[-1])[5], conn.getsockname()[4], conn.getsockname()[4],
                                       socket.inet_aton(local_ip()),
                                       arp(ether_header[-1])[5], arp(ether_header[-1])[6])
                    conn.send(packet.packet)
    except KeyboardInterrupt:
        print("\nCtrl+C Pressed")


def icmp_reply(type, code):
    try:
        conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
        while True:
            raw_data, addr = conn.recvfrom(65535)
            ip_header = ip(raw_data[14:])
            if ip_header[8] == 1:
                if ip_header[11] == local_ip():
                    print("-------------------")
                    print("New ICMP request received From IP : " + str(ip_header[-3]))
                    print("We sent ICMP Reply with type: {},code : {}".format(type, code))
                    packet_id = int((id(1) * random.random()) / 65535)
                    packet = ICMPPACKET(type, code, packet_id)
                    s.sendto(packet.packet, (ip_header[10], 1))
    except KeyboardInterrupt:
        print("\nCtrl+C Pressed")


def dns_reply():
    try:
        conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
        while True:
            raw_data, addr = conn.recvfrom(65535)
            ip_header = ip(raw_data[14:])
            if ip_header[8] == 17:
                if ip_header[11] == local_ip():
                    # print(ip_header[:-1])
                    # print(udp(ip_header[-1]))
                    if udp(ip_header[-1])[1] == 53:
                        print("---------------------------")
                        print("Request from IP : " + ip_header[10])
                        print("Response sent")
                        packet = pack('!HHHHHH', 1104, 33029, 1, 0, 0, 0)
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.bind(('', dedicate_local_port()))
                        sock.settimeout(2)
                        sock.sendto(bytes(packet), (ip_header[10], udp(ip_header[-1])[1]))
    except KeyboardInterrupt:
        print("\nCtrl+C Pressed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', help='Response Type : arp - icmp - dns', required=True)
    parser.add_argument('-i', '--interface', help='Name of interface : eth0 - ens33 - wlan0')
    parser.add_argument('-d', '--data', help='Data That will be sent to Destination')

    args = parser.parse_args()
    if args.type.upper() == 'ARP':
        if args.interface is None:
            print("usage: main.py [-h] -t TYPE -i INTERFACE\n" + \
                  "main.py: error: the following arguments are required: -i/--interface")
            sys.exit()
        else:
            print("Starting ARP reply at " + str(datetime.datetime.now()))
            args = parser.parse_args()
            arp_reply(args.interface)
    elif args.type.upper() == 'ICMP':
        if args.data is None:
            print("usage: main.py [-h] -t TYPE -i INTERFACE -d DATA\n" + \
                  "main.py: error: the following arguments are required: -d/--DATA")
            sys.exit()
        else:
            print("Starting ICMP reply at " + str(datetime.datetime.now()))
            icmp_type = int(args.data[:args.data.find(',')])
            icmp_code = int(args.data[args.data.find(',') + 1:])
            icmp_reply(icmp_type, icmp_code)
    elif args.type.upper() == 'DNS':
        print("Starting DNS reply at " + str(datetime.datetime.now()))
        dns_reply()


if __name__ == "__main__":
    main()
