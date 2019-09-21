#This Reboots your Bolt Device

from boltiot import Bolt
mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
response = mybolt.restart()
print (response)