# Cấu trúc slide thuyết trình CS106 - Sudoku-Bench

## Tổng quan

- **Thời lượng mục tiêu:** 15 phút
- **Số slide đề xuất:** 24 slide
- **Nhịp trình bày gợi ý:**
  - Mở đầu và động cơ: 3 phút
  - Lý thuyết nền và paper gốc: 4 phút
  - Phương pháp của nhóm: 4 phút
  - Thực nghiệm, kết quả, kết luận: 4 phút

---

## Slide 1. Trang mở đầu

**Tiêu đề:**  
Đánh giá khả năng suy luận và giải quyết bài toán CSP của LLM thông qua Sudoku-Bench

**Nội dung:**
- Tên môn học: CS106 - Trí tuệ nhân tạo
- Nhóm thực hiện
- Giảng viên hướng dẫn

**Media:**
- Logo trường/khoa
- Có thể dùng một hình minh họa nhỏ của lưới Sudoku biến thể

---

## Slide 2. Câu hỏi trung tâm

**Tiêu đề:**  
LLM có thật sự suy luận logic hay chỉ nhận diện mẫu?

**Nội dung:**
- LLM rất mạnh ở sinh văn bản, code, trả lời câu hỏi
- Nhưng với bài toán cần tính nhất quán toàn cục, khả năng suy luận vẫn là dấu hỏi
- Câu hỏi nghiên cứu của đồ án:
  - LLM giải Sudoku biến thể tốt đến đâu?
  - Multi-step có giúp hơn single-shot không?

**Media:**
- Hình minh họa đối chiếu: “pattern recognition” và “constraint reasoning”

---

## Slide 3. Vì sao chọn Sudoku-Bench?

**Tiêu đề:**  
Vì sao Sudoku biến thể là bài kiểm tra hay cho suy luận?

**Nội dung:**
- Không chỉ là Sudoku chuẩn quen thuộc
- Mỗi đề có thêm luật riêng, buộc mô hình phải hiểu luật mới
- Cần tìm được “break-in” để mở khóa lời giải
- Giảm khả năng chỉ dựa vào mẫu đã thấy trong dữ liệu huấn luyện

**Media:**
- 1 ảnh Sudoku variant từ paper hoặc minh họa do nhóm tự tạo
- Chú thích: “Ví dụ một Sudoku variant với luật bổ sung ngoài Sudoku chuẩn”

---

## Slide 4. Mục tiêu đồ án

**Tiêu đề:**  
Mục tiêu của nhóm

**Nội dung:**
- Nghiên cứu lý thuyết về CSP và Sudoku variants
- Tái hiện một phần thiết kế thực nghiệm của paper Sudoku-Bench
- Xây dựng pipeline tự động:
  - chuẩn hóa đề
  - gọi LLM
  - kiểm tra đáp án
- So sánh:
  - Gemini 2.5 Flash
  - Gemini 2.5 Pro
  - single-shot và multi-step

---

## Slide 5. Bài toán CSP là gì?

**Tiêu đề:**  
Constraint Satisfaction Problem (CSP)

**Nội dung:**
- Một CSP gồm:
  - Biến
  - Miền giá trị
  - Tập ràng buộc
- Mục tiêu: gán giá trị cho tất cả biến sao cho mọi ràng buộc đều thỏa
- Sudoku là ví dụ trực quan của CSP

**Media:**
- Sơ đồ 3 thành phần: Variables - Domains - Constraints

---

## Slide 6. Sudoku chuẩn dưới góc nhìn CSP

**Tiêu đề:**  
Mô hình hóa Sudoku chuẩn thành CSP

**Nội dung:**
- Biến: từng ô trên lưới
- Miền giá trị: các số hợp lệ
- Ràng buộc:
  - mỗi hàng khác nhau
  - mỗi cột khác nhau
  - mỗi khối con khác nhau
- Có thể giải bằng backtracking, forward checking, AC-3, MRV

**Media:**
- Hình lưới Sudoku đơn giản với mũi tên chỉ:
  - hàng
  - cột
  - block

---

## Slide 7. Sudoku variants khó hơn ở đâu?

