import vrep,time,sys
import matplotlib.pyplot as plt
from PIL import Image as I
import numpy as np

def streamVisionSensor(visionSensorName,clientID,pause=0.0001):
     # enable the synchronous mode on the client:
    vrep.simxSynchronous(clientID,1)

    # start the simulation:
    vrep.simxStartSimulation(clientID,vrep.simx_opmode_blocking)

    # enable streaming of the iteration counter:
    res, iteration1 = vrep.simxGetIntegerSignal(clientID,"iteration",vrep.simx_opmode_streaming)
    print("iteration1: ", iteration1)
    #Get the handle of the vision sensor
    res1,visionSensorHandle=vrep.simxGetObjectHandle(clientID,visionSensorName,vrep.simx_opmode_oneshot_wait)
    #Get the image
    res2,resolution,image=vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_streaming)
    #Initialiazation of the figure
    time.sleep(0.5)
    res,resolution,image=vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_buffer)
    im = I.new("RGB", (resolution[0], resolution[1]), "white")
    # Init figure
    plt.ion()
    fig = plt.figure(1)
    plotimg = plt.imshow(im, origin='lower')
    #Let some time to Vrep in order to let him send the first image, otherwise the loop will start with an empty image and will crash
    time.sleep(1)
    while (vrep.simxGetConnectionId(clientID)!=-1):
        if iteration1 < 30:
            vrep.simxSynchronousTrigger(clientID)
            res,iteration1 = vrep.simxGetIntegerSignal(clientID,"iteration",vrep.simx_opmode_buffer)
            if res!=vrep.simx_return_ok: iteration1=-1;
            iteration2=iteration1
            while iteration2==iteration1: # wait until the iteration counter has changed
                res, iteration2 = vrep.simxGetIntegerSignal(clientID,"iteration",vrep.simx_opmode_buffer)
                if res!=vrep.simx_return_ok:
                    iteration2=-1
            print(iteration2)

            #Get the image of the vision sensor
            res,resolution,image=vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_buffer)
            #Transform the image so it can be displayed
            img = np.array(image,dtype=np.uint8).reshape([resolution[1],resolution[0],3])
            #Update the image
            fig.canvas.set_window_title(visionSensorName + '_' + str(iteration2))
            plotimg.set_data(img)
            plt.draw()
            plt.pause(pause)
        # vrep.simxSynchronousTrigger(clientID)
    print('End of Simulation')
    
if __name__ == '__main__':
    vrep.simxFinish(-1)
    clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
    if clientID!=-1:
        print('Connected to remote API server')
        streamVisionSensor('cam_1_tex',clientID,0.0001)

    else:
        print('Connection non successful')
        sys.exit('Could not connect')