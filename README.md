# whatsapp_bot

# WhatsApp Chatbot Notification Handler

## Overview
This project implements a notification handler for a WhatsApp chatbot. It processes incoming messages, interacts with an AI model, and sends back appropriate responses. The key functionality includes receiving notifications, managing chat histories, sending messages, and handling errors gracefully.

---

## Project Structure

```
project-root/
  ├── src/
  │   ├── delete_notification.py   # Handles notification deletion
  │   ├── read_notification.py     # Reads incoming notifications
  │   ├── send_msg.py              # Sends messages back to users
  │   ├── chat.py                  # AI interaction logic
  ├── train_model/
  │   ├── train.py                 # English-to-Hinglish translation training
  |   |-- preprocess.py            # for cleaning the data
  |   |-- load_data.py
  ├── main.py                     # Main entry point
  └── README.txt                  # Project documentation
```

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/ganeshnikhil/whatsapp-chatbot.git
   cd whatsapp-chatbot
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

---

## How It Works

1. **Receiving Notifications:**
   - `get_notification()` reads incoming messages.

2. **Managing Chat History:**
   - A dictionary `all_chats` stores messages using `chatId` as the key.

3. **Interacting with AI:**
   - `send_to_ai()` sends chat history to the AI model and retrieves a response.

4. **Sending Responses:**
   - `post_msg()` sends AI-generated responses back to the user.

5. **Notification Cleanup:**
   - `remove_notification()` deletes processed notifications to avoid duplication.

---

## Main Functionality

```python
# Main function
if __name__ == "__main__":
    main()
```

### Detailed Workflow

1. **Read Notification:**
   ```python
   response = get_notification()
   ```

2. **Extract Message Details:**
   ```python
   name = response["senderContactName"]
   chatid = response["chatId"]
   receiptid = response["receiptId"]
   msg = response["textMessage"]
   ```

3. **Manage Chat History:**
   ```python
   if chatid not in all_chats:
       all_chats[chatid] = [
           {"role": "system", "content": "You are a helpful assistant..."}
       ]
   all_chats[chatid].append({"role": "user", "content": msg})
   ```

4. **Send to AI & Respond:**
   ```python
   ai_response = send_to_ai(all_chats[chatid])
   all_chats[chatid].append({"role": "assistant", "content": ai_response})
   post_msg(chatid, ai_response)
   remove_notification(receiptid)
   ```

---

## Error Handling
- If an error occurs during AI interaction or message sending, the system logs an appropriate message and sends a default response:

```python
except Exception as e:
    print(f"An error occurred: {e}")
    post_msg(chatid, "Sorry, there was an issue processing your request.")
```

---

### Future Improvements

API Information

For API keys, usage instructions, and further details about working with APIs, [greenapi](https://green-api.com/docs/sdk/) visit Green API Documentation.

Add persistent chat storage (e.g., a database).

Enhance AI response generation.

Improve error logging and monitoring.



---

## English-to-Hinglish Training Process

### Overview
The `train_model/train.py` script focuses on training a model for English-to-Hinglish translation using the mBART model. The process includes data preprocessing, model training, and saving the trained model for integration into the WhatsApp bot.

### Current Status
The training script is still under development. Interested developers can explore the training process, enhance the translation model, and integrate it into `main.py`.

---

## License
This project is licensed under the MIT License. See `LICENSE` for more details.

---

## Author
**Ganesh nikhil**  
GitHub: [ganeshnikhil](https://github.com/ganeshnikhil)  
Email: ganeshnikhil124@gmail.com

