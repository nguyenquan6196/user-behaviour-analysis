import pandas as pd

class DataAnalyzer:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        
    def get_daily_visits(self):
        daily_visits = self.df.groupby(self.df['timestamp'].dt.date).size()
        daily_visits.index = daily_visits.index.map(str)
        return daily_visits
    
    def get_top_pages(self, n=5):
        top_pages = self.df['page_url'].value_counts().head(n)
        return top_pages
    
    def get_avg_session_duration(self):
        session_durations = self.df.groupby('session_id')['event_duration'].mean()
        return session_durations
    
    def export_to_excel(self, output_path):
        with pd.ExcelWriter(output_path) as writer:
            # Daily visits
            daily_visits = self.get_daily_visits()
            daily_visits.to_excel(writer, sheet_name='Daily Visits')
            
            # Top pages
            top_pages = self.get_top_pages()
            top_pages.to_excel(writer, sheet_name='Top Pages')
            
            # Session duration
            session_durations = self.get_avg_session_duration()
            session_durations.to_excel(
                writer, 
                sheet_name='Session Duration',
                header=['Duration (seconds)']
            )

if __name__ == "__main__":
    analyzer = DataAnalyzer('data/user_behavior.csv')
    analyzer.export_to_excel('reports/excel_reports/analysis_results.xlsx')
