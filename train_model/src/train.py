#!pip install transformers pandas datasets torch
import pandas as pd
from datasets import Dataset
from transformers import MBartTokenizer, MBartForConditionalGeneration
import json
from transformers import Trainer, TrainingArguments
import torch
# from transformers import cached_path
# import shutil
# shutil.rmtree(cached_path('facebook/mbart-large-cc25'))


# Step 1: Load the cleaned data from the CSV file
csv_file = 'movie_dialogues.csv'  # Path to your CSV file
df = pd.read_csv(csv_file, encoding='utf-8')

# Ensure that 'en' and 'hi_ng' columns are in string format (in case they are not)
df['en'] = df['en'].astype(str)
df['hi_ng'] = df['hi_ng'].astype(str)

# Step 2: Load the pre-trained mBART model and tokenizer
model_name = "facebook/mbart-large-cc25"
tokenizer = MBartTokenizer.from_pretrained(model_name, src_lang="en_XX", tgt_lang="hi_IN")
model = MBartForConditionalGeneration.from_pretrained(model_name)

# Step 3: Preprocessing function to tokenize the text
def preprocess_function(examples):
    # Ensure the inputs are in string format
    inputs = tokenizer(examples["en"], padding="max_length", truncation=True, max_length=64)
    targets = tokenizer(examples["hi_ng"], padding="max_length", truncation=True, max_length=64)
    inputs["labels"] = targets["input_ids"]
    return inputs

# Step 4: Convert the data to a HuggingFace Dataset
dataset = Dataset.from_pandas(df)  # Convert pandas DataFrame to HuggingFace Dataset

# Preprocess the dataset
train_dataset = dataset.map(preprocess_function, batched=True)

training_args = TrainingArguments(
    output_dir="./results",              # Directory to save results
    num_train_epochs=3,                  # Adjust for larger dataset size, can be higher
    per_device_train_batch_size=16,      # Reduced batch size to fit memory
    gradient_accumulation_steps=4,       # Accumulate gradients for effective larger batch size
    logging_dir="./logs",                # Directory to save logs
    logging_steps=10,                    # Log every 10 steps
    save_steps=2000,                     # Save model every 2000 steps to save space
    eval_steps=2000,                     # Evaluate every 2000 steps
    save_total_limit=3,                  # Keep up to 3 model checkpoints
    fp16=True,                           # Use mixed precision for faster training
    report_to="none",                    # Disable WandB logging (optional)
    max_grad_norm=1.0,                   # Gradient clipping to avoid exploding gradients
    per_device_eval_batch_size=16,       # Match the batch size during evaluation
    disable_tqdm=False,                  # Keep tqdm for progress bars
    dataloader_num_workers=2,            # Reduce data loading workers to save memory
    run_name="training_run",             # Optional: Name the run
    logging_first_step=True              # Log the first step
)




# Step 6: Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    tokenizer=tokenizer,
)

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
