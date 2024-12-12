import re


def contains_invisible_character(line):
    # Define the invisible character (U+200E)
    invisible_char = '\u200E'

    # Check if the invisible character exists in the string
    if invisible_char in line:
        return True
    return False

def remove_invisible_characters_from_line(line):
    # Define a pattern to match invisible characters (U+200E)
    invisible_char_pattern = r'[\u200E]'

    # Remove invisible characters from the line
    cleaned_line = re.sub(invisible_char_pattern, '', line)

    return cleaned_line


def clean_and_merge_messages_from_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    result = []
    last_sender = None
    combined_message = ""
    url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    for line in lines:
        # Extract sender and message using regex
        match = re.match(r"^\[(.*?)] (.*?): (.*)", line.strip())
        
        # If the line matches the expected pattern (Date, Sender, Message)
        if match:
            _ , sender, message = match.groups()
            message = message.replace(",","")
            if "<This message was edited>" in message:
                message = message.replace("<This message was edited>","")
                message = remove_invisible_characters_from_line(message)
        
            if contains_invisible_character(message) or re.search(url_pattern, message):
                continue 
            
            # If sender changes, save the current combined message
            if sender != last_sender:
                if last_sender is not None:
                    result.append({"sender": last_sender, "message": combined_message.strip()})
                last_sender = sender
                combined_message = message
            else:
                # Append to the current sender's message
                combined_message += " " + message
        else:
            # Handle any unexpected lines (e.g., non-message or malformed lines)
            continue

    # Append the last sender's message
    if last_sender is not None:
        result.append({"sender": last_sender, "message": combined_message.strip()})

    # Save the cleaned data into a CSV or JSON format
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("sender,message\n")  # Writing header
        for entry in result:
            file.write(f"{entry['sender']},{entry['message']}\n")

    print(f"Cleaned data saved to {output_file}")

# Example usage
input_file = "Data/chat.txt"  # Path to your raw text file
output_file = "raw.csv"  # Path where cleaned data will be saved
clean_and_merge_messages_from_text(input_file, output_file)
