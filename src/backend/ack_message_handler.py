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
        message += f"{str(self.pwm1) if self.pwm1 > 9 else '0' + str(self.pwm1)}{str(self.pwm2) if self.pwm2 > 9 else '0' + str(self.pwm2)}"
        match self.state:
            case LcdStatus.setBet:
                message += str(data.current_player["balance"])
                message += "$"
                message += str(data.current_bet)
            case LcdStatus.activeBet:
                message += str(data.current_player["balance"])
                message += "$"
                message += str(data.current_bet)
            case LcdStatus.idle:
                message += "Hello$world!"
            case LcdStatus.result:
                message += str(data.current_player["balance"] - data.current_bet)
                message += "$"
                message += str(data.current_player["balance"])
        print(message)
        return message