**Tiêu đề:**  
Từ Sudoku chuẩn đến Sudoku biến thể

**Nội dung:**
- Bổ sung thêm các ràng buộc:
  - Knight's move
  - Arrows
  - Thermometers
  - Killer cages
- Các ràng buộc có thể chồng chéo nhau
- Không gian tìm kiếm phức tạp hơn và cần suy luận sáng tạo hơn

**Media:**
- Bảng nhỏ liệt kê luật và ý nghĩa
- Có thể dùng icon hoặc mini-diagram cho từng luật

---

## Slide 8. Khái niệm “break-in”

**Tiêu đề:**  
Điểm đột phá logic - Break-in

**Nội dung:**
- Nhiều Sudoku variants lúc đầu gần như không có bước đi hiển nhiên
- Người giải cần phát hiện một suy luận then chốt
- Khi tìm được break-in, các bước sau lan truyền dần
- Đây là lý do variants phù hợp để đo suy luận sáng tạo

**Media:**
- Sơ đồ:
  - Trạng thái ban đầu khó
  - Một suy luận then chốt
  - Các ô được mở khóa dần

---

## Slide 9. Hạn chế của LLM trong CSP

**Tiêu đề:**  
Vì sao CSP là bài toán khó với LLM?

**Nội dung:**
- Khả năng quay lui kém
- Khó duy trì tính nhất quán toàn cục
- Dễ sinh chuỗi lập luận nghe hợp lý nhưng sai
- Nghiêng về “System 1” hơn là “System 2”

**Media:**
- Sơ đồ ngắn:
  - token tiếp theo
  - lỗi sớm
  - lỗi lan theo chuỗi suy luận

---

## Slide 10. Paper gốc Sudoku-Bench

**Tiêu đề:**  
Paper tham chiếu: Sudoku-Bench

**Nội dung:**
- Tác giả: Sakana AI, 2025
- Mục tiêu: đánh giá suy luận sáng tạo với Sudoku variants
- Benchmark gốc:
  - 15 bài 4x4
  - 15 bài 6x6
  - 70 bài 9x9
- Hai chế độ:
  - Single-shot
  - Multi-step

**Media:**
- Ảnh chụp trang đầu paper hoặc hình leaderboard từ paper
- Chú thích nguồn đầy đủ

---

## Slide 11. Hai chế độ đánh giá của paper

**Tiêu đề:**  
Single-shot vs Multi-step

**Nội dung:**
- **Single-shot:**
  - model nhận toàn bộ đề
  - trả về lưới hoàn chỉnh trong một lần
- **Multi-step:**
  - model đi từng bước
  - sau mỗi bước, hệ thống cập nhật lưới
  - sai một bước là dừng

**Media:**
- Sơ đồ hai cột so sánh luồng xử lý

---

## Slide 12. Chỉ số đánh giá của paper

**Tiêu đề:**  
Paper đo gì?

**Nội dung:**
- **ASR - Average Solve Rate**
  - tỷ lệ giải đúng hoàn toàn
- **ACP - Average Correct Placements**
  - số ô đúng trung bình trước khi dừng trong multi-step
- Ý nghĩa:
  - ASR đo thành công cuối cùng
  - ACP đo khả năng tiến xa trong suy luận từng bước

**Media:**
- Bảng nhỏ định nghĩa ASR và ACP

---

## Slide 13. Phạm vi tái hiện của nhóm

**Tiêu đề:**  
Nhóm tái hiện phần nào của paper?

**Nội dung:**
- Không tái hiện toàn bộ 100 bài vì giới hạn chi phí và thời gian
- Tập thực nghiệm rút gọn:
  - bài 4x4 để kiểm tra mức cơ sở
  - 5 bài 6x6 Killer Sudoku làm trọng tâm
  - 1 bài 9x9 đại diện
- Hai model:
  - Gemini 2.5 Flash
  - Gemini 2.5 Pro

**Media:**
- Bảng “paper gốc” vs “đồ án nhóm”

---

## Slide 14. Vì sao không chạy full benchmark?

**Tiêu đề:**  
Giới hạn chi phí của multi-step

