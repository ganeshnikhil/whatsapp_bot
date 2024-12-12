from src.lm_ai import client


def send_to_ai(content ,  max_token = 2000 , model="Lewdiculous/Eris_PrimeV4-Vision-32k-7B-GGUF-IQ-Imatrix"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages = content ,
            temperature=0.7,
            max_tokens=max_token,
            top_p=1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"