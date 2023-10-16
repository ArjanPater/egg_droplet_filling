import numpy as np
import matplotlib.pyplot as plt

# Set the mean and standard deviation of the normal distribution
weight_mean = 50  # Mean of the distribution
weight_std_dev = 9  # Standard deviation of the distribution
num_samples = 30  # Number of samples to generate

# Generate random samples from the normal distribution
egg_weights_samples = np.random.normal(weight_mean, weight_std_dev, num_samples)

s_limit = 53
l_limit = 63

test_eggs = []

for i in range(len(egg_weights_samples)):
    if egg_weights_samples[i] < 53:
        test_eggs.append('S')
    elif egg_weights_samples[i] < 63:
        test_eggs.append('M')
    else:
        test_eggs.append('L')

#print(egg_weights_samples)
#print(test_eggs)

carrier_length = 10
carrier_1  = [0 for _ in range(carrier_length)]

receiver_1 = [0 for _ in range(6)]

missed_eggs = 0



def fill_receiver(receiver_class, receiver_start_index, receiver):
    for i in range(0, 6):
        if receiver[i] == 0 and receiver_class == carrier_1[receiver_start_index + i]:
            receiver[i] = carrier_1[receiver_start_index + i]
            carrier_1[receiver_start_index + i] = 0
        elif receiver[i] == 'X':
            receiver[i] = 0


    # Check if receiver is full
    if receiver.count(receiver_class) == 6:
        for i in range(0, 6):
            receiver_1[i] = 'X'

        



for i in range(100):
    # Insert egg onto supply line, if 
    if carrier_1[-1] != 0:
        missed_eggs = missed_eggs + 1
    try:
        carrier_1.insert(0, test_eggs[i])
    except:
        carrier_1.insert(0, 0)

    carrier_1.pop()

    fill_receiver('S', 0, receiver_1)

    print(f'Carrier 1: {carrier_1}')
    print(f'Receiver 1: {receiver_1}')
    print(f'missed eggs: {missed_eggs}')
    input()


