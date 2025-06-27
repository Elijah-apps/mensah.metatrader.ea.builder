# mt5_connector.py
import zmq
import json

class MT5Connector:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5555")  # MT5 EA should be listening here
    
    def send_command(self, command, params=None):
        """Send command to MT5 EA"""
        message = {
            'action': command,
            'params': params or {}
        }
        self.socket.send_json(message)
        return self.socket.recv_json()
    
    def test_connection(self):
        return self.send_command('PING')
    
    def get_account_info(self):
        return self.send_command('ACCOUNT_INFO')
    
    def backtest_ea(self, ea_code, symbol, timeframe, start_date, end_date):
        """Send EA code to MT5 for backtesting"""
        return self.send_command('BACKTEST', {
            'ea_code': ea_code,
            'symbol': symbol,
            'timeframe': timeframe,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        })