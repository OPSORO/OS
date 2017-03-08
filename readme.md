# OnoSW
OnoSW is the software framework for [OPSORO](http://www.opsoro.be/), to be used in conjunction with [Ono2](https://github.com/cesarvandevelde/Ono2) and [OnoHAT](https://github.com/cesarvandevelde/OnoHAT).

# Hardware Requirements
- Raspberry Pi 1 model B+ | Raspberry Pi 2 model B | Raspberry Pi 3
- [OnoHAT](https://github.com/cesarvandevelde/OnoHAT)
- WiFi dongle that supports AP-mode (e.g. [WiPi](http://be.farnell.com/element14/wipi/dongle-wifi-usb-for-raspberry/dp/2133900?ost=wipi&categoryId=700000005571))
- Separate power supplies for logic (5V 2A) and servos (5V 10A), these can be connected directly to the OnoHAT

# Installation
1. Start with a fresh Raspbian install
2. Copy the contents the folder /OnoSW/ to /home/pi/OnoSW/
3. Copy the contents the folder /Scripts/ to /home/pi/Scripts/
4. Update your system

    ```
    sudo apt-get update
    sudo apt-get upgrade
    ```
5. Install Python development files, Avahi daemon, LuaJIT

    ```
    sudo apt-get install python2.7-dev avahi-daemon libluajit-5.1-dev git
    ```

6. Install PIP

    ```
    sudo apt-get install python-setuptools
    sudo easy_install pip
    ```

7. [Compile and install LibYAML](http://pyyaml.org/wiki/LibYAML)  
    Or run following command:  
    ```
    sudo apt-get install python-yaml
    ```

    This step is not strictly necessary, but will result in a massive speedup when parsing config files. The python version of PyYAML takes well over 3 seconds to parse the configs, the C version takes only a fraction of that.

8. Install Python packages (flask, flask-login, pyyaml, pluginbase, sockjs-tornado, simplejson, lupa, numpy, scipy, spidev)

    ```
    sudo pip install flask flask-login pyyaml pluginbase sockjs-tornado simplejson lupa numpy spidev gitpython flask-babel noise pyserial enum enum34 requests tweepy
    sudo apt-get install -y python-smbus i2c-tools
    sudo apt-get install -y python-scipy
    ```

9. Enable SPI and I2C

    ```
    sudo raspi-config
    ```

    Go to advanced, A5 SPI --> Enable, A6 --> I2C enable.

10. Edit /etc/modules

    ```
    sudo nano /etc/modules
    ```

    Enter the following configuration

    ```
    # /etc/modules: kernel modules to load at boot time.
    #
    # This file contains the names of kernel modules that should be loaded
    # at boot time, one per line. Lines beginning with "#" are ignored.
    # Parameters can be specified after the module name.

    #snd-bcm2835
    i2c-bcm2708
    i2c-dev
    snd_soc_core
    snd_soc_bcm2708_i2s
    bcm2708_dmaengine
    snd_soc_pcm1794a
    snd_soc_rpi_dac
    ```
    Edit /etc/modprobe.d/raspi-blacklist.conf and make the file is empty. (no modules blacklisted)  

    ```
    sudo nano /etc/modprobe.d/raspi-blacklist.conf
    ```
11. Configure audio
    Add hifiberry-dac device tree overlay in config.txt (```sudo nano /boot/config.txt```). And add the following to the end of the config.txt file
    ```
    dtoverlay=hifiberry-dac
    ```
    If present, change ```dtparam=audio=on``` to ```#dtparam=audio=on```

    Configure ALSA

    ```
    sudo nano /etc/asound.conf
    ```

    Enter the following configuration

    ```
    pcm.!default {
      type        softvol
      slave.pcm   dac
      control {
        name      "Master"
        card      0
      }
    }

    pcm.dac {
      type plug
      slave {
        pcm       "hw:0,0"
        format     S16_LE
        channels   2
        rate       48000
      }
    }
    ```

    Reboot the Raspberry Pi

    ```
    sudo reboot
    ```

    Lower the master sound volume to something reasonable (limits 0-255)

    ```
    amixer set Master 128
    ```

12. [Install PicoTTS](http://rpihome.blogspot.be/2015/02/installing-pico-tts.html)

    ```
    sudo apt-get install libttspico-utils
    ```

13. Install the eSpeak TTS engine

    ```
    sudo apt-get install espeak
    ```

14. Setup and configure the WiFi dongle  
    Install hostapd for the access point and dnsmasq for the DHCP server and DNS redirect

    ```
    sudo apt-get install -y hostapd dnsmasq
    ```

    Update ```/etc/network/interfaces``` so it matches following lines

    ```
    auto lo
    iface lo inet loopback

    allow-hotplug eth0
    iface eth0 inet manual

    #allow-hotplug wlan0
    #iface wlan0 inet manual
    #    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

    #allow-hotplug wlan1
    #iface wlan1 inet manual
    #    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

    allow-hotplug wlan0
    auto wlan0
    iface wlan0 inet static
       address 192.168.42.1
       netmask 255.255.255.0
       broadcast 192.168.42.255

    # reset existing rules and chains
    up /sbin/iptables -F
    up /sbin/iptables -X
    up /sbin/iptables -t nat -F

    # Mask for the interface, activate port-forwarding and NAT
    up iptables -A FORWARD -o eth0 -i wlan0 -s 192.168.42.0/24 -m conntrack --ctstate NEW -j ACCEPT
    up iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

    up iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    up sysctl -w net.ipv4.ip_forward=1

    # restart hostapd and dnsmasq
    up /etc/init.d/hostapd restart
    up /etc/init.d/dnsmasq restart
    ```

    Use the following configuration for /etc/hostapd/hostapd.conf

    ```
    interface=wlan0
    driver=nl80211
    ssid=OpSoRo_Robot
    ieee80211n=1          # 802.11n support
    wmm_enabled=1         # QoS support
    ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]
    hw_mode=g
    channel=6
    macaddr_acl=0
    auth_algs=1
    ignore_broadcast_ssid=0
    wpa=2
    wpa_key_mgmt=WPA-PSK
    wpa_passphrase=opsoro123
    rsn_pairwise=CCMP
    ```

    Edit the file /etc/default/hostapd and change the line ```#DAEMON_CONF=""``` to ```DAEMON_CONF="/etc/hostapd/hostapd.conf"```

    Configure the DHCP server and DNS redirect  
    Create new config file (```sudo nano /etc/dnsmasq.d/dnsmasq.opsoro.conf```) and paste following lines

    ```
    # Redirect specific urls
    address=/play.opsoro.be/192.168.42.1

    # DHCP-Server active for the wlan interface
    interface=wlan0

    # IP-Address range / Lease-Time
    dhcp-range=interface:wlan0,192.168.42.100,192.168.42.200,infinite
    ```

15. Change the host name to "opsoro"  
    In the files '/etc/hostname' and '/etc/hosts', change 'raspberrypi' to 'opsoro'

    ```
    sudo nano /etc/hostname
    sudo nano /etc/hosts
    ```

16. Setup Opsoro service  
    The script for setting up opsoro can be found in /Scripts/.  
    Follow next steps to setup OpSoRo

    ```
    sudo cd /home/pi/Scripts/
    sudo chmod +x setup_opsoro
    sudo ./setup_opsoro
    ```

OnoSW and its dependencies should now all be installed and working. Reboot the Raspberry Pi to test. Please let us know if any steps are missing!

# Use
If everything was configured correctly, the Raspberry Pi should create a WiFi hotspot (OPSORO_Robot) at startup (Default password: opsoro123). This network lets access the robot's web interface. Once connected to the network, open a browser and go to http://opsoro.local. If you configured the DHCP and DNS server correctly http://play.opsoro.be should also work. You will be presented with a login screen, the default password is: opsoro123. The main interface lets you control the robot through a number of apps.

### Notes:
- Be sure to properly shut down the operating system! Cutting power without performing a proper shutdown can corrupt the file system on the SD card, requiring a reinstall.
- The opsoro.local address only works on computers that have Bonjour. If you are using OS X or have iTunes installed, you already have Bonjour. Bonjour can also be downloaded [here](https://www.apple.com/support/bonjour/). The web interface can also be accessed by entering the IP-address in your browser, which is 192.168.42.1.
- If the Raspberry Pi is connected to the internet via ethernet, the hotspot will also allow internet access. Additionally, the web interface will be accessible from the parent network using the opsoro.local address.
- Only one user can be logged into the software. This is to prevent conflicting commands from multiple clients. It is possible to overwrite this behaviour inside apps, if desired.
- The code from the visual programming app is currently executed in the browser, which then sends raw commands to the web server. This causes minor bugs, which is why future versions will run the generated code on the server.
- To create custom apps, please look at the examples in /OnoSW/apps/. Apps are self-contained within their folder inside /apps/, and are automatically detected and activated by the software.


# More info
More information about this project can be found on [our website](http://www.opsoro.be/).  
Also be sure to check out the [main repository](http://www.github.com/cesarvandevelde/ono2), which contains all the mechanical design files.  
If you have any questions concerning this project, feel free to contact us at info [at] opsoro [dot] be

Copyright (C) 2016 OPSORO.

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
