import constants

# Convert text to a string of 1s and 0s (bit string)
def text_to_bits(text):
    bits = ""

    for t in text:
        bits += format(ord(t), '07b')
    
    #print([bits[i:i+7] for i in range(0, len(bits), 7)])
    return bits


# Convert string of binary back to ascii
def bits_to_text(bits):
    text = ""
    start = 0
    end = 7

    # Loop through the bits and convert sections to ascii value
    while end <= len(bits):
        bits_segment = bits[start:end]
        text += chr(int(bits_segment, 2))
        
        start += 7
        end += 7
    
    return text

# Zero pad the data to a size that is a multiple of the modulus
def pad_bits(bits, modulus, end=True):
    leftover_bits = len(bits) % modulus

    # If there are leftover bits, pad the end
    if leftover_bits != 0:
        padding = modulus - leftover_bits
        if end:
            bits = bits + "0"*(padding)
        else:
            bits = "0"*(padding) + bits
    
    return bits

# Converts a string of bits to an array of integers representing them
def bits_to_ints(bits):
    start = 0
    end = constants.MFSK_SEGMENT_BITS
    
    bits = pad_bits(bits, constants.MFSK_SEGMENT_BITS)

    integers = []

    # Loop through the bits and convert sections to an integer
    while end <= len(bits):
        bits_segment = bits[start:end]
        integers.append(int(bits_segment, 2))
        
        start += constants.MFSK_SEGMENT_BITS
        end += constants.MFSK_SEGMENT_BITS

    return integers

# Convert integers to a string of bits
def ints_to_bits(int_stream):
    bits = ""

    for i in int_stream:
        bits += bin(i)[2:].zfill(constants.MFSK_SEGMENT_BITS)
    
    return bits

# Interlace zeros between the integer values to symbolise the end of each symbol
def add_ints_gaps(int_stream):
    output = []

    for i in int_stream:
        output.append(i)
        output.append(0)

    return output

# Remove interlaced zeros between the integer values to symbolise the end of each symbol
def remove_ints_gaps(int_stream):
    output = []

    for i in int_stream:
        if i != 0:
            output.append(i)

    return output