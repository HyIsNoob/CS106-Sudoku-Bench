# **KẾ HOẠCH TRIỂN KHAI ĐỒ ÁN CS106 \- TRÍ TUỆ NHÂN TẠO**

**Đề tài:** Đánh giá khả năng suy luận sáng tạo của LLM thông qua Sudoku-Bench.

**Reference Paper:** Sudoku-Bench: Evaluating creative reasoning with Sudoku variants (Sakana AI, 2025).

**Nhân sự:** 4 thành viên (Bao gồm Nguyễn Khang Hy).

**Thời gian:** 20 ngày.

## **1\. MỤC TIÊU ĐỒ ÁN**

1. Tái hiện lại một phần thí nghiệm trong bài báo: Đánh giá khả năng giải Sudoku biến thể (Variants) của ít nhất 2 LLMs (ví dụ: Gemini 1.5 Flash/Pro, GPT-4o-mini hoặc các model mã nguồn mở qua API miễn phí như Groq/Together AI).  
2. Xây dựng một Pipeline tự động: Đọc đề bài (Text) \-\> Gửi Prompt cho LLM \-\> Phân tích câu trả lời đúng/sai.  
3. Phân loại lỗi (Error Analysis) theo chuẩn bài báo: Incorrect Solution, Surrender, Missing Information, Claimed Contradiction.

## **2\. PHÂN CÔNG NHIỆM VỤ CHI TIẾT (4 NGƯỜI)**

### **Thành viên 1: Coder Chính / API Integration**

**Làm gì:** Xây dựng khung mã nguồn chính (Core Pipeline) bằng Python để giao tiếp với LLM.

**Làm như thế nào:**

* Đăng ký và lấy API Keys (Gemini API hiện đang miễn phí giới hạn, Groq API cung cấp Llama 3 miễn phí).  
* Viết 2 hàm chính tương ứng với 2 cấu hình đánh giá của bài báo:  
  * evaluate\_single\_shot(puzzle\_text, model): Yêu cầu model giải toàn bộ trong 1 lần.  
  * evaluate\_multi\_step(puzzle\_text, model): Tương tác nhiều vòng, mỗi vòng model điền 1 số, code sẽ tự động cập nhật bảng lưới và gửi lại.  
* Dùng json regex hoặc strict prompting (như Instructor/Marvin) để ép LLM trả về đúng định dạng (ví dụ trả về mảng 2D Python hoặc dictionary tọa độ) để dễ chấm điểm tự động.

### **Thành viên 2: Data Engineer**

**Làm gì:** Quản lý dữ liệu đầu vào (Dataset) và bộ chấm điểm (Evaluator).

**Làm như thế nào:**

* Lên HuggingFace tải dataset SakanaAI/Sudoku-Bench (hoặc lấy từ Github của bài báo).  
* Lọc ra tập 15 bài 4x4 và 15 bài 6x6 trước để chạy test (lưới 9x9 để chạy cuối cùng vì tốn token).  
* Viết script Python nhận đầu ra của Thành viên 1 (lời giải của LLM) và so sánh với file đáp án gốc (Ground Truth) để xuất ra kết quả True/False.  
* Nếu mô hình chạy sai, lưu lại file log text của phiên chat để Thành viên 3 và 4 phân tích.

### **Thành viên 3: Prompt Engineer & Tester**

**Làm gì:** Thiết kế prompt, chạy thực nghiệm và tìm cách tối ưu kết quả.

**Làm như thế nào:**

* Đọc kỹ cấu trúc Text Representation trong bài báo (Figure 3\) để hiểu cách họ mô tả bảng Sudoku bằng chữ.  
* Thử nghiệm nhiều kỹ thuật Prompt khác nhau để xem model nào giải tốt hơn:  
  * *Standard Prompt:* Chỉ đưa luật và yêu cầu giải.  
  * *Chain-of-Thought (CoT):* Yêu cầu model suy luận từng bước trước khi chốt số.  
* Chạy thực nghiệm hàng loạt (Batch testing) qua đêm để thu thập đủ số liệu của toàn bộ 30-100 câu đố.

### **Thành viên 4: Researcher & Report Writer**

**Làm gì:** Theo sát lý thuyết bài báo, phân tích lỗi và làm báo cáo, slide.

**Làm như thế nào:**

* Đọc kỹ phần 4 (Baseline Performance and Analysis) của paper.  
* Nhận file log từ Thành viên 2 & 3\. Dùng code Python (matplotlib/seaborn) hoặc Excel để vẽ các biểu đồ so sánh:  
  * Tỷ lệ giải đúng (Solve rate) giữa các models.  
  * Biểu đồ tròn/cột phân loại nguyên nhân LLM thất bại (Hình 4 trong bài báo).  
* Trực tiếp viết báo cáo môn học, giải thích tại sao LLM hiện tại (mặc dù rất mạnh) vẫn thất bại trước các quy tắc mới lạ của Sudoku Variants (do chưa có trong tập dữ liệu huấn luyện \- thiếu khả năng học luật mới zero-shot).

## **3\. TIMELINE TRIỂN KHAI (20 NGÀY)**

**Giai đoạn 1: Khởi động & Môi trường (Ngày 1 \- 4\)**

* Chốt nhóm, chia API key.  
* Hoàn thành script "Hello World": Gọi API thành công và lấy được chuỗi trả về.  
* Kéo thành công dataset từ HuggingFace về máy dạng file .json hoặc .csv.

**Giai đoạn 2: Tích hợp & Chạy thử nghiệm quy mô nhỏ (Ngày 5 \- 11\)**

* Ghép code của TV1 và TV2. Đưa thành công 1 bài Sudoku 4x4 vào LLM và chấm điểm đúng/sai tự động.  
* Xử lý các lỗi lặt vặt (API Rate limit, LLM trả về format rác không parse được).  
* TV3 bắt đầu tinh chỉnh Prompt.

**Giai đoạn 3: Chạy Benchmark toàn tập (Ngày 12 \- 16\)**

* Treo máy chạy toàn bộ dataset (15 câu 4x4, 15 câu 6x6, nếu dư thời gian/token thì chạy thêm 9x9) trên ít nhất 2 Models khác nhau.  
* Thu thập toàn bộ file JSON/CSV log kết quả.

**Giai đoạn 4: Đóng gói (Ngày 17 \- 20\)**

* TV4 tổng hợp số liệu, vẽ biểu đồ.  
* Cả nhóm rà soát lại báo cáo, viết file README.md cho mã nguồn.  
* Chuẩn bị slide và tập thuyết trình demo.