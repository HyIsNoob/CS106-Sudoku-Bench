# Phân Công Thuyết Trình 3 Người - CS106 Sudoku-Bench

---

## Tổng Quan Phân Công

| Người | Phạm vi slide trong PDF | Vai trò chính | Thời lượng gợi ý |
|---|---:|---|---:|
| Người A | Slide 1-22 | Mở bài, vấn đề nghiên cứu, paper, lý thuyết, thiết kế đánh giá, phạm vi tái hiện | 7-8 phút |
| Người B | Slide 23-37 | Pipeline thực nghiệm, dataset, prompt, validator, kết quả 6x6 | 8-9 phút |
| Người C | Slide 38-55 | 9x9, so sánh single/multi, phân tích lỗi, so sánh paper, demo, hạn chế, kết luận | 8-9 phút |

Tổng thời lượng mục tiêu: **23-25 phút**, gồm slide và demo. Nếu cần rút xuống 20 phút, xem phần timeline rút gọn ở cuối file.

---

## Người A - Mở Bài, Paper Và Lý Thuyết

**Phạm vi chính: Slide 1-22**

Người A cần làm nhiệm vụ “đặt sân”: giải thích vì sao nhóm chọn paper này, paper đang kiểm tra năng lực gì của LLM, và nhóm tái hiện trong phạm vi nào.

### Slide Phụ Trách

| Slide | Tiêu đề/nội dung trên PDF | Cách nói chính |
|---:|---|---|
| 1 | Trang bìa | Giới thiệu đề tài, nhóm, môn học, GVHD |
| 2 | Thành viên trong nhóm | Nói nhanh danh sách thành viên |
| 3 | Table of Content | Dẫn cấu trúc 6 phần lớn |
| 4 | Section 01 - Vấn đề nghiên cứu | Chuyển vào vấn đề |
| 5 | Vấn đề nghiên cứu | LLM mạnh nhưng bài logic ràng buộc cần đúng tuyệt đối |
| 6 | Câu hỏi nghiên cứu | Nêu 5 câu hỏi nhóm kiểm tra |
| 7 | Paper tham chiếu | Giới thiệu Sudoku-Bench và mục tiêu creative reasoning |
| 8 | Vì sao chọn Sudoku-Bench? | Paper cụ thể, có benchmark, có ground truth, phù hợp yêu cầu môn |
| 9 | Section 02 - Cơ sở lý thuyết và paper tham chiếu | Chuyển sang nền tảng |
| 10 | Constraint reasoning trong Sudoku-Bench | Nhấn mạnh nhóm không làm CSP solver, dùng góc nhìn ràng buộc để đánh giá LLM |
| 11 | Text representation của paper | Paper chuyển puzzle sang text, nhóm cũng lưu JSON/text để gọi LLM |
| 12 | Một số biến thể phổ biến | Giới thiệu Knight, Arrow, Thermometer, Killer Cage |
| 13 | Sudoku variants | Slide hình/nhấn lại ý: variant thêm luật ngoài Sudoku chuẩn |
| 14 | Killer Sudoku | Giải thích cage sum, không lặp trong cage, phải kết hợp nhiều ràng buộc |
| 15 | Break-in | Giải thích bước mở khóa trong Sudoku variants |
| 16 | Break-in | Slide nhấn mạnh khái niệm, nói ngắn |
| 17 | Vì sao Sudoku variants khó với LLM? | Khó duy trì trạng thái, khó quay lui, reasoning nghe đúng chưa chắc đúng |
| 18 | Section 03 - Thiết kế đánh giá và phạm vi tái hiện | Chuyển sang cách paper đánh giá |
| 19 | Thiết kế đánh giá của paper | Single-shot vs multi-step |
| 20 | Chỉ số đánh giá | Solve rate, final status, error type, number of steps |
| 21 | Phạm vi tái hiện của nhóm | Killer Sudoku, 5 puzzle 6x6, 2 puzzle 9x9, 4 model Gemini |
| 22 | Vì sao không chạy toàn bộ benchmark? | Chi phí/thời gian API; 9x9 nhiều lượt gọi |

### Ý Chính Cần Chốt

