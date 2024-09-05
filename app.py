from flask import Flask, request, jsonify
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import os

app = Flask(__name__)

@app.route('/get-cron-schedule', methods=['GET'])
def get_cron_schedule():
    cron_expression = request.args.get('expression')
    count = request.args.get('count', default=5, type=int)

    if not cron_expression:
        return jsonify({'error': 'Cron expression is required'}), 400

    try:
        # Dividir a expressão cron de 7 campos
        cron_fields = cron_expression.split()
        if len(cron_fields) != 7:
            return jsonify({'error': 'Cron expression must have 7 fields'}), 400

        # Substituir "?" por "*", já que o APScheduler não suporta "?"
        cron_fields = ['*' if field == '?' else field for field in cron_fields]

        # Criar o trigger usando APScheduler (segundo, minuto, hora, dia do mês, mês, dia da semana)
        cron_trigger = CronTrigger(
            second=cron_fields[0],
            minute=cron_fields[1],
            hour=cron_fields[2],
            day=cron_fields[3],
            month=cron_fields[4],
            day_of_week=cron_fields[5]
        )

        # Obter a data/hora atual
        base_time = datetime.now()

        # Criar uma lista para armazenar as próximas execuções
        next_dates = []

        # Calcular as próximas execuções corretamente
        for _ in range(count):
            # Calcula a próxima execução com base no último "base_time"
            next_execution = cron_trigger.get_next_fire_time(None, base_time)
            next_dates.append(next_execution.strftime('%Y-%m-%d %H:%M:%S'))
            # Atualiza o base_time para a próxima iteração
            base_time = next_execution + timedelta(seconds=1)  # Incrementa o base_time em 1 segundo para garantir iteração correta

        return jsonify({'next_dates': next_dates}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
