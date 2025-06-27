# api.py
from flask import Blueprint, request, jsonify
from mql5_generator import MQL5Generator
from mt5_connector import MT5Connector
import tempfile
import os

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/generate-mql5', methods=['POST'])
def generate_mql5():
    data = request.get_json()
    blocks_xml = data['blocks_xml']
    strategy_name = data['strategy_name']
    
    # Generate MQL5 code
    mql5_code = MQL5Generator.generate_ea(blocks_xml, strategy_name)
    
    # Create temporary .mq5 file
    with tempfile.NamedTemporaryFile(suffix='.mq5', delete=False) as temp_file:
        temp_file.write(mql5_code.encode('utf-8'))
        temp_path = temp_file.name
    
    return jsonify({
        'code': mql5_code,
        'file_path': temp_path
    })

@api_blueprint.route('/backtest', methods=['POST'])
def backtest():
    data = request.get_json()
    mt5 = MT5Connector()
    
    result = mt5.backtest_ea(
        ea_code=data['ea_code'],
        symbol=data.get('symbol', 'EURUSD'),
        timeframe=data.get('timeframe', 'M15'),
        start_date=data['start_date'],
        end_date=data['end_date']
    )
    
    return jsonify(result)