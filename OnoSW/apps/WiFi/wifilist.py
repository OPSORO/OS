from wifi import Cell, Scheme
import time
from subprocess import call

# get all cells from the air
ssids = [cell.ssid for cell in Cell.all('wlan0')]

for ssid in ssids:
	print ssid



# cell = Cell.all('wlan0')[8]
# print cell
# scheme = Scheme.for_cell('wlan0', 'ONO_Assistant', cell)
# scheme.save()
# scheme.activate()

# print scheme
# scheme = Scheme.find('wlan0', 'ONO_Assistant')
# scheme.activate()
