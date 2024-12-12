from webdev.django_first.chaiaurDjango.URL import url 
from requests import request 

def get_notification()-> int | None :
    payload = {}
    headers= {}

    response = request("GET", url, headers=headers, data = payload)
    
    status_code = response.status_code 
    if status_code == 200:
        details = response.json()
        # get the necessary from the json 
        receiptid = details["receiptId"]
        textmsg = details["textMessageData"]["textMessage"]
        chatid = details["senderData"]["chatId"]
        sendername = details["senderData"]["senderContactName"]
        return {"senderContactName":sendername , "chatId":chatid , "receiptId":receiptid ,"textMessage":textmsg}
    print(response.text)
    return None 



