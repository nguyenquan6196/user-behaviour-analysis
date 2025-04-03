import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_mock_data(num_users=20, num_records=100):
    # Các trang web mẫu
    pages = [
        '/home', 
        '/products', 
        '/product-detail',
        '/cart', 
        '/checkout',
        '/about',
        '/contact',
        '/blog',
        '/profile',
        '/search'
    ]
    
    # Các loại event
    event_types = ['view', 'click', 'scroll', 'submit']
    
    # Tạo danh sách user_ids
    user_ids = list(range(1001, 1001 + num_users))
    
    # List để lưu các records
    records = []
    
    # Tạo thời gian end là hiện tại
    end_time = datetime.now()
    # Thời gian start là 5 ngày trước
    start_time = end_time - timedelta(days=5)
    
    current_session_id = 5001
    
    def generate_event_duration(event_type, is_last_in_session=False):
        # Base duration theo event type
        base_durations = {
            'view': (30, 180),    # 30s - 3m
            'click': (10, 60),    # 10s - 1m
            'scroll': (20, 120),  # 20s - 2m
            'submit': (5, 30)     # 5s - 30s
        }
        
        if is_last_in_session:
            # Các trường hợp đặc biệt cho event cuối
            scenarios = [
                (0.3, lambda: random.randint(1, 10)),          # Đóng tab ngay: 1-10s
                (0.2, lambda: 1800),                           # Timeout 30m
                (0.3, lambda: random.randint(60, 300)),        # Inactive: 1-5m
                (0.2, lambda: random.randint(10, 60))          # Logout bình thường: 10-60s
            ]
            
            # Chọn ngẫu nhiên một scenario theo weight
            scenario = random.choices(scenarios, weights=[w for w, _ in scenarios])[0]
            return scenario[1]()
        else:
            min_dur, max_dur = base_durations[event_type]
            return random.randint(min_dur, max_dur)

    # Với mỗi user
    for user_id in user_ids:
        # Mỗi user có 2-5 sessions trong 5 ngày
        num_sessions = random.randint(2, 5)
        
        for _ in range(num_sessions):
            # Tạo thời gian bắt đầu ngẫu nhiên cho session này
            random_minutes = random.randint(0, int((end_time - start_time).total_seconds() / 60))
            session_start = start_time + timedelta(minutes=random_minutes)
            
            # Đảm bảo session không kéo dài quá 30 phút
            session_end = min(
                session_start + timedelta(minutes=30),
                end_time
            )
            
            # Tạo session_id unique
            session_id = f"{user_id}_{current_session_id}"
            current_session_id += 1
            
            # Số lượng actions trong session này (3-8 actions)
            num_actions = random.randint(3, 8)
            
            # Typical flows với xác suất cao hơn
            typical_flows = [
                ['/home', '/products', '/product-detail', '/cart', '/checkout'],
                ['/home', '/blog', '/product-detail'],
                ['/home', '/search', '/product-detail', '/cart'],
                ['/home', '/profile', '/cart', '/checkout'],
                ['/home', '/about', '/contact'],
                ['/home', '/search', '/products', '/product-detail']
            ]
            
            # 70% chance để sử dụng typical flow
            if random.random() < 0.7:
                page_sequence = random.choice(typical_flows)
                # Cắt sequence nếu dài hơn num_actions
                page_sequence = page_sequence[:num_actions]
            else:
                page_sequence = random.sample(pages, num_actions)
            
            # Tính thời gian giữa các actions trong session
            available_time = (session_end - session_start).total_seconds()
            time_per_action = available_time / (len(page_sequence) + 1)
            
            current_time = session_start
            for i, page in enumerate(page_sequence):
                is_last = (i == len(page_sequence) - 1)
                event_type = random.choice(event_types)
                event_duration = generate_event_duration(event_type, is_last)
                
                event = {
                    'user_id': user_id,
                    'session_id': session_id,
                    'page_url': page,
                    'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'event_type': event_type,
                    'event_duration': event_duration
                }
                records.append(event)
                
                current_time += timedelta(seconds=event_duration)
    
    # Tạo DataFrame
    df = pd.DataFrame(records)
    
    # Sắp xếp theo timestamp
    df = df.sort_values('timestamp')
    
    return df

# Tạo dữ liệu mẫu
mock_data = generate_mock_data(num_users=20, num_records=100)

# Lưu vào file CSV
mock_data.to_csv('data/user_behavior.csv', index=False)

# In thống kê
print("Đã tạo xong dữ liệu mẫu!")
print("\nMẫu dữ liệu:")
print(mock_data.head(10))
print("\nThống kê:")
print(f"Tổng số records: {len(mock_data)}")
print(f"Số lượng users unique: {mock_data['user_id'].nunique()}")
print(f"Số lượng sessions unique: {mock_data['session_id'].nunique()}")
print("\nPhân bố thời gian:")
mock_data['date'] = pd.to_datetime(mock_data['timestamp']).dt.date
print(mock_data.groupby('date').size())
