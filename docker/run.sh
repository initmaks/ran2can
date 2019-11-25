docker run -d \
		   -p 5902:5900 \
		   --name vrep2 \
		   -v /home/dl/Projects/CAN/VREP_scene:/root/scene/ \
		   -v /home/dl/:/home/dl/ \
		   vrep