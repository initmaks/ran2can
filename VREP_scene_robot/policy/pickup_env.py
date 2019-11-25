import vrep,time,sys
import matplotlib.pyplot as plt
from PIL import Image as I
import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG)

class ObjectPickUpEnv():
    def __init__(self, camera_name = 'cam_1_tex', sim_ip = '127.0.0.1', sim_port = 19999):
        vrep.simxFinish(-1)
        self.clientID = vrep.simxStart(sim_ip,sim_port,True,True,5000,5)
        self.camera_name = camera_name
        if self.clientID==-1: sys.exit('Could not connect')
        # enable the synchronous mode on the client:
        self.figure = None
        self.episode_length = 50 # TODO
        
    def seed(self, seed=None):
        logging.warning("Seeding is not supported")

    def step(self, action):
        assert vrep.simxGetConnectionId(self.clientID)!=-1

        # TODO SEND THE ACTION

        vrep.simxSynchronousTrigger(self.clientID)
        res,iteration1 = vrep.simxGetIntegerSignal(self.clientID,"iteration",vrep.simx_opmode_buffer)
        if res!=vrep.simx_return_ok: iteration1=-1;
        iteration2=iteration1
        while iteration2==iteration1: # wait until the iteration counter has changed
            res, iteration2 = vrep.simxGetIntegerSignal(self.clientID,"iteration",vrep.simx_opmode_buffer)
            if res!=vrep.simx_return_ok: iteration2=-1
        logging.debug(f"iteration2: {iteration2}")
        #Get the image of the vision sensor
        res,resolution,image=vrep.simxGetVisionSensorImage(self.clientID,self.visionSensorHandle,0,vrep.simx_opmode_buffer)
        #Transform the image so it can be displayed
        self.img = np.array(image,dtype=np.uint8).reshape([resolution[1],resolution[0],3])
        done = True if iteration2 > self.episode_length else False
        reward, info = 0, {} # TODO
        return self.img, reward, done, info # TODO .copy() ?

    def reset(self):
        # stop the simulation
        vrep.simxStopSimulation(self.clientID,vrep.simx_opmode_blocking)
        vrep.simxSynchronous(self.clientID,1)
        # start the simulation
        vrep.simxStartSimulation(self.clientID,vrep.simx_opmode_blocking)
        # enable streaming of the iteration counter:
        res, iteration1 = vrep.simxGetIntegerSignal(self.clientID,"iteration",vrep.simx_opmode_streaming)
        logging.debug(f"iteration1: {iteration1}")
        #Get the handle of the vision sensor
        _,self.visionSensorHandle=vrep.simxGetObjectHandle(self.clientID,self.camera_name,vrep.simx_opmode_oneshot_wait)
        #Get the image
        _,resolution,image=vrep.simxGetVisionSensorImage(self.clientID,self.visionSensorHandle,0,vrep.simx_opmode_streaming)
        if self.figure is not None: plt.close() # try?
        self.figure = None
        return self.step(0)

    def render(self):
        if self.figure is None:
            #Initialiazation of the figure
            time.sleep(0.1) #TODO tune?
            res,resolution,image=vrep.simxGetVisionSensorImage(self.clientID,self.visionSensorHandle,0,vrep.simx_opmode_buffer)
            self.img = I.new("RGB", (resolution[0], resolution[1]), "white")
            # Init figure
            plt.ion()
            fig = plt.figure(1)
            fig.canvas.set_window_title(self.camera_name) # str(iteration2)
            self.figure = plt.imshow(self.img, origin='lower')
            time.sleep(0.1) #TODO tune?
        else:
            #Update the image
            self.figure.set_data(self.img)
            plt.draw()
            plt.pause(0.0001)

    def close(self,):
        # stop the simulation
        vrep.simxStopSimulation(self.clientID,vrep.simx_opmode_blocking)

def main():
    env = ObjectPickUpEnv()
    for epoch in range(3):
        o, r, d, i = env.reset()
        while not d:
            # TODO action_space.sample?
            o, r, d, i = env.step(0)
            env.render()
    env.close()

if __name__ == '__main__':
    main()