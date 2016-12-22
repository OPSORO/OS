#!/bin/bash

sudo rm /etc/dnsmasq.d/dnsmasq.reroute_pre_opsoro.conf
sudo cp dnsmasq.reroute_all.conf /etc/dnsmasq.d/dnsmasq.reroute_all.conf

sudo service networking restart
sudo service network-manager restart

# restart hostapd and dnsmasq
sudo /etc/init.d/hostapd restart
sudo /etc/init.d/dnsmasq restart