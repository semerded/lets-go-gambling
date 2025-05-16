from src.enums import LcdStatus
from src import data

class AckMessageHandler:
    def __init__(self):
        self.state = LcdStatus.idle
        self.pwm1 = 0
        self.pwm2 = 0
        self.checksum = 0
        
        self.update_available = True
        self.current_bet_tracker = None
        self.balance_tracker = None
        
    def set_state(self, state: LcdStatus):
        if self.state == state:
            return
        self.state = state
        self.update_available = True
        
    def set_pwm(self, pwm1, pwm2):
        if self.pwm1 != pwm1 or self.pwm2 != pwm2:
            self.pwm1 = pwm1
            self.pwm2 = pwm2
            self.update_available = True
        
    def check_for_update(self):
        if self.update_available:
            return True
        if self.current_bet_tracker != data.current_bet:
            self.current_bet_tracker = data.current_bet
            return True
        if self.balance_tracker != data.current_player["balance"]:
            self.balance_tracker = data.current_player["balance"]
            return True
        return False
        
    def get_checksum(self):
        self.checksum += 1
        if self.checksum > 999:
            self.checksum = 0
        
        _chk = str(self.checksum)
        if self.checksum < 10:
            _chk = "00" + _chk
        elif self.checksum < 100:
            _chk = "0" + _chk
        return _chk
        
    def get_message(self) -> str:
        message: str = self.get_checksum() + self.state.value
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
                message += str(data.current_bet)
                message += "$"
                message += str(data.current_player["balance"])
        print(message)
        self.update_available = False
        return message