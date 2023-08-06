from imports import *

async def SkelCoord():                          # return xyz coordinates of person1
    # Define the keypoints
    global person1, lwristperson, rwristperson
    
    keypoints = {
        0: 'nose',
        1: 'neck',
        2: 'right_shoulder',
        3: 'right_elbow',
        4: 'right_wrist',
        5: 'left_shoulder',
        6: 'left_elbow',
        7: 'left_wrist',
        8: 'right_hip',
        9: 'right_knee',
        10: 'right_ankle/foot',
        11: 'left_hip',
        12: 'left_knee',
        13: 'left_ankle/foot',
        14: 'right_eye',
        15: 'left_eye',
        16: 'right_ear',
        17: 'left_ear'
    }

    # Create ZED objects
    zed = sl.Camera()
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720
    init_params.depth_mode = sl.DEPTH_MODE.ULTRA
    init_params.sdk_verbose = True
    init_params.coordinate_units = sl.UNIT.MILLIMETER

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        # Quit if an error occurred
        exit()

    # Define the Object Detection module parameters
    obj_param = sl.ObjectDetectionParameters()
    # Different model can be chosen, optimizing the runtime or the accuracy
    obj_param.detection_model = sl.DETECTION_MODEL.HUMAN_BODY_FAST
    # run detection for every Camera grab
    obj_param.image_sync = True
    # Enable tracking to detect objects across time and space
    obj_param.enable_tracking = True
    # Optimize the person joints position, requires more computations
    obj_param.enable_body_fitting = True

    # If you want to have object tracking you need to enable positional tracking first
    if obj_param.enable_tracking:
        positional_tracking_param = sl.PositionalTrackingParameters()
        zed.enable_positional_tracking(positional_tracking_param)

    print("Object Detection: Loading Module...")
    err = zed.enable_object_detection(obj_param)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(err))
        zed.close()
        exit(1)

    # Set runtime parameter confidence to 40
    obj_runtime_param = sl.ObjectDetectionRuntimeParameters()
    obj_runtime_param.detection_confidence_threshold = 40

    objects = sl.Objects()
    j = 0
    # Grab new frames and detect objects
    while zed.grab() == sl.ERROR_CODE.SUCCESS:
        await asyncio.sleep(0.1)
        err = zed.retrieve_objects(objects, obj_runtime_param)
        if objects.is_new:
            # Count the number of objects detected
            obj_array = objects.object_list
            
            if len(obj_array) == 0:
                #print("No people detected")
                global p 
                p = 0

            else:
                for i in range(len(obj_array)):
                    p = 1
                    #print(f"Person {i+1} neck coordinates: ")
                    keypoint = obj_array[i].keypoint
                    neck_coordinates = keypoint[1]
                    rwrist_coordinates = keypoint[4]
                    lwrist_coordinates = keypoint[7]
                    bx = (rwrist_coordinates[0])/8
                    by = (rwrist_coordinates[1])/8
                    bz = rwrist_coordinates[2]
                    cx = (lwrist_coordinates[0])/8
                    cy = (lwrist_coordinates[1])/8
                    cz = lwrist_coordinates[2]
                    ax = (neck_coordinates[0])/8
                    ay = (neck_coordinates[1])/8
                    az = neck_coordinates[2]
                    person1 = [ax, ay,az]
                    rwristperson = [bx, by, bz]
                    lwristperson = [cx, cy, cz]
                    #print("hello")
                    # X is left right, y is up down (is POV is camera, right is negative), z is towards and away when facing

    # Disable object detection and close the camera
    zed.disable_object_detection()
    zed.close()

async def _send_cmd(ws, dstnode, msgtype, data):    # send cmd to vine
    await ws.send(json.dumps(dict(
        msgtype = msgtype,
        dstnode = dstnode,
        data = data,
    )))

async def inflate(ws, chamber, pressure):           # assign pressure to chamber
    # set chamber c to pressure (0-1)
    if not (0 <= pressure <= 1):
        raise ValueError("Pressure should be a value between 0 and 1")

    if not (0 <= chamber <= 2):
        raise ValueError("Chamber should be a value between 0 and 2")

    await _send_cmd(ws, chamber+2, "targetdrive", pressure*1.4-0.2)  # node numbers are offset from chamber numbers by 2

async def alight(ws, r,g,b):                        # set LEDs on
    # RGB colours range 0 ~ 255(0xff)
    await _send_cmd(ws, 0, "rgb", [int(g),int(r),int(b),0])
    await _send_cmd(ws, 0, "rgb", [int(g),int(r),int(b),1])

