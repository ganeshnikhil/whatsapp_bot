from datasets import Dataset
from transformers import MBartForConditionalGeneration, MBartTokenizer
from transformers import Trainer, TrainingArguments
import torch
import json

# Step 1: Load the cleaned data from the JSON file
with open('.Data/cleaned_data.json', 'r', encoding='utf-8') as f:
    cleaned_data = json.load(f)

# Step 2: Load the pre-trained mBART model and tokenizer
model_name = "facebook/mbart-large-cc25"
tokenizer = MBartTokenizer.from_pretrained(model_name, src_lang="en_XX", tgt_lang="hi_IN")
model = MBartForConditionalGeneration.from_pretrained(model_name)

# Step 3: Preprocessing function to tokenize the text
def preprocess_function(examples):
    inputs = tokenizer(examples["en"], padding="max_length", truncation=True, max_length=64)
    targets = tokenizer(examples["hi_ng"], padding="max_length", truncation=True, max_length=64)
    inputs["labels"] = targets["input_ids"]
    return inputs

# Step 4: Convert the data to a HuggingFace Dataset
dataset = Dataset.from_dict({
    'en': [entry['en'] for entry in cleaned_data],
    'hi_ng': [entry['hi_ng'] for entry in cleaned_data]
})

# Preprocess the dataset
train_dataset = dataset.map(preprocess_function, batched=True)

# Step 5: Define the training arguments
training_args = TrainingArguments(
    output_dir="./results",          
    num_train_epochs=1,              # Reduce for testing
    per_device_train_batch_size=1,   # Minimized batch size
    gradient_accumulation_steps=8,   # Accumulate gradients
    logging_dir="./logs",            
    logging_steps=10,                
    save_steps=5000,                 
    eval_steps=500,                  
    save_total_limit=2,
    fp16=False,   
)

# Step 6: Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    tokenizer=tokenizer,
)

# Step 7: Train the model
trainer.train()

# Step 8: Save the trained model
trainer.save_model("./mbart_hinglish")

# Step 9: Function to translate English to Hinglish
def translate_to_hinglish(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=64).to(model.device)
    translated = model.generate(inputs["input_ids"], num_beams=4, max_length=64, early_stopping=True)
    translation = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translation

# Example usage of the translation function
text = "What's the name of the movie?"
translation = translate_to_hinglish(text)
print(f"Translated text: {translation}")
