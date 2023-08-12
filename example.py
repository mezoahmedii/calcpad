def swap_substrings(string, substring1, substring2):
    # Find the indices of the substrings
    index1 = string.find(substring1)
    index2 = string.find(substring2)

    # Check if the substrings are found in the string
    if index1 == -1 or index2 == -1:
        return string  # Substrings not found, return the original string

    # Swap the substrings
    swapped_string = string[:index1] + substring2 + string[index1 + len(substring1):index2] + substring1 + string[index2 + len(substring2):]

    return swapped_string

# Example usage
original_string = "Hello world, how are you? The are is messed up, but world are still perfect!"
substring1 = "world"
substring2 = "are"
swapped_string = swap_substrings(original_string, substring1, substring2)
print(swapped_string)