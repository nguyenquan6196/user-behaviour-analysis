import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import io
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from data_analysis import DataAnalyzer

class ReportGenerator:
    def __init__(self, csv_file):
        # Register font
        pdfmetrics.registerFont(TTFont('Calibri', 'C:/Windows/Fonts/Calibri.ttf'))
        
        self.analyzer = DataAnalyzer(csv_file)
        
        self.styles = getSampleStyleSheet()
        
        # Customize style with font
        self.styles['Normal'].fontName = 'Calibri'
        self.styles['Heading1'].fontName = 'Calibri'
        self.styles['Heading2'].fontName = 'Calibri'
        
        self.elements = []

    def analyze_data(self):
        """Enhanced data analysis"""
        analysis = {
            'daily_visits': self.analyzer.get_daily_visits(),
            'top_pages': self.analyzer.get_top_pages(),
            'avg_session_duration': self.analyzer.get_avg_session_duration(),
        }
        
        return analysis

    def create_visualizations(self):
        """Enhanced visualizations"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 13))
        
        # Plot daily visits
        daily_visits = self.analyze_data()['daily_visits']
        daily_visits.plot(kind='line', ax=ax1)
        ax1.set_title("Daily Visits")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Visit Count")
        ax1.tick_params(axis='x', rotation=45)
        
        # Plot top pages
        top_pages = self.analyze_data()['top_pages']
        top_pages.plot(kind='bar', ax=ax2)
        ax2.set_title("Top 5 Most Visited Pages")
        ax2.set_xlabel("Page URL")
        ax2.set_ylabel("Visit Count")
        ax2.tick_params(axis='x', rotation=45)
        
        # Điều chỉnh khoảng cách và layout
        plt.subplots_adjust(hspace=0.5)  # Đặt trước khi lưu
        
        # Save plot to buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, bbox_inches='tight')
        img_buffer.seek(0)
        return img_buffer

    def generate_recommendations(self):
        """Generate recommendations based on analysis"""
        daily_visits = self.analyze_data()['daily_visits']
        top_pages = self.analyze_data()['top_pages']
        
        # Format daily visits details
        daily_visits_details = "\n".join([f"- Ngày {date}: {count} lượt truy cập" 
                                        for date, count in daily_visits.items()])
        
        # Format top pages details
        top_pages_details = "\n".join([f"- Trang {url}: {count} lượt truy cập" 
                                     for url, count in top_pages.items()])
        
        recommendations = [
            "1. Phân tích lượt truy cập hàng ngày:",
            f"{daily_visits_details}",
            "→ Nhận xét: Có sự dao động lớn về lượt truy cập giữa các ngày."
            "→ Đề xuất: Cần phân tích kỹ các ngày có lượt truy cập thấp để tìm nguyên nhân và có giải pháp cải thiện.",
            
            "2. Phân tích các trang được truy cập nhiều:"
            f"{top_pages_details}"
            "→ Đề xuất cải thiện:"
            "   - Tối ưu hóa tốc độ tải trang"
            "   - Cải thiện giao diện người dùng"
            "   - Thêm các tính năng tương tác để tăng thời gian người dùng ở lại trang",
            
            "3. Đề xuất chung về cải thiện website:"
            "   - Thực hiện A/B testing để tối ưu giao diện"
            "   - Phân tích và cải thiện SEO cho các trang ít được truy cập"
            "   - Thêm các tính năng theo dõi hành vi người dùng chi tiết hơn"
            "   - Tạo chiến lược content marketing để tăng lưu lượng truy cập"
        ]
        
        return recommendations

    def create_report(self):
        # Tạo buffer để lưu PDF
        buffer = io.BytesIO()
        
        # Tạo document với buffer thay vì file path
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            fontSize=24,
            spaceAfter=30,
            alignment=1,
            fontName='Calibri'
        )
        self.elements.append(Paragraph("BÁO CÁO PHÂN TÍCH DỮ LIỆU", title_style))
        self.elements.append(Spacer(1, 20))

        # Detailed analysis section
        analysis = self.analyze_data()
        self.elements.append(Paragraph("1. Kết Quả Phân Tích", self.styles['Heading1']))
        
        # Daily visits
        self.elements.append(Paragraph("1.1 Lượt truy cập hàng ngày", self.styles['Heading2']))
        self.elements.append(Paragraph(
            f"Tổng số lượt truy cập: {analysis['daily_visits'].sum()}",
            self.styles['Normal']
        ))
        daily_visits = analysis['daily_visits']
        for date, count in daily_visits.items():
            self.elements.append(Paragraph(
                f"• {date}: {count} lượt truy cập",
                ParagraphStyle(
                    'Indented',
                    parent=self.styles['Normal'],
                    leftIndent=30
                )
            ))
        self.elements.append(Spacer(1, 12))

        # Top pages
        self.elements.append(Paragraph("1.2 Trang được truy cập nhiều nhất", self.styles['Heading2']))
        top_pages = analysis['top_pages']
        for url, count in top_pages.items():
            self.elements.append(Paragraph(
                f"• {url}: {count} lượt truy cập",
                ParagraphStyle(
                    'Indented',
                    parent=self.styles['Normal'],
                    leftIndent=30
                )
            ))
        self.elements.append(Spacer(1, 12))
        
        # Average session duration
        self.elements.append(Paragraph("1.3 Thời gian trung bình mỗi phiên", self.styles['Heading2']))
        session_durations = analysis['avg_session_duration']
        self.elements.append(Paragraph(
            f"Tổng số phiên: {len(session_durations)}",
            self.styles['Normal']
        ))
        for session_id, duration in session_durations.items():
            self.elements.append(Paragraph(
                f"• Phiên {session_id}: {duration:.2f} giây",
                ParagraphStyle(
                    'Indented',
                    parent=self.styles['Normal'],
                    leftIndent=30
                )
            ))
        self.elements.append(Spacer(1, 12))

        # Visualization section
        self.elements.append(Paragraph("2. Trực Quan Hóa Dữ Liệu", self.styles['Heading1']))
        img_buffer = self.create_visualizations()
        img = Image(img_buffer, width=15*cm, height=20*cm)
        self.elements.append(img)
        self.elements.append(Spacer(1, 40))

        # Recommendations section
        self.elements.append(Paragraph("3. Đề Xuất Cải Thiện", self.styles['Heading1']))
        recommendations = self.generate_recommendations()
        for rec in recommendations:
            if rec.startswith("→"):
                # Indent recommendations that start with arrow
                self.elements.append(Paragraph(
                    rec,
                    ParagraphStyle(
                        'Indented',
                        parent=self.styles['Normal'],
                        leftIndent=30
                    )
                ))
            else:
                self.elements.append(Paragraph(rec, self.styles['Normal']))
            self.elements.append(Spacer(1, 10))

        # Build PDF vào buffer
        doc.build(self.elements)
        
        # Trả về bytes của PDF
        buffer.seek(0)
        return buffer.getvalue()

if __name__ == "__main__":
    report_gen = ReportGenerator("data/user_behavior.csv")
    report_gen.create_report()
