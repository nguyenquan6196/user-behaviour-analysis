# User Behavior Analysis Project

## Cài đặt môi trường

1. Tạo môi trường ảo Python:
```bash
python -m venv venv
```

2. Kích hoạt môi trường ảo:
- Windows:
```bash
venv\Scripts\activate
```
- macOS/Linux:
```bash
source venv/bin/activate
```

3. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Cấu hình Google Analytics API

1. Truy cập Google Cloud Console
2. Tạo project mới
3. Enable Google Analytics Data API
4. Tạo Service Account và tải file credentials JSON
5. Đổi tên file credentials thành `ga_credentials.json` và đặt trong thư mục gốc
6. Tạo file .env và thêm các thông tin:
