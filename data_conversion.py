# Convert text to a string of 1s and 0s (bit string)
def text_to_bits(text):
    bits = ""

    for t in text:
        bits += format(ord(t), '07b')
    
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

        # Add the zeroes to either the front or the rear
        if end:
            bits = bits + "0"*(padding)
        else:
            bits = "0"*(padding) + bits
    
    return bits