async def lights_travel(ws, r,g,b,addr):            # send propogating lights
    # set lights to travel from end to end - addr 0 top, addrs 1 bottom
    await _send_cmd(ws, 0, "rgb", [int(r), int(g), int(b), int(addr)])
    
async def recvpump(ws):
    """Empty the recv buffer, doing nothing with the messages."""
    while True: 

        print("clear")
        await ws.recv()


# STATE TRANSISIONING DECISIONS #######################################################################################################################

async def decision():                               # deciding what state to be in
    global person1, state, finalstate, i, p
    radius = 800        # radius within which reaction occurs
    state = []
    # state 1 : neutral - no one detected
    # state 2 : awake - person detected
    # state 3 : reactive - person within interaction bound

    while i < 10:
        await asyncio.sleep(0.5)
        #start = time.time()
        state.clear()   # clear transient state array
        robot_pos = [0, 1800]          # L/R, Front/Back
        readings = 0
        for readings in range(10):        # best of 10 readings

            x = person1[0]       # L/R range (), 0 in center, right is negative
            z = person1[2]       # Front/Back >= 0. depth

            distance = ((x - robot_pos[0])**2) + ((z - robot_pos[1])**2)

            if p == 0:                      # if no one detected
                state.append(1)
            elif p == 1:                    # if detected
                if distance < (radius**2):  # if in range
                    state.append(3)
                else:                       # if detected but not in range
                    state.append(2)
                    
        finalstate = stats.mode(state)
        print('final state is', finalstate)


async def acceleration():
    global person1, lwristperson, rwristperson
    global ac
    accelerations = []
    await asyncio.sleep(0.1)
    while True:
        print('es')
        acceleration.clear()
        starttime = time.time()
        for readings in range(10):
            xal = lwristperson[0]
            xar = rwristperson[0]
            zal = lwristperson[2]
            zar = rwristperson[2]
            ta = time.time()-starttime
            print(ta)
            xbl = lwristperson[0]
            xbr = rwristperson[0]
            zbl = lwristperson[2]
            zbr = rwristperson[2]
            tb = time.time()-starttime
            vlx = (xbl - xal) / (tb - ta)
            vrx = (xbr - xar) / (tb - ta)
            vlz = (zbl - zal) / (tb - ta)
            vrz = (zbr - zar) / (tb - ta)
            vl = np.sqrt(vlx**2 + vlz**2)
            vr = np.sqrt(vrx**2 + vrz**2)
            al = vl / (tb - ta)
            ar = vr / (tb - ta)
            accelerations.append(al)
            accelerations.append(ar)
            print('acceleration is ',accelerations)
            
            if np.mean(accelerations) > 5: #placeholder acceleration, subject to change
                
                ac = 1
                print('Movement', ac)
            else:
            
                ac =0
                print('No movement', ac)
          

# VINE BASE BEHAVIOURS ###################################################################################################

async def reset(ws):                                # all chambers to 1
    print("reset")
    for c in range(0,3):
        await inflate(ws, c, 1)

async def simul_inflate(ws, p0, p1, p2):            # simultaneously inflate all chambers to desired pressure
    
    c0 = asyncio.create_task(inflate(ws, 0, p0))
    c1 = asyncio.create_task(inflate(ws, 1, p1))
    c2 = asyncio.create_task(inflate(ws, 2, p2))
    await c0
    await c1
    await c2

async def bounce(ws):                               # NEW and IMPROVED bounce TM - simultaneous action

        #print('bouncin')
        high = 1
        low = 0.3
        t = time.time()
        R = (255*(math.sin(t/2))+255)/2
        G = (255*(math.sin(t))+255)/2
        B = (255*(math.sin(t/3))+255)/2
        await alight(ws,R,G,B)
        await simul_inflate(ws,high,high,high)
        await asyncio.sleep(1)
        await simul_inflate(ws,low,low,low)
        await asyncio.sleep(1)

# VINE ADVANCED BEHAVIOURS #############################################

async def death(ws):                                # dramatic death
    print('dead, slain, ended before his time. too young, too soon')

    await alight(ws,255,0,0)                       # wound
    await simul_inflate(ws, 0, 0, 0)                # kill
    await asyncio.sleep(0.2)
    await alight(ws,0,0,0)                          # lights out

