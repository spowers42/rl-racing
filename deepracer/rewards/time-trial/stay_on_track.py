def reward_function(params):
    '''
    Simple baseline model that tries to stay on the track.  
    '''
    
    if params['progress'] == 100:
        # handle the end condition
        return float(10000)
    
    
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    
    # Give a very low reward by default
    reward = 1e-3

    # Give a high reward if no wheels go off the track and
    # the agent is somewhere in between the track borders
    if all_wheels_on_track and (0.5*track_width - distance_from_center) >= 0.05:
        reward = 1.0
        
    # Always return a float value
    return float(reward)