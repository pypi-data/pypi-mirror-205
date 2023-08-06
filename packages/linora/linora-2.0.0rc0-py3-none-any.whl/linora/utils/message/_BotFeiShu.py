import requests

from linora.utils._logger import Logger


__all__ = ['BotFeiShu']


class BotFeiShu():
    """send message by Feishu
    
    Args:
        webhook: Feishu robot url
    """
    def __init__(self, webhook):
        warn = Logger(name='')
        warn.info(f"la.utils.message.BotFeiShu has been deprecated and will be deleted in version 2.1.0. Please use la.server.message.BotFeiShu")
        self.webhook = webhook
        
    def send_text(self, msg):
        """send message
        
        Args:
            msg: str, message
        Return:
            request post information.
        """
        t = requests.post(self.webhook, json={"msg_type": "text", "content":{"text": msg}})
        return t.content.decode()