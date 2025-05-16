from src.enums import LcdStatus
from src import data

class AckMessageHandler:
    def __init__(self):
        self.state = LcdStatus.idle
        self.pwm1 = 0
        self.pwm2 = 0
        
    def set_state(self, state: LcdStatus):
        self.state = state
        
    def set_pwm(self, pwm1, pwm2):
        self.pwm1 = pwm1
        self.pwm2 = pwm2
        
    def get_message(self) -> str:
        message: str = self.state.value
        message += f"{self.pwm1}{self.pwm2}"
        match self.state:
            case LcdStatus.setBet:
                message += data.current_player["balance"]
                message += "$"
                message += data.current_bet
            case LcdStatus.activeBet:
                message += data.current_player["balance"]
                message += "$"
                message += data.current_bet
            case LcdStatus.idle:
                message += "Hello$world!"
            case LcdStatus.result:
                message += data.current_player["balance"] - data.current_bet
                message += "$"
                message += data.current_player["balance"]
        print(message)
        return message