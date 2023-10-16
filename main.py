import numpy as np
import matplotlib.pyplot as plt
import parameters

# Generate random samples from the normal distribution
egg_weights_samples = np.random.normal(parameters.egg_weight_mean, parameters.egg_weight_std_dev, parameters.egg_sample_size)

# Subdived eggs into classes based on weight
test_eggs = []

for i in range(len(egg_weights_samples)):
    if egg_weights_samples[i] < parameters.egg_S_upper_limit:
        test_eggs.append('S')
    elif egg_weights_samples[i] < parameters.egg_L_upper_limit:
        test_eggs.append('M')
    else:
        test_eggs.append('L')


# This list will contain the eggs in the order of entering the machine
egg_supply = []

carrier_occupation_ratio = parameters.infeed_speed / parameters.carrier_speed

# Generate random samples from the uniform distribution, determines if eggholder is occupied
samples = np.random.uniform(0, 1,  parameters.egg_sample_size*100)

last_test_egg_index = -1
for i in range(len(samples)):
    if samples[i] > carrier_occupation_ratio:
        egg_supply.append(0)
    else:
        egg_supply.append(test_eggs[last_test_egg_index + 1])
        last_test_egg_index = last_test_egg_index + 1
        if last_test_egg_index == parameters.egg_sample_size - 1:
            break

# Divide total egg stream over 2 carriers
egg_supply_1 = []
egg_supply_2 = []

samples = np.random.uniform(0, 1,  len(egg_supply))

for i in range(0, len(samples)):
    if samples[i] > 0.5:
        egg_supply_1.append(egg_supply[i])
    else:
        egg_supply_2.append(egg_supply[i])


# Create 2 carriers, initialize as being empty
carrier_length = (parameters.number_of_S_packers +  parameters.number_of_M_packers +  parameters.number_of_L_packers) * 8

carrier_1 = [0 for _ in range(carrier_length)]
carrier_2 = [0 for _ in range(carrier_length)]

# Create receivers, assumed order S1, S2, ... M1, M2, ... L1, L2, ....
number_of_receivers = parameters.number_of_S_packers +  parameters.number_of_M_packers +  parameters.number_of_L_packers
receivers_1 = [[0 for _ in range(6)] for _ in range(number_of_receivers)]
receivers_2 = [[0 for _ in range(6)] for _ in range(number_of_receivers)] 

receiver_start_indices = []
receiver_classes = []

start_index = 0
for i in range(0, parameters.number_of_S_packers):
    receiver_start_indices.append(start_index)
    receiver_classes.append('S')
    start_index = start_index + 8

for i in range(0, parameters.number_of_M_packers): 
    receiver_start_indices.append(start_index)
    receiver_classes.append('M')
    start_index = start_index + 8

for i in range(0, parameters.number_of_L_packers): 
    receiver_start_indices.append(start_index)
    receiver_classes.append('L')
    start_index = start_index + 8

def fill_receiver_1_row_wise(receiver_class, receiver_start_index, receiver):
    for i in range(0, 6):
        if receiver[i] == 0 and receiver_class == carrier_1[receiver_start_index + i]:
            receiver[i] = carrier_1[receiver_start_index + i]
            carrier_1[receiver_start_index + i] = 0
        elif receiver[i] == 'X':
            receiver[i] = 0
    
    return receiver

def fill_receiver_2_row_wise(receiver_class, receiver_start_index, receiver):
    for i in range(0, 6):
        if receiver[i] == 0 and receiver_class == carrier_2[receiver_start_index + i]:
            receiver[i] = carrier_2[receiver_start_index + i]
            carrier_2[receiver_start_index + i] = 0
        elif receiver[i] == 'X':
            receiver[i] = 0
    
    return receiver

