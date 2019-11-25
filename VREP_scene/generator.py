import time
import subprocess

for i in range(10):
	print('Current simulation start #',i)
	start_time = time.time()
	process = subprocess.Popen('/root/V-REP/vrep.sh -h -s -q /root/scene/test_scene.ttt', shell=True, stdout=subprocess.PIPE)
	process.wait()
	elapsed_time = time.time() - start_time
	print("elapsed_time: ", elapsed_time)
	print("time per image: ", elapsed_time/1000)
	print("objects per minute: ", 60/elapsed_time/1000)
	print(process.returncode)
print('Complete!')