**Nội dung:**
- Multi-step của nhóm:
  - 1 ô = 2 lượt gọi LLM
  - 1 lượt phân tích
  - 1 lượt điền số
- Với 6x6:
  - 36 ô = 72 lần gọi LLM / bài
- Với 9x9:
  - 81 ô = 162 lần gọi LLM / bài
- Vì vậy nhóm chọn một tập rút gọn hợp lý để vẫn có thực nghiệm nhưng kiểm soát chi phí

**Media:**
- Biểu đồ cột:
  - 6x6 = 72 calls
  - 9x9 = 162 calls

---

## Slide 15. Dữ liệu sử dụng

**Tiêu đề:**  
Tập bài toán của nhóm

**Nội dung:**
- Biến thể chính: Killer Sudoku
- Mỗi đề gồm:
  - lưới khởi tạo
  - nghiệm chuẩn
  - danh sách cage và tổng mục tiêu
- Dữ liệu 6x6 được kiểm tra tính nhất quán trước khi benchmark

**Media:**
- 1 ví dụ JSON rút gọn
- 1 ảnh minh họa cage trên lưới 6x6

---

## Slide 16. Pipeline tổng thể

**Tiêu đề:**  
Pipeline đánh giá tự động

**Nội dung:**
- Data Loader
- Text Representation
- LLM Interface
- Evaluator
- Output:
  - đúng / sai
  - log từng bước

**Media:**
- Sơ đồ pipeline dạng luồng:
  - Puzzle JSON -> Prompt Builder -> LLM -> Parser -> Validator -> Result

---

## Slide 17. Biểu diễn đề bài bằng văn bản

**Tiêu đề:**  
Từ đề bài sang prompt text-only

**Nội dung:**
- Không dùng ảnh
- Mô tả:
  - kích thước lưới
  - quy tắc
  - cage sums
  - hệ tọa độ
- Mục tiêu: đo suy luận logic, không đo thị giác máy tính

**Media:**
- Ảnh hoặc snippet một đoạn prompt thật
- Chú thích: “Ví dụ biểu diễn text-only của một đề 6x6”

---

## Slide 18. Cải tiến prompt của nhóm

**Tiêu đề:**  
Prompt engineering đã thêm gì?

**Nội dung:**
- Bổ sung luật rõ ràng hơn
- Thêm cheat sheet tổ hợp cage
- Với multi-step:
  - tách thành bước phân tích
  - rồi bước quyết định điền một ô
- Mục tiêu:
  - giảm lỗi diễn giải cage sums
  - buộc mô hình duy trì suy luận có cấu trúc

**Media:**
- Ảnh chụp cheat sheet hoặc bảng tổ hợp cage

---

## Slide 19. Ví dụ multi-step

**Tiêu đề:**  
Một vòng lặp multi-step diễn ra như thế nào?

**Nội dung:**
- Bước 1: mô hình phân tích toàn cục
- Bước 2: mô hình chọn đúng một ô để điền
- Hệ thống cập nhật lưới
- Nếu sai, dừng ngay vì không cho hoàn tác

**Media:**
- Sơ đồ vòng lặp 4 bước
- Có thể dùng ảnh trước/sau của một lưới 6x6

---

## Slide 20. Thiết lập thực nghiệm

**Tiêu đề:**  
Cấu hình thực nghiệm

**Nội dung:**
- Nền tảng: Python
- Model:
  - Gemini 2.5 Flash
  - Gemini 2.5 Pro
- Chế độ:
  - single-shot
  - multi-step
- Tập bài:
  - 4x4
  - 5 bài 6x6
  - 1 bài 9x9

**Media:**
- Bảng cấu hình thực nghiệm

---

## Slide 21. Bảng kết quả tổng hợp

**Tiêu đề:**  
Kết quả thực nghiệm

**Nội dung:**
- Bảng tổng hợp:
  - model
  - kích thước lưới
  - solve rate single-shot
  - solve rate multi-step
- Ghi chú:
  - số liệu sẽ được cập nhật sau khi chốt lần chạy cuối

**Media:**
- Bảng kết quả đầy đủ
- Chú thích:
  - “ASR / Solve rate trên tập thực nghiệm rút gọn của nhóm”

