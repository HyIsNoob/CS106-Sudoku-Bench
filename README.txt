1. Thư mục Demo
Thư mục chứa toàn bộ mã nguồn của trang giao diện mô phỏng từng bước lập luận phân tích của mô hình khi giải quyết câu đố (Từ log đã chạy).
python -m http.server 8000
http://localhost:8000/src/

2. Thư mục Source-Code
Thư mục chứa toàn bộ mã nguồn, dữ liệu và các outputs chạy thực nghiệm đánh giá.
Cụ thể:
dataset/: Chứa tập dữ liệu câu đố Killer Sudoku đã được chuẩn hóa dưới dạng JSON
map/: Lưu trữ file cấu hình bản đồ câu đố gốc trước khi xử lý.
6x6/ và 9x9/: Chứa các file Jupyter Notebook dùng để trực tiếp chạy thực nghiệm kích hoạt API Gemini tương ứng với từng kích thước lưới.
outputs/: Nơi lưu trữ toàn bộ logs và kết quả phản hồi thô định dạng JSON trả về từ các lần gọi mô hình.
evaluation/: Chứa các mã nguồn phân tích dữ liệu.
Extra-ToT: Mã nguồn của 2 phương pháp thực nghiệm thêm: Iterative Correction Loop và Tree of Thoughts với mô hình gemini-3.1-flash-lite để giải các câu đố Killer Sudoku.

3. Thư mục Documents
Thư mục chứa paper tham chiếu và slide thuyết trình.
Tài liệu Slide:
documents/Nhom3-Slide-CS106.pdf: File slide ở dạng PDF.
Đường dẫn Slide Canva trực tuyến: https://www.canva.com/design/DAHKBMZOuVg/Q74T1PaEqTJo_YCqyY1qWg/edit
Bài báo tham khảo gốc của Sakana.AI: Sudoku-Bench: Evaluating creative reasoning with Sudoku variants




