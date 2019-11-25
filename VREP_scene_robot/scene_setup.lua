require "scene_control"
require "camera_control"
require "helper_math"
-- random seed
math.randomseed(os.time())

TRAINING = true
episode_id = string.sub(uuid(), 1, 8)

-- FLAGS etc.
RECORD_CAMERA = true
data_folder = '/home/dl/data/vrep/robot_v0/'
-- mask_id_filename = data_folder..'mask_ids_'..episode_id..'.txt'
-- mask_id_file = io.open(mask_id_filename, "a")
textures_folder = "/home/dl/data/CAN/textures/"

img_dims = {512,512}
camera_types = {'tex'}--{'tex', 'can', 'msk'}
number_of_cameras = 2
for id = 1, number_of_cameras, 1 do
    for _, camera_type in pairs(camera_types) do
        camera_name = 'cam_'..tostring(id)..'_'..camera_type
        os.execute("mkdir " .. data_folder..camera_name) 
    end
end
captures_made = 1
captures_per_drop = 16
captures_required = 500

texture_list = {}
for texture_folder in io.popen("ls "..textures_folder):lines() do
    for texture_file in io.popen("ls "..textures_folder..'/'..texture_folder):lines() do
        table.insert(texture_list, texture_folder..'/'..texture_file)
    end
end
total_texture_count = #texture_list
texturized_objects = {}

if TRAINING then
    object_list = getObjectsHandleList('train_objects')
else
    object_list = getObjectsHandleList('test_objects')
end 

drop_height = 1.

function sysCall_init()
    init_scene()
    -- save_mask_ids()
    episode_start_time = sim.getSimulationTime()
    iteration=1
end

function sysCall_actuation()
    -- put your actuation code here
    -- For example:
    -- local position=sim.getObjectPosition(handle,-1)
    -- position[1]=position[1]+0.001
    -- sim.setObjectPosition(handle,-1,position)
end

function episode()
    elapsed_time = sim_time - episode_start_time
    -- process_camera()
    -- if elapsed_time > 30.0 then -- every N image captures OR M seconds
    --     -- restart the episode
    --     episode_start_time = sim.getSimulationTime() 
    --     move_table()
    --     drop_objects(object_list, drop_height)
    -- end
    -- if elapsed_time > 0.3 then
    --     -- enable_shadows(true)
    --     if RECORD_CAMERA then
    --         -- retexturize()
    --         -- move_light()
    --         -- move_camera()
    --         -- process_camera()
    --         captures_made = captures_made + 1
    --     end 
    -- else
    --     enable_shadows(false)
    -- end

    -- -- STOP SIMULATOR IF REQUIRED AMOUNT OF DATA IS COLLECTED
    -- if captures_made > captures_required then
    --     sim.stopSimulation()
    -- end
end

function sysCall_sensing()
    sim_time = sim.getSimulationTime()
    simSetIntegerSignal('iteration',iteration)
    iteration=iteration+1
    episode()
    -- if captures_made%10 == 0 then
    --     print(tostring(60/(sim_time/captures_made)).."objects per minute (simulation time")
    -- end
end

function default_setup()
    floor_obj = sim.getObjectHandle('PlainFloor')
    sim.setShapeTexture(floor_obj, -1, sim.texturemap_plane, 0, {1.0,1.0})
end

function sysCall_cleanup()
    simClearIntegerSignal('iteration')
    clean_collections()
    default_setup()
end

-- You can define additional system calls here:
--[[
function sysCall_suspend()
end

function sysCall_resume()
end

function sysCall_dynCallback(inData)
end

function sysCall_jointCallback(inData)
    return outData
end

function sysCall_contactCallback(inData)
    return outData
end

function sysCall_beforeCopy(inData)
    for key,value in pairs(inData.objectHandles) do
        print("Object with handle "..key.." will be copied")
    end
end

function sysCall_afterCopy(inData)
    for key,value in pairs(inData.objectHandles) do
        print("Object with handle "..key.." was copied")
    end
end

function sysCall_beforeDelete(inData)
    for key,value in pairs(inData.objectHandles) do
        print("Object with handle "..key.." will be deleted")
    end
    -- inData.allObjects indicates if all objects in the scene will be deleted
end

function sysCall_afterDelete(inData)
    for key,value in pairs(inData.objectHandles) do
        print("Object with handle "..key.." was deleted")
    end
    -- inData.allObjects indicates if all objects in the scene were deleted
end
--]]
