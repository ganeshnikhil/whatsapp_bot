from webdev.django_first.chaiaurDjango.URL import url 
from requests import request

def remove_notificaton(receiptid:int) -> bool:

    payload = {}
    headers= {}
    delete_url = url+str(receiptid)
    response = request("DELETE", delete_url , headers=headers, data = payload)
    
    status_code = response.status_code
    if status_code == 200:
        if response["result"] == 'true':
            return True 
    print(response.text)
    return False 