def fill_receiver_crossed_row_wise(receiver_class, receiver_start_index, receiver_1, receiver_2):
    for i in range(0, 6):
        if receiver_1[i] == 0 and receiver_class == carrier_1[receiver_start_index + i] and receiver_2[i] == 0:
            receiver_1[i] = carrier_1[receiver_start_index + i]
            carrier_1[receiver_start_index + i] = 0
        elif receiver_2[i] == 0 and receiver_class == carrier_2[receiver_start_index + i] and receiver_1[i] == 0:
            receiver_2[i] = carrier_2[receiver_start_index + i]
            carrier_2[receiver_start_index + i] = 0
        if receiver_1[i] == 'X':
            receiver_1[i] = 0
        if receiver_2[i] == 'X':
            receiver_2[i] = 0
    
    return receiver_1, receiver_2

# For simulation extend egg supply input to equal lenght
desired_input_lenght = max(len(egg_supply_1), len(egg_supply_2)) + carrier_length 

egg_supply_1.extend([0]*(desired_input_lenght-len(egg_supply_1)))
egg_supply_2.extend([0]*(desired_input_lenght-len(egg_supply_2)))

missed_eggs = []

# Move eggs through machine
for i in range(len(egg_supply_1)):
    # Insert eggs onto supply line, if last index in not empty increase missed egg counter
    if carrier_1[-1] != 0:
        missed_eggs.append(carrier_1[-1])
   
    carrier_1.insert(0, egg_supply_1[i]) 
    carrier_1.pop()
   
    if carrier_2[-1] != 0:
        missed_eggs.append(carrier_2[-1])
   
    carrier_2.insert(0, egg_supply_2[i]) 
    carrier_2.pop()  

    print(f'Carrier 1 before receiving: {carrier_1}')
    print(f'Carrier 2 before receiving: {carrier_2}')

    # Update all receivers
    for i in range(0, number_of_receivers):
        if parameters.receiver_filling_mode == parameters.ROW_WISE:
            receivers_1[i][:] = fill_receiver_1_row_wise(receiver_classes[i], receiver_start_indices[i], receivers_1[i][:])
            receivers_2[i][:] = fill_receiver_2_row_wise(receiver_classes[i], receiver_start_indices[i], receivers_2[i][:])
        else:
            receivers_1[i][:], receivers_2[i][:] = fill_receiver_crossed_row_wise(receiver_classes[i], receiver_start_indices[i], receivers_1[i][:], receivers_2[i][:])

        print(f'Class: {receiver_classes[i]}, Receiver 1: {receivers_1[i][:]}')
        print(f'Class: {receiver_classes[i]}, Receiver 2: {receivers_2[i][:]}')
        
    print(f'Carrier 1 after receiving: {carrier_1}')
    print(f'Carrier 2 after receiving: {carrier_2}')

    # Empty receivers if possible
    for i in range(0, number_of_receivers):
        if parameters.receiver_filling_mode == parameters.ROW_WISE:
            if receivers_1[i][:].count(receiver_classes[i]) == 6:
                        for j in range(0, 6):
                            receivers_1[i][j] = 'X'
            elif receivers_2[i][:].count(receiver_classes[i]) == 6:
                        for j in range(0, 6):
                            receivers_2[i][j] = 'X'
        else:
            egg_count = 0
            for k in range(0, 6):    
                if receivers_1[i][k] == receiver_classes[i] or receivers_2[i][k] == receiver_classes[i]:
                    egg_count = egg_count + 1
            if egg_count == 6:
                for j in range(0, 6):
                    receivers_1[i][j] = 'X'
                    receivers_2[i][j] = 'X'
















   
   # input()


# Create a frequency count of each size
counts = {'S': 0, 'M': 0, 'L': 0}
for egg in missed_eggs:
    counts[egg] += 1

# Plotting the histogram
plt.bar(counts.keys(), counts.values(), color=['blue', 'green', 'red'])
plt.xlabel('Size')
plt.ylabel('Frequency')
plt.title(f'Histogram of missed eggs ({(100*len(missed_eggs)/parameters.egg_sample_size)} %)')
plt.show()










