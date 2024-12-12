from webdev.django_first.chaiaurDjango.URL import url 
from requests import post

def post_msg(Phone_id:str , msg:str) -> bool:
    payload = {
    "chatId": f"{Phone_id}@c.us", 
    "message": msg
    }
    headers = {
    'Content-Type': 'application/json'
    }

    response = post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return True 
    
    print(response.text)
    return False