from flask import Flask, request, jsonify
from croniter import croniter
from datetime import datetime

app = Flask(__name__)

@app.route('/get-cron-schedule', methods=['GET'])
def get_cron_schedule():
    # Obter a expressão cron e o parâmetro da quantidade de datas
    cron_expression = request.args.get('cron_expression')
    param = request.args.get('param', default=5, type=int)  # Padrão é 5

    if not cron_expression:
        return jsonify({'error': 'Cron expression is required'}), 400

    try:
        # Data/hora atual
        base_time = datetime.now()

        # Cria um iterador a partir da expressão Cron
        cron = croniter(cron_expression, base_time)

        # Obtém as próximas 'param' datas
        next_dates = [cron.get_next(datetime).strftime('%Y-%m-%d %H:%M:%S') for _ in range(param)]

        return jsonify({'next_dates': next_dates}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