---

## Slide 22. Phân tích kết quả

**Tiêu đề:**  
Nhìn vào kết quả, cần quan sát gì?

**Nội dung:**
- 4x4 là bài kiểm tra mức cơ sở
- 6x6 là nơi so sánh chính giữa:
  - Flash vs Pro
  - single-shot vs multi-step
- 9x9 cho thấy chi phí và độ khó tăng khi mở rộng quy mô
- Chỉ kết luận trong phạm vi tập bài đã kiểm thử

**Media:**
- Biểu đồ cột so sánh solve rate
- Chú thích đầy đủ:
  - trục X: cấu hình
  - trục Y: solve rate (%)

---

## Slide 23. Phân tích lỗi

**Tiêu đề:**  
Nếu mô hình sai, sai theo kiểu nào?

**Nội dung:**
- Khung phân loại theo paper:
  - Incorrect Solution
  - Surrender
  - Claimed Contradiction
  - Missing Information
- Nếu tập bài rút gọn không phát sinh lỗi:
  - báo cáo đây là khung phân tích kế thừa từ paper
  - chưa đủ dữ liệu để thống kê phân bố lỗi riêng

**Media:**
- Bảng 4 loại lỗi và mô tả ngắn
- Nếu có log lỗi thật:
  - thêm biểu đồ cột hoặc pie chart tỷ lệ lỗi

---

## Slide 24. Kết luận

**Tiêu đề:**  
Kết luận chính

**Nội dung:**
- Nhóm đã tái hiện được một phần thiết kế của Sudoku-Bench
- Đã xây dựng pipeline tự động cho Sudoku biến thể
- Multi-step là một hướng hữu ích để khảo sát suy luận từng bước
- Việc mở rộng benchmark cần cân bằng giữa độ phủ và chi phí API

---

## Slide 25. Hạn chế

**Tiêu đề:**  
Hạn chế của đồ án

**Nội dung:**
- Tập thực nghiệm rút gọn, chưa đại diện đầy đủ cho toàn bộ paper
- Tập trung vào Killer Sudoku, chưa bao phủ nhiều loại variant
- Chưa tích hợp solver ký hiệu để kiểm tra hoặc hỗ trợ suy luận
- Kết quả 9x9 chỉ mang tính quan sát đại diện

---

## Slide 26. Hướng phát triển

**Tiêu đề:**  
Hướng phát triển tiếp theo

**Nội dung:**
- Mở rộng số lượng đề và số loại variant
- Bổ sung ACP cho multi-step
- So sánh thêm nhiều model hơn
- Kết hợp LLM với symbolic solver / Neuro-Symbolic AI

**Media:**
- Sơ đồ ý tưởng:
  - LLM hiểu luật
  - Solver ký hiệu tìm nghiệm

---

## Slide 27. Cảm ơn

**Tiêu đề:**  
Cảm ơn thầy và các bạn đã lắng nghe

**Nội dung:**
- Q&A

**Media:**
- Có thể để một hình Sudoku variant nền nhẹ

---

## Gợi ý rút gọn nếu cần còn 20 slide

- Gộp Slide 5 và 6
- Gộp Slide 7 và 8
- Gộp Slide 10 và 11
- Gộp Slide 15 và 17
- Gộp Slide 18 và 19
- Gộp Slide 24, 25 và 26 thành 2 slide

---

## Gợi ý phân công nói

- **Người 1:** Slide 1-4
- **Người 2:** Slide 5-12
- **Người 3:** Slide 13-20
- **Người 4:** Slide 21-27

---

## Các media nên chuẩn bị trước

1. Ảnh ví dụ Sudoku variant từ paper
2. Sơ đồ CSP
3. Sơ đồ single-shot vs multi-step
4. Sơ đồ pipeline của nhóm
5. Ảnh hoặc bảng cheat sheet cage combinations
6. Ảnh lưới Killer Sudoku 6x6 có cage
7. Bảng kết quả cuối cùng
8. Biểu đồ solve rate
9. Biểu đồ lỗi nếu có lỗi thật
10. Sơ đồ Neuro-Symbolic AI cho slide hướng phát triển
