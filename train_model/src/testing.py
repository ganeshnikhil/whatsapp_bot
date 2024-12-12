import warnings
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Suppress specific warnings related to pad_token_id
warnings.filterwarnings("ignore", message="Setting pad_token_id to eos_token_id")

def load_model_and_tokenizer():
    model = GPT2LMHeadModel.from_pretrained("./fine_tuned_distilgpt2")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokenizer.pad_token = tokenizer.eos_token  # Set pad_token to eos_token
    return model, tokenizer

def generate_response(prompt, model, tokenizer, max_length=100, temperature=0.1):
    # Encode the input prompt
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True)

    # Ensure no padding token warnings
    attention_mask = inputs['attention_mask']

    # Generate a response with sampling and adjusted parameters
    outputs = model.generate(
        inputs['input_ids'], 
        attention_mask=attention_mask, 
        max_length=max_length, 
        num_return_sequences=1, 
        do_sample=True, 
        top_k=50, 
        top_p=0.95, 
        temperature=temperature,
        min_length=15  # Minimum length of the response to avoid short outputs
    )

    # Decode and return the generated text
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Post-processing: remove redundant parts like repeated prompt in response
    if response.lower().startswith(prompt.lower()):
        response = response[len(prompt):].strip()  # Remove the prompt part from the response

    return response

def main():
    # Load the fine-tuned model and tokenizer
    model, tokenizer = load_model_and_tokenizer()

    # Sample prompts (using more specific phrasing)
    prompts = [
        "shi",
    ]
    
    # Generate and print responses for each prompt
    for prompt in prompts:
        response = generate_response(prompt, model, tokenizer, temperature=1.2)
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
        print("-" * 50)

if __name__ == "__main__":
    main()
