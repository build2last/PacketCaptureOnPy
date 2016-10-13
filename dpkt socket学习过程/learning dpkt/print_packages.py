# coding:utf-8
"""
2016-09-29
TESTED OK !

Use DPKT to read in a pcap file and print out the contents of the packets
This example is focused on the fields in the Ethernet Frame and IP packet
"""
import dpkt
import datetime
import socket
import pcap
import readhttp

def mac_addr(address):
    """Convert a MAC address to a readable/printable string

       Args:
           address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
       Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02x' % ord(b) for b in address)



def inet_to_str(inet):
    """Convert inet object to a string

        Args:
            inet (inet struct): inet network address
        Returns:
            str: Printable/readable IP address
    """
    # First try ipv4 and then ipv6
    try:
        return socket.inet_ntoa(inet) # change here socket.AF_INET, 
    except ValueError:
        return socket.inet_ntoa(inet) # socket.AF_INET6,


def print_packets(pcap):
    """Print out information about each packet in a pcap
       Args:
           pcap: dpkt pcap reader object (dpkt.pcap.Reader)
    """
    # For each packet in the pcap process the contents
    for timestamp, buf in pcap:
        data_dict = readhttp.main_pcap(timestamp, buf)
        if data_dict:
            print data_dict
        # Print out the timestamp in UTC
        # print 'Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp))

        # Unpack the Ethernet frame (mac src/dst, ethertype)
        eth = dpkt.ethernet.Ethernet(buf)
        #print 'Ethernet Frame: ', mac_addr(eth.src), mac_addr(eth.dst), eth.type
        # Make sure the Ethernet data contains an IP packet
        #if not isinstance(eth.data, dpkt.ip.IP):
        #    print 'Non IP Packet type not supported %s\n' % eth.data.__class__.__name__
        #    continue

        # Now unpack the data within the Ethernet frame (the IP packet)
        # Pulling out src, dst, length, fragment info, TTL, and Protocol
        #ip = eth.data

        # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
        #do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
        #more_fragments = bool(ip.off & dpkt.ip.IP_MF)
        #fragment_offset = ip.off & dpkt.ip.IP_OFFMASK

        # Print out the info
        #print 'IP: %s -> %s   (len=%d ttl=%d DF=%d MF=%d offset=%d)\n' % \
        #      (inet_to_str(ip.src), inet_to_str(ip.dst), ip.len, ip.ttl, do_not_fragment, more_fragments, fragment_offset)
        """
        for i in str(buf).split('\n'):
            # if "text/html" not in str(buf):
            #    continue
            try:
                print i.decode("utf-8")
            except Exception as e:
                continue
        """
        
def test():
    """Open up a test pcap file and print out the packets"""
    pc=pcap.pcap("D:\pcap.pcap")
    # pc = pcap.pcap()
    print_packets(pc)



if __name__ == '__main__':
    test()
