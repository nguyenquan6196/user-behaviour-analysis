import pandas as pd
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore

class DataAnalyzer:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        
    def get_daily_visits(self):
        daily_visits = self.df.groupby(self.df['timestamp'].dt.date).size()
        return daily_visits
    
    def get_top_pages(self, n=5):
        return self.df['page_url'].value_counts().head(n)
    
    def get_avg_session_duration(self):
        session_durations = self.df.groupby('session_id').agg({
            'timestamp': lambda x: (x.max() - x.min()).total_seconds()
        })
        return session_durations['timestamp'].mean()
    
    def export_to_excel(self, output_path):
        with pd.ExcelWriter(output_path) as writer:
            # Daily visits
            daily_visits = self.get_daily_visits()
            daily_visits.to_excel(writer, sheet_name='Daily Visits')
            
            # Top pages
            top_pages = self.get_top_pages()
            top_pages.to_excel(writer, sheet_name='Top Pages')
            
            # Session duration
            avg_duration = self.get_avg_session_duration()
            pd.Series({'Average Session Duration (s)': avg_duration}).to_excel(
                writer, sheet_name='Session Duration'
            )

if __name__ == "__main__":
    analyzer = DataAnalyzer('data/sample_data.csv')
    analyzer.export_to_excel('reports/excel_reports/analysis_results.xlsx')
