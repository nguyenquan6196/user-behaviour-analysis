from flask import Flask, jsonify
from data_analysis import DataAnalyzer

app = Flask(__name__)

@app.route('/api/daily-visits', methods=['GET'])
def get_daily_visits():
    analyzer = DataAnalyzer('data/sample_data.csv')
    daily_visits = analyzer.get_daily_visits()
    return jsonify(daily_visits.to_dict())

@app.route('/api/top-pages', methods=['GET'])
def get_top_pages():
    analyzer = DataAnalyzer('data/sample_data.csv')
    top_pages = analyzer.get_top_pages()
    return jsonify(top_pages.to_dict())

@app.route('/api/health', methods=['GET'])
def get_health():
    return jsonify({"status": "good"})

if __name__ == '__main__':
    app.run()