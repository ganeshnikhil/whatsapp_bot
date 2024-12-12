
from src.delete_notification import remove_notificaton
from src.read_notificaton import get_notification 
from src.send_msg import post_msg 
from src.chat import send_to_ai 



def main():
    all_chats = {}
    response = get_notification()
    if response:
        name = response["senderContactName"]
        chatid = response["chatId"]
        receiptid = response["receiptId"]
        msg = response["textMessage"]
        
        if chatid not in all_chats:
            all_chats[chatid] = [{"role": "system", "content": "You are a helpful, informative assistant. Provide clear, concise answers to questions while maintaining a friendly and professional tone."}]
            all_chats[chatid].append({"role": "user", "content": msg})
        else:
            all_chats[chatid].append({"role": "user", "content": msg})
        
        
        # Send the chat history to the AI model and get the response
        try:
            ai_response = send_to_ai(all_chats[chatid])
            # Store AI's response in the chat history
            all_chats[chatid].append({"role": "assistant", "content": ai_response})

            # Clean up the processed notification
            remove_notificaton(receiptid)

            # Send the AI-generated response back to the user
            post_msg(chatid, ai_response)
        except Exception as e:
            print(f"An error occurred: {e}")
            # Optionally, send an error message to the user if needed
            post_msg(chatid, "Sorry, there was an issue processing your request.")
