import math


"""
Determine the total steel required for making diamond grill with 3" spacing
"""

def calculate_hypotenuse(l, h):
    """
    Find the longest diagonal line
    """
    res = math.sqrt((l**2) + (h**2))
    return res

# Window dimensions
original_h = 28
original_l = 78

h = original_h
l = original_l

spacing = 3
total_length = 0


while h > spacing:
    """
    Iteratively compute the new diagonal and add that to the sum
    """
    total_length += calculate_hypotenuse(l,h)

    # Reduce both height & length by 3"
    h -= spacing
    l -= spacing

# Multiply by 2 to get for the entire window
total_length *= 2

print(f"Length in inches: {(total_length*2)}")
print(f"Length in feet: {((total_length*2))/12}")
