def reward_function(params):
    '''
    Example of rewarding the agent to stay inside two borders
    and penalizing getting too close to the objects in front
    '''
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    objects_distance = params['objects_distance']
    _, next_object_index = params['closest_objects']
    objects_left_of_center = params['objects_left_of_center']
    is_left_of_center = params['is_left_of_center']
    speed = params['speed']
    progress = params['progress']
    wheel_theta = abs(params['steering_angle'])
    

    # Initialize reward with a small number but not zero
    # because zero means off-track or crashed
    reward = 1e-3

    marker_1 = 0.1 * track_width
    marker_2 = 0.5 * track_width

    if distance_from_center <= marker_1:
        reward_lane = 1.0
    elif distance_from_center <= marker_2:
        reward_lane = 0.5
    else:
        reward_lane = 1e-3  # likely crashed/ close to off track

    # Penalize if the agent is too close to the next object, and if it is going too fast
    reward_avoid = 1.0 
    speed_on_avoid = 1.0

    # Distance to the next object
    distance_closest_object = objects_distance[next_object_index]
    # Decide if the agent and the next object is on the same lane
    is_same_lane = objects_left_of_center[next_object_index] == is_left_of_center
    
    if is_same_lane:
        if 0.5 <= distance_closest_object < 0.8: 
            reward_avoid *= 0.5
            speed_on_avoid /= speed
        elif 0.3 <= distance_closest_object < 0.5:
            reward_avoid *= 0.4
            speed_on_avoid /= speed
        elif distance_closest_object < 0.3:
            reward_avoid = 1e-3 # Likely crashed
    else:
        # give incentive for going faster when not close to an obstacle
        speed_on_avoid = speed
    

    steering_reward = 0.2 if wheel_theta>=15 else 1.0

    # calculate the weighted reward
    reward += 2.0 * reward_lane + 4.0 * reward_avoid + 1.0 * speed_on_avoid + 0.75 * progress + 1.0 * steering_reward

    return reward