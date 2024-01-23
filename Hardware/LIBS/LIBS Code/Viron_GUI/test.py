input_string = "+0.001001000"

# Convert the string to a floating-point number
value = float(input_string)

# Define the unit dictionary
unit_dict = {
    's': 10**0,
    'ms': 10**-3,
    'us': 10**-6,
    'ns': 10**-9,
    'ps': 10**-12
}

# Determine the appropriate unit based on the magnitude of the value
magnitude = 0
for unit, exponent in unit_dict.items():
    if float(exponent) <= abs(value) < 1000:
        magnitude = exponent
        break

# Convert the value to the appropriate unit
scaled_value = value / magnitude

# Format the result as a string with three decimal places and append the unit
result = ['{:.3f}'.format(scaled_value), unit]

# Print the result
print(result)