from flask import Flask, jsonify, send_file, make_response
from io import BytesIO
from data_analysis import DataAnalyzer
from report_generator import ReportGenerator
from datetime import datetime

app = Flask(__name__)

@app.route('/api/daily-visits', methods=['GET'])
def get_daily_visits():
    analyzer = DataAnalyzer('data/user_behavior.csv')
    daily_visits = analyzer.get_daily_visits()
    return jsonify(daily_visits.to_dict())

@app.route('/api/top-pages', methods=['GET'])
def get_top_pages():
    analyzer = DataAnalyzer('data/user_behavior.csv')
    top_pages = analyzer.get_top_pages()
    return jsonify(top_pages.to_dict())

@app.route('/api/avg-session-duration', methods=['GET'])
def get_avg_session_duration():
    analyzer = DataAnalyzer('data/user_behavior.csv')
    avg_session_duration = analyzer.get_avg_session_duration()
    return jsonify(avg_session_duration.to_dict())

@app.route('/api/health', methods=['GET'])
def get_health():
    return jsonify({"status": "okee"})

@app.route('/api/download-report', methods=['GET'])
def download_report():
    try:
        # Tạo timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_report_{timestamp}.pdf"
        
        # Tạo report
        report_gen = ReportGenerator("data/user_behavior.csv")
        pdf_content = report_gen.create_report()
        
        # Tạo response với PDF content
        buffer = BytesIO(pdf_content)
        response = make_response(send_file(
            buffer,
            mimetype='application/pdf',
            download_name=filename
        ))
        
        # Thêm headers
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        
        return response
        
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)