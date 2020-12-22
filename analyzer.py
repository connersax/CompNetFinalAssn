from scapy.all import *
from threading import Thread
import pandas
import time
import os
import pwd

# initialize the networks dataframe that will contain all access points nearby
networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Security"])

# set the index BSSID (MAC address of the access point)
# UID and BSSID are the same and listed twice because when the get_networks() function is called
# the BSSID will be included in the values returned
networks.set_index("BSSID", inplace=True)


def callback(packet):
    if packet.haslayer(Dot11Beacon):
        # MAC address of the network
        bssid = packet[Dot11].addr2
        
        # name of wifi network
        ssid = packet[Dot11Elt].info.decode()
        if '\x00' in ssid:
            ssid = '' # null characters show up for hidden networks. This makes the final output file look nicer
        
        # signal strength
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"
        
        # stats such as the network channel and type of security on the scanned network
        stats = packet[Dot11Beacon].network_stats()
        
        # channel of the access point
        channel = stats.get("channel")
        # there is a bug in scapy that where it doesn't read the channel correctly all the time. My solution
        # is to retrieve what the current channel of the wireless card using the iwlist program.
        if type(channel) != int:
            os.system("iw dev | awk '$1==\"channel\"{print $2}' > /tmp/current_sniff_channel")
            channel = int(open("/tmp/current_sniff_channel", "r").read())
            os.system("rm /tmp/current_sniff_channel")
        
        # get the security of the network
        security = stats.get("crypto")
        networks.loc[bssid] = (ssid, dbm_signal, channel, security)


def retrieve_channels(interface):
    os.system("iwlist %s channel | awk '$1==\"Channel\"{print $2}' > /tmp/sniff_capable_channels" %interface)
    all_ch = []
    all_ch_file = open("/tmp/sniff_capable_channels")

    for line in all_ch_file:
        all_ch.append(int(line))
    
    os.system('rm /tmp/sniff_capable_channels') # removes temporary file since there is no need for it now
    return all_ch


def change_channel(interface):
    channels = retrieve_channels(interface)
    while True:
        for ch in channels:
            os.system("iw dev | awk '$1==\"Interface\"{print $2}' > /tmp/wireless_interfaces")
            if "mon" in str(open("/tmp/wireless_interfaces", "r").readline()).strip():
                print(f"{interface} = ch{ch}")
                os.system(f"iwconfig {interface} channel {ch}")
                time.sleep(0.5)
            else:
                break


def get_networks():
    os.system("iw dev | awk '$1==\"Interface\"{print $2}' > /tmp/wireless_interfaces")
    interface = str(open("/tmp/wireless_interfaces", "r").readline()).strip()
    os.system("rm /tmp/wireless_interfaces")

    # thread that will cycle through the channels
    channel_changer = Thread(target=change_channel, args=[interface])
    channel_changer.daemon = True
    channel_changer.start()

    # scanning for Beacon Frames (Wi-Fi network packets)
    sniff(prn=callback, count=200, iface=interface)

    # outputting to file
    user = os.getenv("SUDO_USER")
    networks_sorted = networks.sort_values(by=["Channel"])
    print(networks_sorted, file=open("output.txt", 'w'))
    os.system(f"chown {user} output.txt") # changes ownership back to the user that launched the program

    # sorts the list before returning it
    networks_sorted = networks_sorted.reset_index()

    return networks_sorted.values.tolist()
    