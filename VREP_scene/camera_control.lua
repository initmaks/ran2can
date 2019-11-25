function save_mask_ids()
    output_string = "#"..episode_id..","
    for ix, obj in pairs(object_list) do
        object_name = sim.getObjectName(obj)
        obj_id = tostring(obj)
        output_string = output_string..'('..object_name..' '..obj_id..'),' 
    end
    mask_id_file:write(output_string,'\n') -- TODO save to file
end

function process_camera()
    img_id = episode_id..'_'..tostring(sim_time) 
    for cam_id = 1, number_of_cameras, 1 do
        for _, camera_type in pairs(camera_types) do
            camera_name = 'cam_'..tostring(cam_id)..'_'..camera_type
            cam = sim.getObjectHandle(camera_name)
            img = sim.getVisionSensorCharImage(cam)
            r = sim.saveImage(img, img_dims, 0, data_folder..camera_name..'/'..img_id..'.png',100)
        end
    end
    -- depth = sim.getVisionSensorDepthBuffer(cam)
    -- depth_str = sim.packTable(depth)
end

function enable_shadows(shadows_on)
	if shadows_on then
		mode = 3
	else
		mode = 0
	end
    for cam_id = 1, number_of_cameras, 1 do
		cam = sim.getObjectHandle('cam_'..tostring(cam_id)..'_tex')
		sim.setObjectInt32Parameter(cam, sim.visionintparam_render_mode, mode)
	end
end

function move_camera()
    camera_type = 'tex'
    for cam_id = 1, number_of_cameras, 1 do
        camera_name = 'cam_'..tostring(cam_id)..'_'..camera_type
        cam = sim.getObjectHandle(camera_name)
        cam_x = randomFloat(-0.5,0.5)
        cam_y = randomFloat(-0.5,0.5)
        cam_z = 2
        cam_alpha = math.pi - math.rad(40 * cam_y) -- linear rotation of the camera to the "center" of table
        cam_beta = math.rad(-30 * cam_x)
        cam_gamma = math.pi 
        sim.setObjectPosition(cam, -1, {cam_x,cam_y,cam_z})
        sim.setObjectOrientation(cam, -1, {cam_alpha, cam_beta, cam_gamma})
    end
end

function move_light()
    light = sim.getObjectHandle("light")
    x = randomFloat(0,2.5)
    y = randomFloat(0,2.5)
    z = randomFloat(0,2.5)
    sim.setObjectPosition(light, -1, {x,y,z})
end