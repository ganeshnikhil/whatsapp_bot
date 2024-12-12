import re

def remove_invisible_characters_from_line(line):
    # Define a pattern to match invisible characters (U+200E)
    invisible_char_pattern = r'[\u200E]'

    # Remove invisible characters from the line
    cleaned_line = re.sub(invisible_char_pattern, '', line)

    return cleaned_line

def contains_invisible_character(line):
    # Define the invisible character (U+200E)
    invisible_char = '\u200E'

    # Check if the invisible character exists in the string
    if invisible_char in line:
        return True
    return False

# Example usage
line = "‎[31/10/24, 11:05:40 AM] Ganesh Nikhil: ‎GIF omitted"
if contains_invisible_character(line):
    print("Invisible character found!")
else:
    print("Invisible character not found.")

# Example usage
line = "‎[31/10/24, 11:05:40 AM] Ganesh Nikhil: ‎GIF omitted"
cleaned_line = remove_invisible_characters_from_line(line)

print(cleaned_line)  # Output: "Hello World!"
#31/10/24, 11:05:40 AM] Ganesh Nikhil: GIF omitted