- Đề tài không phải xây solver Sudoku truyền thống.
- Đề tài là tái hiện rút gọn paper Sudoku-Bench để đánh giá reasoning của LLM.
- Sudoku variants phù hợp vì có luật rõ, ground truth rõ, nhưng cần duy trì nhiều ràng buộc.
- Nhóm chọn Killer Sudoku vì đủ rõ để prompt hóa, validate và phân tích lỗi.
- Nhóm chạy rút gọn do chi phí và thời gian, nhưng vẫn có pipeline, log, validator và evaluation.

### Câu Chuyển Cho Người B

> Sau khi đã biết paper đánh giá LLM bằng Sudoku variants như thế nào, phần tiếp theo sẽ đi vào hệ thống thực nghiệm của nhóm: dữ liệu được lưu ra sao, prompt được tạo như thế nào, model trả lời ra sao và validator kiểm tra kết quả như thế nào.

---

## Người B - Pipeline Thực Nghiệm Và Kết Quả 6x6

**Phạm vi chính: Slide 23-38**

Người B là người phụ trách chính phần pipeline và 6x6. Đây là khối nói liền mạch: từ cách nhóm chạy thực nghiệm đến kết quả 6x6.

### Slide Phụ Trách

| Slide | Tiêu đề/nội dung trên PDF | Cách nói chính |
|---:|---|---|
| 23 | Section 04 - Pipeline thực nghiệm của nhóm | Mở phần thực nghiệm |
| 24 | Dataset | Giải thích JSON gồm id, difficulty, grid_size, puzzle, solution, cages |
| 25 | Pipeline tổng quát | Data Loader -> Prompt Builder -> LLM API -> Parser -> Validator -> Logger -> Evaluation |
| 26 | Single-prompt evaluation | Một lần gọi model, trả về grid hoàn chỉnh |
| 27 | Multi-step evaluation | Mỗi vòng analysis + fill, điền từng ô, validator kiểm tra ngay |
| 28 | Định dạng output multi-step | JSON có cell, value, reasoning, is_certain |
| 29 | Killer Sudoku cheat sheet | Cheat sheet là context tổ hợp cage, không phải lời giải |
| 30 | Validator | Nhấn mạnh validator chỉ kiểm tra, không giúp model suy nghĩ |
| 31 | Section 05 - Kết quả và phân tích | Chuyển sang kết quả |
| 32 | Kết quả single-prompt hiện tại | Bảng 6x6 single-prompt: 2.5 Pro và 3.5 Flash đạt 5/5 |
| 33 | Nhận xét single-prompt | Nói ngắn, tập trung 6x6; lưu ý slide này có câu 9x9 cũ cần sửa trên Canva |
| 34 | Chi tiết single-prompt 6x6 | Bảng từng puzzle 6x6 |
| 35 | Chi tiết single-prompt 9x9 | Nói như cầu nối: khi lên 9x9, single-prompt giảm mạnh |
| 36 | Kết quả multi-step 6x6 | 3.5 Flash đạt 5/5; 2.5 Flash và 2.5 Pro đạt 4/5 |
| 37 | Chi tiết multi-step 6x6 | Bảng từng puzzle, nhấn số bước trước khi fail |

### Ý Chính Cần Chốt

- Dataset có ground truth nên đánh giá khách quan.
- Single-prompt rẻ hơn, đơn giản hơn, nhưng khi sai khó biết sai từ đâu.
- Multi-step tốn chi phí hơn nhưng có log reasoning từng bước.
- Validator không vi phạm yêu cầu “không hỗ trợ AI suy nghĩ”; validator chỉ kiểm tra sau khi model đã trả lời.
- Cheat sheet không chứa nghiệm puzzle, chỉ giảm lỗi tính toán tổ hợp cage.
- 6x6 easy là phạm vi mà model mạnh làm khá tốt:
  - Gemini 2.5 Pro: 5/5 single-prompt.
  - Gemini 3.5 Flash: 5/5 single-prompt và 5/5 multi-step.
  - Gemini 3.1 Flash Lite: baseline yếu, fail toàn bộ.
- Slide 35 nên được nói rất ngắn như “đây là dấu hiệu đầu tiên cho thấy 9x9 khó hơn”, rồi chuyển sang multi-step 6x6.

### Câu Chuyển Cho Người C

