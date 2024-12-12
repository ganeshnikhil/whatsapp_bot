import pandas as pd
import json

def load_eng_hing():
    # Load the dataset (replace with your dataset path)
    df = pd.read_json("hf://datasets/findnitai/english-to-hinglish/hinglish_upload_v1.json", lines=True)

    df_cleaned = pd.json_normalize(df['translation'])
    # Remove the 'source' column
    df_cleaned = df_cleaned.drop(columns=['source'])

    data = df_cleaned.to_dict(orient='records')

    with open("./Data/output_english_to_hinglish.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Data saved to output_english_to_hinglish.json")
