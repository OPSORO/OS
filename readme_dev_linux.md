# OPSORO OS
The OPSORO OS is the software framework for [OPSORO](http://www.opsoro.be/), and can be used in conjunction with [OPSORO HAT](https://github.com/OPSORO/HAT).

# Hardware Requirements
- Linux
- Tested with Ubuntu Mate

# Installation
1. Start with a fresh Raspbian or ubuntu install
2. Update your system
    ```
    sudo apt-get update
    sudo apt-get upgrade
    ```

3. Install Python development files, Avahi daemon, LuaJIT, git
    ```
    sudo apt-get install python2.7-dev avahi-daemon libluajit-5.1-dev git
    ```

4. Create OPSORO folder and Download Source code
    ```
    mkdir /OPSORO
    git clone https://github.com/opsoro/os.git
    ```

5. Install PIP, virtual environment
    ```
    sudo apt-get install python-setuptools
    sudo apt-get install virtualenv
    sudo easy_install pip
    ```

6. [Compile and install LibYAML](http://pyyaml.org/wiki/LibYAML)  
    Or run following command:  
    ```
    sudo apt-get install python-yaml
    ```

    This step is not strictly necessary, but will result in a massive speedup when parsing config files. The python version of PyYAML takes well over 3 seconds to parse the configs, the C version takes only a fraction of that.


7. Create and activate virtual environment
    ```
    mkvirtualenv -p python2.7 opsoro
    source opsoro/bin/activate
    ```

8. Install Python packages (flask, flask-login, pyyaml, pluginbase, sockjs-tornado, simplejson, lupa, numpy, scipy, spidev, gitpython, flask-babel, noise, pyserial, requests, tweepy)

    ```
    sudo pip install flask flask-login pyyaml pluginbase sockjs-tornado simplejson lupa numpy gitpython flask-babel noise pyserial requests tweepy -U
    sudo apt-get install -y python-smbus i2c-tools -U
    ```
9. Install scipy
    ```
    sudo pip install scipy -U
    ```
    OR
    ```
    sudo apt-get install -y python-scipy -U
    ```

10. [Install PicoTTS](http://rpihome.blogspot.be/2015/02/installing-pico-tts.html)
    ```
    sudo apt-get install libttspico-utils
    ```

11. Install the eSpeak TTS engine
    ```
    sudo apt-get install espeak
    ```


12. Activate virtual environment and run server
    ```
    source opsoro/bin/activate
    sudo python /OPSORO/OS/run
    ```

The OPSORO OS and its dependencies should now all be installed and working.

# Use
If everything was configured correctly, open a browser and go to http://localhost or http://127.0.0.1. I you have an Internet connection, You will be presented with a login screen, the default password is: opsoro123. The main interface lets you control the robot through a number of apps.


### Notes:
- To create custom apps, please look at the examples in the apps folder. Apps are self-contained within their folder inside /apps/, and are automatically detected and activated by the software.

# More info
More information about this project can be found on [our website](https://www.opsoro.be/).  
Also be sure to check out the [Design files](https://www.github.com/OPSORO/BUILD), which contains all the mechanical design files.
If you have any questions concerning this project, feel free to contact us at info [at] opsoro [dot] be.

Copyright (C) 2017 OPSORO.

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
