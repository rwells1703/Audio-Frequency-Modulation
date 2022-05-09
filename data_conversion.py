import struct

# Convert text to a string of 1s and 0s (bit string)
def text_to_binary_string(text):
    binary_string = ""

    for t in text:
        binary_string += format(ord(t), '07b')
    
    #print([binary_string[i:i+7] for i in range(0, len(binary_string), 7)])
    return binary_string

# Converts a string of bits to an array of integers representing them
def bits_to_integers(bits, segment_bits):
    start = 0
    end = segment_bits
    
    # Zero pad the data to a size that is a multiple of the segment bits
    leftover_bits = len(bits) % segment_bits

    # If there are leftover bits, pad the end
    if leftover_bits != 0:
        padding = segment_bits - leftover_bits
        bits += "0"*(padding)

    integers = []

    # Loop through the bits and convert sections to an integer
    while end <= len(bits):
        bit_segment = bits[start:end]
        integers.append(int(bit_segment, 2))
        
        start += segment_bits
        end += segment_bits

    return integers

# Convert a bytestring of wav audio data to a list of integer values
def raw_data_to_int(data):
    int_tuples = struct.iter_unpack("H", data)
    int_data = list(map(lambda t : t[0], int_tuples))

    return int_data