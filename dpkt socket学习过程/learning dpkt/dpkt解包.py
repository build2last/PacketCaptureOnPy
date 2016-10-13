# -*- coding:utf-8 -*-
import dpkt
import datetime
import socket
import pcap
import struct

def add_colons_to_mac( mac_addr ) :
    """Convert a MAC address to a readable/printable string

       Args:
           address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
       Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02x' % ord(b) for b in mac_addr)

# 利用 struct 处理字节流中的mac地址
def mac2str(bi_mac):
    mac = ""
    for i in bi_mac[:-1]:
        i_str = i + "\x00\x00\x00"
        tmac, = struct.unpack("i", i_str)
        mac += str(tmac) + ":"
    i_str = bi_mac[-1] + "\x00\x00\x00"
    tmac, = struct.unpack("i", i_str)
    mac += str(tmac)
    return mac
    
class AH(dpkt.Packet):
    """Authentication Header.

    TODO: Longer class information....

    Attributes:
        __hdr__: Header fields of AH.
        auth: Authentication body.
        data: Message data.
    """
    
    __hdr__ = (
        ('nxt', 'B', 0),
        ('len', 'B', 0),  # payload length
        ('rsvd', 'H', 0),
        ('spi', 'I', 0),
        ('seq', 'I', 0)
    )
    auth = ''

    def unpack(self, buf):
        dpkt.Packet.unpack(self, buf)
        self.auth = self.data[:self.len]
        buf = self.data[self.len:]
        import ip

        try:
            self.data = ip.IP.get_proto(self.nxt)(buf)
            setattr(self, self.data.__class__.__name__.lower(), self.data)
        except (KeyError, dpkt.UnpackError):
            self.data = buf


    def __len__(self):
        return self.__hdr_len__ + len(self.auth) + len(self.data)

    def __str__(self):
        return self.pack_hdr() + str(self.auth) + str(self.data)


class Readpcap():
    def __init__(self,pcpath='D:\pcap.pcap'):
        self.pc = pcap.pcap(pcpath)
    def printsocket(self):
        while True:
            aa = self.pc.next();
            if(aa == None):
                break
            (ti,pkt ) = aa;
            ff = dpkt.ethernet.Ethernet(pkt)
            print(u"源Mac地址: " + mac2str(ff.src) + u" 目的Mac地址: " + mac2str(ff.dst) )
            # Returns the Ethernet type.  For example, type 2048 (0x0800) is IPv4 and 34525 (0x86DD) is IPv6
            if(ff.type != 2048):
                continue;
            self.ippkt = ff.data;
            print "Packet size: ",
            if self.ippkt.p == 6:
                print str(self.ippkt.len)+"\t"+"tcp"
            elif self.ippkt.p == 17:
                print str(self.ippkt.len)+"\t"+"udp"
        
def test():
    mm = Readpcap()
    mm.printsocket()
       
if __name__ == "__main__":
    test()
        
