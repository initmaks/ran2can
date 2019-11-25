function getRandomTexture()
    return textures_folder..texture_list[math.random(total_texture_count)]
end

function spawnModel(objType, reference, position, orientation)
    if objType == 'model' then
        obj = sim.loadModel(reference)
    elseif objType == 'object' then
        obj = reference
    elseif objType == 'box_side' then
        obj = sim.createPureShape(0,2+8+16,{0.8,0.01,0.2},1)
        sim.setObjectSpecialProperty(obj, sim.objectspecialproperty_renderable)
    elseif objType == 'box_bottom' then
        obj = sim.createPureShape(0,2+8+16,{0.8,0.01,0.8},1)
        sim.setObjectSpecialProperty(obj, sim.objectspecialproperty_renderable)
    else -- simple non-renderable
        obj = sim.createPureShape(0,2+8,{0.1,0.1,0.1},1)
    end
    sim.setObjectPosition(obj, -1, position)
    sim.setObjectOrientation(obj, -1, orientation)
    return obj
end

function retexturize()
    for _, obj in pairs(texturized_objects) do
        shapeHandle,textureId,resolution=sim.createTexture(getRandomTexture(),0)
        sim.setShapeTexture(obj, textureId, sim.texturemap_plane, 4+8, {1.0,1.0}, nil, {0,randomFloat(-math.pi/2,math.pi/2),randomFloat(-math.pi/2,math.pi/2)})
        sim.removeObject(shapeHandle)
    end
end

function create_table(table_height)
    -- load table
    table_obj = spawnModel('model','models/furniture/tables/customizable table.ttm', {0,0,table_height},{0,0,0})
    sim.addObjectToCollection(canonical_collection, table_obj, sim_handle_single, 0)
    -- Apple texture to the table top
    table_top = sim.getObjectHandle("customizableTable_tableTop")
    sim.addObjectToCollection(canonical_collection, table_top, sim_handle_single, 0)
    table_top_tex = sim.copyPasteObjects({table_top}, 0)[1]
    table.insert(texturized_objects, table_top_tex)
    sim.setObjectParent(table_top_tex, table_obj, 0)

    -- construct box
    box_height = table_height 
    shift_from_center = 0.45
    for id, i in pairs({{0,-1},{0,1},{1,0},{-1,0}}) do
        x, y = i[1], i[2]
        table_position = {shift_from_center * x,  shift_from_center * y, box_height + 0.1}
        table_orientation = {(math.pi/4) * -y,(math.pi/4) * x,(math.pi/2) * x}
        box_side_obj = spawnModel('box_side', tostring(id), table_position, table_orientation)
        sim.setObjectParent(box_side_obj, table_obj, 0)
        -- Texturized object
        sim.addObjectToCollection(canonical_collection, box_side_obj, sim_handle_single, 0)
        box_side_obj_tex = sim.copyPasteObjects({box_side_obj}, 0)[1]
        table.insert(texturized_objects, box_side_obj_tex)
        sim.setObjectParent(box_side_obj_tex, table_obj, 0)
    end
    table_position = {0,  0, box_height+ 0.05}
    table_orientation = {math.pi/2,0,0}
    box_side_obj = spawnModel('box_bottom', '', table_position, table_orientation)
    sim.setObjectParent(box_side_obj, table_obj, 0)
    -- Texturized object
    sim.addObjectToCollection(canonical_collection, box_side_obj, sim_handle_single, 0)
    box_side_obj_tex = sim.copyPasteObjects({box_side_obj}, 0)[1]
    table.insert(texturized_objects, box_side_obj_tex)
    sim.setObjectParent(box_side_obj_tex, table_obj, 0)
end

function move_table()
    table_obj = sim.getObjectHandle('customizableTable')
    sim.setObjectPosition(table_obj, -1, {0,0,table_height + randomFloat(-0.15,0.15)})
end

function drop_objects(object_list, drop_height)
    -- drop objects
    object_list = shuffle(object_list)
    drop_n_objects = gaussian(#object_list/2, #object_list/2)
    drop_n_objects = math.floor(drop_n_objects)
    drop_n_objects = math.min(drop_n_objects,#object_list)
    drop_n_objects = math.max(drop_n_objects,1)
    for ix, object_handle in pairs(object_list) do
        if TRAINING and ix > drop_n_objects then
            obj_z = -1
        else
            obj_z = drop_height + randomFloat(-0.2,0.2)
        end
        obj_x = randomFloat(-0.3,0.3)
        obj_y = randomFloat(-0.3,0.3)
        obj_alpha = randomFloat(-math.pi,math.pi)
        obj_beta = randomFloat(-math.pi,math.pi)
        obj_gamma = randomFloat(-math.pi,math.pi)
        obj = spawnModel('object', object_handle,   {obj_x, obj_y, obj_z}, {obj_alpha,obj_beta,obj_gamma})
        sim.addObjectToCollection(obj_collection, obj, sim_handle_single, 0)
        sim.addObjectToCollection(canonical_collection, obj, sim_handle_single, 0)
    end
end

function clean_collections()
    collections = {'canonical', 'textured'}
    for _, collection_name in pairs(collections) do
        obj_collection = sim.getCollectionHandle(collection_name)
        sim.emptyCollection(obj_collection)
        spawner = sim.getObjectHandle('zDummy')
        sim.addObjectToCollection(obj_collection, spawner, sim_handle_single, 0)
    end
end

function getObjectsHandleList(set_name)
    object_folder = sim.getObjectHandle(set_name)
    handle_list = {}
    i = 0
    while true do
        obj = sim.getObjectChild(object_folder  ,i)
        if obj == -1 then 
            break 
        end
        i = i+1
        table.insert(handle_list, obj)
    end 
    return handle_list
end

function init_scene()
    canonical_collection = sim.getCollectionHandle('canonical')
    obj_collection = sim.getCollectionHandle('textured')

    -- shift original floor underneath
    sq_floor_obj = sim.getObjectHandle('SquaredFloor')
    sim.setObjectPosition(sq_floor_obj, -1, {0,0,-0.003})

    -- add floor to collection
    floor_obj = sim.getObjectHandle('PlainFloor')
    sim.addObjectToCollection(canonical_collection, floor_obj, sim_handle_single, 0)

    -- add texture to floor
    table.insert(texturized_objects, sim.copyPasteObjects({floor_obj}, 0)[1])

    table_height = 0.65
    create_table(table_height)
    drop_objects(object_list, drop_height)
end