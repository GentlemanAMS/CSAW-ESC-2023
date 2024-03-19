

filename = 'hello_relay_data.txt'
f = open(filename, 'r')

lines = f.readlines()

time = []
bits = []

for each_line in lines:
    line = each_line.split(',')
    time.append(int(line[0]))
    bits.append(int(line[1]))

def find_smallest_toggle_distances(arr):
    ones_to_zeros = []  # Stores indices of 1 to 0 transitions
    zeros_to_ones = []  # Stores indices of 0 to 1 transitions
    
    # Iterate through the array and record transition indices
    for i in range(1, len(arr)):
        if arr[i - 1] == 1 and arr[i] == 0:
            ones_to_zeros.append(i - 1)
        elif arr[i - 1] == 0 and arr[i] == 1:
            zeros_to_ones.append(i - 1)
    
    # Initialize minimum distances with a large value
    min_distance_1_to_0 = float('inf')
    min_distance_0_to_1 = float('inf')
    
    # Calculate the smallest distances
    for i in ones_to_zeros:
        for j in zeros_to_ones:
            distance = abs(j - i)
            min_distance_1_to_0 = min(min_distance_1_to_0, distance)
    
    for i in zeros_to_ones:
        for j in ones_to_zeros:
            distance = abs(j - i)
            min_distance_0_to_1 = min(min_distance_0_to_1, distance)
    
    return min(min_distance_1_to_0, min_distance_0_to_1)


smallest_time = find_smallest_toggle_distances(bits)
print(smallest_time)

index = bits.index(1)
bits = bits[index:]



def combine_values(arr, smallest_unit_time, tolerance=0.1):
    combined_values = []
    
    # Find the index of the first occurrence of 1
    start_index = arr.index(1)
    
    # Iterate through the array from the first 1 onward
    i = start_index
    
    while i < len(arr):
        segment = arr[i:i + smallest_unit_time]

        # Count the number of 1s and 0s in the segment
        count_1s = segment.count(1)
        count_0s = smallest_unit_time - count_1s

        # Determine whether to consider the value as 0 or 1
        tolerance_limit = smallest_unit_time * tolerance
        if count_1s >= count_0s - tolerance_limit:
            combined_values.append(1)
        else:
            combined_values.append(0)
        
        # Move the index to the next segment
        i += smallest_unit_time

    return combined_values

combined_bits = combine_values(bits, smallest_time)
print(combined_bits)