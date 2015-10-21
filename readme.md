# OnoSW
OnoSW is the software framework for [social robot Ono](http://www.industrialdesigncenter.be/ono/), to be used in conjunction with [Ono2](https://github.com/cesarvandevelde/Ono2) and [OnoHAT](https://github.com/cesarvandevelde/OnoHAT).

# Hardware Requirements
- Raspberry Pi model B+ (RPi 2 model B should also work)
- [OnoHAT](https://github.com/cesarvandevelde/OnoHAT)
- WiFi dongle that supports AP-mode (e.g. [WiPi](http://be.farnell.com/element14/wipi/dongle-wifi-usb-for-raspberry/dp/2133900?ost=wipi&categoryId=700000005571))
- Separate power supplies for logic (5V 2A) and servos (5V 10A), these can be connected directly to the OnoHAT

# Installation
1. Start with a fresh Raspbian install
2. Downgrade kernel to pre-3.18. This workaround is needed because more recent kernels use device tree, which causes timeout errors on the I2C bus. I have not found a better solution yet, unfortunately.

    ```
    sudo rpi-update f74b92120e0d469fc5c2dc85b2b5718d877e1cbb
    ```
3. Copy the contents the folder /OnoSW/ to /home/pi/OnoSW/
4. Update your system

    ```
    sudo apt-get update
    sudo apt-get upgrade
    ```
5. Install Python development files, Avahi daemon, LuaJIT

    ```
    sudo apt-get install python2.7-dev avahi-daemon libluajit-5.1-dev
    ```

6. Install PIP:

    ```
    sudo apt-get install python-setuptools
    sudo easy_install pip
    ```

7. [Compile and install LibYAML](http://pyyaml.org/wiki/LibYAML)  
This step is not strictly necessary, but will result in a massive speedup when parsing config files. The python version of PyYAML takes well over 3 seconds to parse the configs, the C version takes only a fraction of that.
8. Install Python packages (flask, flask-login, pyyaml, pluginbase, sockjs-tornado, simplejson, lupa, numpy, scipy, spidev)

    ```
    sudo pip install flask flask-login pyyaml pluginbase sockjs-tornado simplejson lupa numpy scipy spidev
    ```

9. Disable Device Tree, enable SPI and I2C.

    ```
    sudo raspi-config
    ```
    
    Go to advanced, A5 Device Tree --> Disable, A6 SPI --> Enable, A7 --> I2C enable.

10. Edit /etc/modules:

    ```
    sudo nano /etc/modules
    ```
    
    Enter the following configuration:
    
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
11. Configure ALSA:
    
    ```
    sudo nano /etc/asound.conf
    ```
    
    Enter the following configuration:
    
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
    
    Reboot the Raspberry Pi:
    
    ```
    sudo reboot
    ```
    
    Lower the master sound volume to something reasonable (limits 0-255):
    
    ```
    amixer set Master 128
    ```
    
12. [Install PicoTTS](http://rpihome.blogspot.be/2015/02/installing-pico-tts.html)
13. [Setup and configure the WiFi dongle](http://elinux.org/RPI-Wireless-Hotspot)  
Use the following configuration for /etc/hostapd/hostapd.conf:

    ```
    interface=wlan0
    driver=nl80211
    ssid=Ono_AP
    hw_mode=g
    channel=6
    macaddr_acl=0
    auth_algs=1
    ignore_broadcast_ssid=0
    wpa=2
    wpa_passphrase=RobotOno
    wpa_key_mgmt=WPA-PSK
    wpa_pairwise=TKIP
    rsn_pairwise=CCMP
    ```

14. [Change the host name to "ono"](http://www.raspians.com/Knowledgebase/how-to-change-hostname-on-raspberrypi/)
15. [Setup a daemon for Ono](http://blog.scphillips.com/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/)  
The script for the daemon can be found in /Scripts/onosw.sh.  
Make sure the main OnoSW python script is executable!

    ```
    sudo chmod 755 /home/pi/OnoSW/main.py  
    ```

OnoSW and its dependencies should now all be installed and working. Reboot the Raspberry Pi to test. Please let me know if any steps are missing!

# Use
If everything was configured correctly, the Raspberry Pi should create a WiFi hotspot (Ono_AP) at startup. This network lets access the robot's web interface. Once connected to the network, open a browser and go to http://ono.local. You will be presented with a login screen, the default password is "RobotOno". The main interface lets you control the robot through a number of apps.

### Notes:
- Be sure to properly shut down the operating system! Cutting power without performing a proper shutdown can corrupt the file system on the SD card, requiring a reinstall.
- The ono.local address only works on computers that have Bonjour. If you are using OS X or have iTunes installed, you already have Bonjour. Bonjour can also be downloaded [here](https://www.apple.com/support/bonjour/). The web interface can also be accessed by entering the IP-address in your browser, which is 192.168.42.1.
- If the Raspberry Pi is connected to the internet via ethernet, the hotspot will also allow internet access. Additionally, the web interface will be accessible from the parent network using the ono.local address.
- Only one user can be logged into the software. This is to prevent conflicting commands from multiple clients. It is possible to overwrite this behaviour inside apps, if desired.
- The code from the visual programming app is currently executed in the browser, which then sends raw commands to the web server. This causes minor bugs, which is why future versions will run the generated code on the server.
- To create custom apps, please look at the examples in /OnoSW/apps/. Apps are self-contained within their folder inside /apps/, and are automatically detected and activated by the software.


# More info
More information about this project can be found on [our website](http://www.industrialdesigncenter.be/ono/).  
Also be sure to check out the [main repository](http://www.github.com/cesarvandevelde/ono2), which contains all the mechanical design files.  
If you have any questions concerning this project, feel free to contact me at cesar [dot] vandevelde [at] ugent [dot] be

Copyright (C) 2015 Cesar Vandevelde.

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
