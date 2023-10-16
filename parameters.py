infeed_speed = 36000       # Eggs/hour that enter machine
carrier_speed = 48000      # Eggs/hour for carrier that moves above the receivers

egg_weight_mean = 50       # Mean of normal egg weight distribution
egg_weight_std_dev = 9     # Standard diviation of normal egg weight distribution

egg_S_upper_limit = 53    
egg_L_upper_limit = 63

egg_sample_size = 10000     # Number of eggs for simulation

number_of_S_packers = 1    # Number of droplets for small eggs
number_of_M_packers = 1    # Number of droplets for medium eggs
number_of_L_packers = 1    # Number of droplets for large eggs


ROW_WISE = 1
CROSSED_ROW_WISE = 2

receiver_filling_mode = CROSSED_ROW_WISE