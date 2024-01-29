#!/usr/bin/python3
import socket
import argparse
import ipaddress
import sys
import getCloudflare, getCloudfront, getMerlinCDN
from prettytable import PrettyTable
import threading, time, random
from queue import Queue

parser = argparse.ArgumentParser(description="Take a list of IPs or domains, checks if they are pointing to a Content Delivery Network")
parser.add_argument('-dL', dest='domainlist', required=False, help='A list of domains to resolve and check if they are in-scope')
parser.add_argument('-iL', dest='iplist', required=False, help='A list of IP addresses to check against the in-scope list')
parser.add_argument('-tS', dest='tablesort', required=False, help='Specify to sort by domain, ip, or CDN')
args = parser.parse_args()

def build_cdn_list():
        cdnProviders = ['cloudflare', 'cloudfront', 'merlin']
        providerIPRanges = [getCloudflare.get_cloudflare_cdn_ranges(), getCloudfront.get_cloudfront_cdn_ranges(), getMerlinCDN.get_merlin_cdn_ranges()]
        return dict(zip(cdnProviders, providerIPRanges))

def check_if_cdn_ip(ip_to_check, cdnlist):
        for provider in cdnlist.keys():
                for cdn_iprange in cdnlist[provider]: 
                        if ipaddress.ip_address(ip_to_check) in ipaddress.ip_network(cdn_iprange):
                                return provider
        return "None"

def resolve_domain(jobs):
        #print("Threaded job for domain ", domain)
        while not jobs.empty():
                domain, cdnList, t, failed_to_resolve = jobs.get()
                try:
                        ipaddress = socket.gethostbyname(domain.strip())
                        #print("Hostname {0}\t|\t IPAddress {1}\t|\t {2}".format(domain.strip(), ipaddress, check_if_cdn_ip(ipaddress, cdnList)))
                        t.add_row([domain, ipaddress, check_if_cdn_ip(ipaddress, cdnList)])
                except:
                        failed_to_resolve.append(domain)
                jobs.task_done()


def check_domains():
        cdnList = build_cdn_list()
        domain_array = []
        failed_to_resolve = []
        jobs = Queue()

        with open(args.domainlist) as domain_list:
                for line in domain_list:
                        domain_array.append(line)

        t = PrettyTable(['Hostname', 'IP Address', 'CDN Provider'])
        if domain_array:
                for domain in domain_array:
                        jobs.put([domain, cdnList, t, failed_to_resolve])
        else:
                print("Error: No domains loaded from ", domainlist)

        for i in range(300):
                worker = threading.Thread(target=resolve_domain, args=(jobs,))
                worker.start()

        print("Waiting for queue to complete", jobs.qsize(), "tasks")
        jobs.join()
        return t, failed_to_resolve

def check_iplist():
        cdnList = build_cdn_list()
        ip_list = []
        with open(args.iplist) as readips:
                for line in readips:
                        ip_list.append(line)

        t = PrettyTable(['IP Address', 'CDN Provider'])
        if ip_list:
                for ipaddr in ip_list:
                        t.add_row(ipaddress, check_if_cdn_ip(ipaddress, cdnList))
                        #print("IP Address {0}\t|\t {1}".format(ipaddr, check_if_cdn_ip(ipaddr, cdnList)))
        else:
                print("Error: No IP Addresses loaded from", iplist)


if __name__ == '__main__':                                                                                                                                                                                                           
        if args.domainlist:
                table, failed_to_resolve = check_domains()
                if args.tablesort:
                        print(table.get_string(sortby=args.tablesort))
                else:
                        print(table)
                print("Finished! Failed to resolve {0} domains.".format(len(failed_to_resolve)))
        elif args.iplist:
                table = check_iplist()
                print(table)
        else:
                print("Error: Please select from IP List (-iL) or Domain List (-dL)")