> Với 6x6, các model mạnh đã giải khá tốt nên chưa phân hóa hết năng lực reasoning. Phần tiếp theo sẽ quan trọng hơn: khi tăng lên 9x9 hard, single-prompt và multi-step khác nhau rất rõ, và đây là phần thể hiện rõ nhất tinh thần của Sudoku-Bench.

---

## Người C - 9x9, Phân Tích, Demo Và Kết Luận

**Phạm vi chính: Slide 39-56**

Người C phụ trách khối cuối: 9x9, tổng hợp kết quả, phân tích lỗi, liên hệ paper, demo và kết luận. Đây là phần “chốt luận điểm” của bài.

### Slide Phụ Trách

| Slide | Tiêu đề/nội dung trên PDF | Cách nói chính |
|---:|---|---|
| 38 | Kết quả multi-step 9x9 | Bảng chính: 2.5 Pro và 3.5 Flash đạt 2/2; hai model yếu fail |
| 39 | Chi tiết multi-step 9x9 | Nhấn average correct placements và No Certain Move |
| 40 | So sánh single-prompt và multi-step | Bảng tổng hợp 6x6/9x9, đây là slide rất quan trọng |
| 41 | So sánh single-prompt và multi-step | Kết luận: cần xem đồng thời size, model và mode |
| 42 | Ví dụ single-prompt fail | Một ô sai cũng làm whole solution fail |
| 43 | Ví dụ multi-step thành công | Reasoning cage/subgrid r3c3 = 2, log giúp quan sát quá trình |
| 44 | Phân tích lỗi | Incorrect Solution vs No Certain Move |
| 45 | Error type theo paper | Liên hệ taxonomy lỗi của paper |
| 46 | Vì sao 9x9 khó hơn? | 81 ô, miền 1-9, nhiều tổ hợp cage, context dài hơn |
| 47 | Nhận định từ kết quả hiện tại | Tổng hợp insight: 6x6 khả thi, 9x9 phân tách rõ |
| 48 | So sánh với paper gốc | Quan sát của nhóm khớp tinh thần paper |
| 49 | So sánh với paper gốc | Slide chuyển/chốt phần paper, nói ngắn |
| 50 | Section 06 - Demo, kết luận và hướng phát triển | Chuyển sang phần cuối |
| 51 | Demo | Mở web demo; nếu Người B phụ trách thao tác, Người C vẫn giữ mạch nói |
| 52 | Hạn chế của đồ án | Dataset nhỏ, ít variant, chỉ Gemini, 9x9 còn ít puzzle |
| 53 | Hướng phát triển | Thêm puzzle/model/variant, hướng neuro-symbolic/tool-use |
| 54 | Kết luận | Chốt thông điệp chính |
| 55 | Thank you | Kết thúc và mời hỏi đáp |

### Ý Chính Cần Chốt

- 9x9 là phần phân tách model rõ nhất:
  - Single-prompt 9x9: chỉ Gemini 3.5 Flash giải được 1/2.
  - Multi-step 9x9: Gemini 2.5 Pro và Gemini 3.5 Flash đạt 2/2.
  - Gemini 2.5 Flash và Gemini 3.1 Flash Lite bị kẹt ở No Certain Move.
- Multi-step không chỉ để tăng solve rate mà còn giúp biết model đi được bao xa trước khi fail.
- Error analysis là điểm quan trọng để bài không chỉ là “gọi API lấy kết quả”.
- Kết quả nhóm khớp tinh thần paper:
  - puzzle lớn hơn khó hơn;
  - reasoning tự nhiên không đảm bảo đúng;
  - cần validator và log;
  - multi-step giúp quan sát quá trình suy luận.
- Demo chỉ cần minh họa trực quan: board cập nhật từng bước, reasoning bên cạnh, trạng thái success/fail.

## Slide Có Thể Nói Nhanh Hoặc Để Backup Khi Thiếu Thời Gian

Các slide này vẫn hữu ích, nhưng không nhất thiết phải nói kỹ trong mạch chính:

- Slide 13. Sudoku variants
- Slide 16. Break-in
- Slide 33. Nhận xét single-prompt
- Slide 37. Kết quả multi-step hiện tại
- Slide 43. Ví dụ single-prompt fail
- Slide 46. Error type theo paper
- Slide 50. So sánh với paper gốc

---