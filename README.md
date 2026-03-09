# So sánh AI WAF và Regex (WAF Comparison)
Dự án này thực hiện so sánh đối chiếu giữa hai phương pháp phát hiện mã độc trong HTTP Request (Web Application Firewall):
1. **Phương pháp truyền thống:** Sử dụng Regular Expression (Regex).
2. **Phương pháp trí tuệ nhân tạo:** Sử dụng mô hình Random Forest Classifier.

## Kết quả đánh giá
Mô hình tập trung so sánh các chỉ số quan trọng:
* **Accuracy (Độ chính xác):** Khả năng phân loại đúng payload lành tính và độc hại.
* **Recall & Precision:** Khả năng bắt sót và bắt nhầm mã độc.
* **Latency (Độ trễ):** Thời gian xử lý của mỗi phương pháp (tính bằng ms).
* **Bypass Test:** Kiểm tra khả năng nhận diện các payload đã qua mặt (obfuscation).

## Công nghệ sử dụng
* **Ngôn ngữ:** Python
* **Thư viện:** Scikit-learn, Pandas, TfidfVectorizer
* **Mô hình:** Random Forest (100 estimators)
* **Dataset:** CSIC 2010 HTTP Dataset

## Cách chạy
1. Đảm bảo bạn có file dữ liệu `csic_database.csv`.
2. Chạy file `AI-WAF-vs-Regex-Comparison.py`.
