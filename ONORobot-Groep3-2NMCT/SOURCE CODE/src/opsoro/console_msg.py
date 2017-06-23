def print_info(msg):
    print("\033[1m[\033[96m INFO \033[0m\033[1m]\033[0m %s" % msg)


def print_warning(msg):
    print("\033[1m[\033[93m WARN \033[0m\033[1m]\033[0m %s" % msg)


def print_error(msg):
    print("\033[1m[\033[91m ERRO \033[0m\033[1m]\033[0m %s" % msg)


def print_apploaded(appname):
    print("\033[1m[\033[92m APP LOADED \033[0m\033[1m]\033[0m %s" % appname)


def print_appstarted(appname):
    print("\033[1m[\033[92m APP STARTED \033[0m\033[1m]\033[0m %s" % appname)


def print_appstopped(appname):
    print("\033[1m[\033[93m APP STOPPED \033[0m\033[1m]\033[0m %s" % appname)


def print_spi(msg):
    print("\033[1m[\033[94m SPI \033[0m\033[1m]\033[0m %s" % msg)
