# Convert text to a string of 1s and 0s (bit string)
def text_to_binary_string(text):
    binary_string = ""

    for t in text:
        binary_string += format(ord(t), '07b')
        
    return bit_string
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