from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()

class GoogleAnalyticsConnector:
    def __init__(self):
        # GA4 property ID should be stored in .env file
        self.property_id = os.getenv("GA_PROPERTY_ID")
        # Initialize the client
        # Note: This assumes you have set up authentication 
        # (either via GOOGLE_APPLICATION_CREDENTIALS env var or explicitly)
        self.client = BetaAnalyticsDataClient()
    
    def _process_response(self, response):
        """
        Process API response into a pandas DataFrame
        """
        rows = []
        for row in response.rows:
            row_data = {}
            for i, dimension in enumerate(response.dimension_headers):
                row_data[dimension.name] = row.dimension_values[i].value
            
            for i, metric in enumerate(response.metric_headers):
                row_data[metric.name] = row.metric_values[i].value
            
            rows.append(row_data)
        
        return pd.DataFrame(rows)
    
    

    def get_dashboard_metrics(self, current_period_days=7):
        """
        Get the dashboard metrics:
        - Active users
        - Event count
        - New users
        With comparison to previous period
        """
        # Calculate date ranges
        end_date = "today"
        start_date = f"{current_period_days}daysAgo"
        previous_start_date = f"{current_period_days*2}daysAgo"
        previous_end_date = f"{current_period_days+1}daysAgo"
        
        # Current period request
        current_request = RunReportRequest(
            property=f"properties/{self.property_id}",
            dimensions=[Dimension(name="date")],
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="eventCount"),
                Metric(name="newUsers"),
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        )
        
        # Previous period request
        previous_request = RunReportRequest(
            property=f"properties/{self.property_id}",
            dimensions=[Dimension(name="date")],
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="eventCount"),
                Metric(name="newUsers"),
            ],
            date_ranges=[DateRange(start_date=previous_start_date, end_date=previous_end_date)],
        )
        
        # Get responses
        current_response = self.client.run_report(current_request)
        previous_response = self.client.run_report(previous_request)
        
        # Process data
        current_data = self._process_response(current_response)
        previous_data = self._process_response(previous_response)
        
        # Calculate totals
        current_totals = {
            'activeUsers': current_data['activeUsers'].astype(float).sum(),
            'eventCount': current_data['eventCount'].astype(float).sum(),
            'newUsers': current_data['newUsers'].astype(float).sum()
        }
        
        previous_totals = {
            'activeUsers': previous_data['activeUsers'].astype(float).sum(),
            'eventCount': previous_data['eventCount'].astype(float).sum(),
            'newUsers': previous_data['newUsers'].astype(float).sum()
        }
        
        # Calculate percentage changes
        percentage_changes = {}
        for metric in current_totals:
            if previous_totals[metric] > 0:
                change = ((current_totals[metric] - previous_totals[metric]) / previous_totals[metric]) * 100
            else:
                change = 0
            percentage_changes[metric] = change
        
        return {
            'current_period': current_totals,
            'previous_period': previous_totals,
            'percentage_changes': percentage_changes,
            'raw_data': {
                'current_data': current_data,
                'previous_data': previous_data
            }
        }


# Example usage
if __name__ == "__main__":
    ga = GoogleAnalyticsConnector()

    dashboard_metrics = ga.get_dashboard_metrics(7)  # Last 7 days
    
    print(f"Active Users: {dashboard_metrics['current_period']['activeUsers']} "
          f"({dashboard_metrics['percentage_changes']['activeUsers']:.1f}%)")
    
    print(f"Event Count: {dashboard_metrics['current_period']['eventCount']} "
          f"({dashboard_metrics['percentage_changes']['eventCount']:.1f}%)")
    
    print(f"New Users: {dashboard_metrics['current_period']['newUsers']} "
          f"({dashboard_metrics['percentage_changes']['newUsers']:.1f}%)")
