import os
from flask import Flask, request, jsonify
from croniter import croniter
from datetime import datetime

app = Flask(__name__)

@app.route('/get-cron-schedule', methods=['GET'])
def get_cron_schedule():
    cron_expression = request.args.get('expression')
    count = request.args.get('count', default=5, type=int)

    if not cron_expression:
        return jsonify({'error': 'Cron expression is required'}), 400

    try:
        base_time = datetime.now()
        cron = croniter(cron_expression, base_time)
        next_dates = [cron.get_next(datetime).strftime('%Y-%m-%d %H:%M:%S') for _ in range(count)]

        return jsonify({'next_dates': next_dates}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # O Render define a porta na variável de ambiente PORT
    app.run(host='0.0.0.0', port=port, debug=True)
