class NotificationService:
    def __init__(self,*channels) -> None: self.channels=channels
    def info(self,message: str) -> None:
        for channel in self.channels:
            if hasattr(channel,"info"): channel.info(message)
    def critical(self,message: str) -> None:
        for channel in self.channels:
            if hasattr(channel,"critical"): channel.critical(message)
