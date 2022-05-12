# Check to see if a detected value has been detected a several times recently
# if it is recurring, store it as it is probably being deliberately sent
def check_sent_deliberately(int_value, int_stream_raw, certainty, certainy_sample_size):
    # Calculate the total proportion of recently received values (within a given sample size)
    # that are equal to the target value
    target_value_count = int_stream_raw[-certainy_sample_size:].count(int_value)

    # If the amount of values equal to the target value is above a threshold "certainty", the value was sent deliberately so store it
    if target_value_count >= certainty:
        return True
    
    # The value was probably a result of random noise
    return False

# Only store values that are not identical to the value directly preceding them
# This should never occur as after each value is sent, a "gap" value is also sent
def check_not_added(int_value, int_stream):
    if len(int_stream) == 0:
        # If there are no values stored
        return True
    elif int_stream[-1] != int_value:
        # If the previous value has not already been stored
        return True

    # The value is already stored
    return False