async def sleeby(ws):                               # sinusoidal sleeby  
    print('sleebing')
    breath_time = random.uniform(8,12)      # total
    hold_time = random.uniform(2,4)         # peak 
    pauses = [1.0, 1.0, 1.1, 1.1, 1.2, 1.2, 2.0, 3.0]  
    pause_time = random.choice(pauses)      # between breaths
    max_vol = 1.0
    min_vol = 0.6
    max_light = 200
    min_light = 50
    r = 0.2                                 # refresh rate
    
    async def inhale():
        t = 0.0
        lim = breath_time/2
        while t <= lim:
            phase = math.sin(t*math.pi/breath_time)**2
            cp = phase*(max_vol - min_vol) + min_vol
            await simul_inflate(ws, cp, cp, cp)
            await alight(ws,phase*(max_light-min_light) + min_light,0,0)
            t = t + r
            await asyncio.sleep(r)        
        
    async def exhale():
        t = 0.0
        lim = breath_time/2
        while t <= lim:
            phase = math.cos(t*math.pi/breath_time)**2
            cp = phase*(max_vol - min_vol) + min_vol
            await simul_inflate(ws, cp, cp, cp)
            await alight(ws,phase*(max_light-min_light) + min_light,0,0)
            t = t + r
            await asyncio.sleep(r)    
        
    await inhale()
    await asyncio.sleep(hold_time)
    await exhale()
    await asyncio.sleep(pause_time)

async def dream(ws):                                # to dream or not to dream
    
    dur = [0.7,0.9,1.0,1.0,1.2,1.5,3.0]             # possible dream durations
    duration = random.choice(dur)
    dream_chance = 0.2                              # chance of dream
    not_dream = 1 - dream_chance
    dreaming = random.choices([0,1], weights=[not_dream,dream_chance])

    async def electric_sheep(ws):                   # dream contents: colors and twitches
        
        low = 50            # lights
        high = 150          # lights
        shimmer_rate = random.uniform(0.1,0.5)
        twitch_active = random.choice([0,1])
        
        async def shimmer(ws):
            while i < 10:
                R = random.randint(low, high)
                G = random.randint(low, high)
                B = random.randint(low, high)
                await alight(ws, R, G, B)
                await asyncio.sleep(shimmer_rate)
            
        async def twitch(ws):

            if twitch_active == 1:
                twitch_wait = random.uniform(0,duration)
                await asyncio.sleep(twitch_wait)

                chambs = [0,1,2]
                c = random.choice(chambs)
                twitch_pressure = random.uniform(0.7,1)
                await inflate(ws, c, twitch_pressure)
            else:
                pass

        dream_on = [                    # sing with me! sing for the years
        asyncio.ensure_future(shimmer()),
        asyncio.ensure_future(twitch())
        ] 
        await asyncio.wait(dream_on)
        
    if dreaming == 1:
        await electric_sheep()
    
    else:
        pass

async def awake(ws):                                # neutral alert state

    high = 1.0                  # max pressure             
    low = 0.8                   # min pressure              
    p = [0, 0, 0, 0, 0, 0.1, 0.3, 0.7, 1.0, 1.5]         
    pause = random.choice(p)    # random pause              
    pulserate = random.uniform(0.8,1.2) # light pulse       
       
    async def sway():               # random sway motion
        while True:
            chamber = [0,1,2]
            c = random.choice(chamber)
            pressure = random.uniform(low,high)
            await inflate(ws,c,pressure)
            await asyncio.sleep(pause)
    
    async def pulse():              # light pulses along 
        while True:
            await lights_travel(ws, 0, 0, 0xff, 0)
            await asyncio.sleep(pulserate)

    await asyncio.gather(sway(), pulse())


async def random_light(ws):
    lights= random.uniform(0,255)
    await alight(ws, lights,lights,lights)
    return

async def simulate_signal():
    global finalstate
    while True:
        finalstate = random.uniform(0,20)
        print(finalstate)
        await asyncio.sleep(1)

async def loop_break(func,ws,state):
    global finalstate
    while True:
        await func(ws)
        await asyncio.sleep(1)
        if finalstate != state:
            return
    
    

# VINE STATES #################################################################################################

async def DORMANT(ws):
    await reset(ws)
    global finalstate
    print('state 1: dormant - no person detected')
    state = finalstate
    await random_light(ws)
    return
 

async def ALERT(ws):
    global finalstate
    print('state 2: alert - person detected')
    state = finalstate
    await random_light(ws)
    return

async def ACTIVE(ws):
    global finalstate
    print('state 3: active - person in interaction range')
    state = finalstate
    await random_light(ws)
    return 
    
    
async def Decision(ws):
    global finalstate 
    while True:
        await asyncio.sleep(0.3)
        print("something error")
        if finalstate<6:
            print('state 1: dormant - no person detected')

            await reset(ws)
        elif finalstate<15:
            print('state 2: alert - person detected')

            await bounce(ws)
        elif finalstate<20:
            print('state 3: active - person in interaction range')

            await reset(ws)
        else:
            print("working")
        
    
        




           
