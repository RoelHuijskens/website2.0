from azure.communication.email import EmailClient
from azure.identity import DefaultAzureCredential
import os 


class NotificationsInterface(object):
    
    def __init__(self, endpoint: str, notification_email: str, sender_adress:str):
        endpoint = endpoint
        self.client = EmailClient(endpoint, DefaultAzureCredential())

        self.message_base = {
            "senderAddress": sender_adress,
            "recipients":  {
                "to": [{"address": notification_email }],
            },
        }
        
        
    def _get_base_message_template(self) -> dict:
        return self.message_base.copy()
    
    
    def send_error_notification(self, error_text: str):
        error_postifx = f"""
            
            ====================================================
            
            For more detailed information about this error see:
            
            https://roelhuijskens.scm.azurewebsites.net/api/logs/docker/zip
            
            
        """
        
        message={
                "subject": "[ERROR] Personal Website Notification",
                "plainText": error_text + error_postifx,
            }
        
        self._send_message(message)
        
    
    def send_update_notification(self, message_text: str): 
        message={
                "subject": "Personal Website Notification",
                "plainText": message_text,
            }
        self._send_message(message)
        
    
    def _send_message(self, message: dict):
        base_message = self._get_base_message_template()
        base_message["content"] = message
        poller = self.client.begin_send(base_message)
        result = poller.result()

        
         
    
    
    