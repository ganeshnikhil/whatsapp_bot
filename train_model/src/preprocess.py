import re 
import json 
import pandas as pd
def clean_text(text):
    # Remove URLs
    text = re.sub(r'http[s]?://\S+', '', text)  # Remove URLs (both http and https)
    text = text.replace(".","")
    # Remove extra spaces (leading, trailing, and multiple spaces)
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove unwanted symbols like ?, ,, -, etc.
    text = re.sub(r'[?,-]', '', text)  # Remove ?, commas, and dashes
    
    # remove non assci characters 
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    # Remove escaped quotes (\")
    text = text.replace(r'\\"', '')  # Removes the escaped quotes
    return text


# Load the JSON data
with open('./Data/output_english_to_hinglish.json', 'r') as file:
    data = json.load(file)
    

for entry in data:
    entry['en'] = clean_text(entry['en'])
    entry['hi_ng'] = clean_text(entry['hi_ng'])
    

with open('./Data/cleaned_data.json', 'w') as file:
    json.dump(data, file, indent=4)
    

import json 
with open('/Data/cleaned_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Save to CSV
csv_file = "./Data/movie_dialogues.csv"
df.to_csv(csv_file, index=False, encoding='utf-8')

print(f"Data saved to {csv_file}")