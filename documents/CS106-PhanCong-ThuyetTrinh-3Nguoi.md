# Phân Công Thuyết Trình 3 Người - CS106 Sudoku-Bench

File này chia nội dung theo thứ tự slide trong `CS106-NoiDung-Slide-BaoCao.md`.

Nguyên tắc chia:

- Mỗi người nói một đoạn liên tục, tránh lên xuống nhiều lần.
- Người phụ trách demo và 6x6 sẽ nhận phần pipeline + kết quả 6x6 + demo.
- Người phụ trách 9x9 sẽ nhận phần kết quả 9x9 + phân tích + kết luận.
- Tổng thời lượng mục tiêu: 20-25 phút, gồm slide + demo.

---

## Tổng Quan Phân Công

| Người | Phạm vi slide | Vai trò chính | Thời lượng gợi ý |
|---|---:|---|---:|
| Người A | Slide 1-16 | Mở bài, paper, lý thuyết, thiết kế benchmark | 7-8 phút |
| Người B | Slide 17-28, 37-40 | Pipeline, dataset, single/multi, 6x6, demo | 8-10 phút |
| Người C | Slide 29-36, 41-44 | 9x9, phân tích lỗi, so sánh paper, hạn chế, kết luận | 7-8 phút |

Backup slide dùng khi vấn đáp, không cần đưa vào mạch nói chính trừ khi còn thời gian.

---

## Người A - Mở Bài, Paper Và Lý Thuyết

**Phạm vi chính: Slide 1-16**

### Slide phụ trách

| Slide | Tiêu đề | Ghi chú |
|---:|---|---|
| 1 | Trang Bìa | Giới thiệu đề tài, nhóm, paper tham chiếu |
| 2 | Table Of Contents | Nói nhanh cấu trúc bài |
| 3 | Vấn Đề Nghiên Cứu | Đặt vấn đề: LLM có thật sự suy luận logic không |
| 4 | Câu Hỏi Nghiên Cứu | Nêu các câu hỏi nhóm kiểm tra |
| 5 | Paper Tham Chiếu | Giới thiệu Sudoku-Bench |
| 6 | Vì Sao Chọn Sudoku-Bench? | Liên hệ yêu cầu môn học và paper |
| 7 | Constraint Reasoning Trong Sudoku-Bench | Nói rõ nhóm không làm CSP solver, chỉ dùng góc nhìn ràng buộc |
| 8 | Dataset Và Text Representation Của Paper | Giải thích paper chuẩn hóa puzzle thành text |
| 9 | Sudoku Variants | Giải thích variant và luật bổ sung |
| 10 | Killer Sudoku | Giới thiệu variant nhóm chọn |
| 11 | Break-In | Giải thích điểm mở khóa lời giải |
| 12 | Vì Sao Sudoku Variants Khó Với LLM? | Nêu khó khăn với LLM |
| 13 | Thiết Kế Đánh Giá Của Paper | Single-shot vs multi-step |
| 14 | Chỉ Số Đánh Giá | Solve rate, correct placements, error type |
| 15 | Phạm Vi Tái Hiện Của Nhóm | Nhóm tái hiện rút gọn thế nào |
| 16 | Vì Sao Không Chạy Toàn Bộ Benchmark? | Giải thích chi phí/thời gian |

### Mục tiêu phần nói

Người A cần làm rõ:

- Nhóm chọn một paper cụ thể: **Sudoku-Bench: Evaluating Creative Reasoning with Sudoku Variants**.
- Trọng tâm không phải xây thuật toán CSP truyền thống.
- Trọng tâm là tái hiện cách paper dùng Sudoku variants để benchmark reasoning của LLM.
- Paper đánh giá bằng hai mode: single-shot và multi-step.
- Nhóm tái hiện rút gọn: Killer Sudoku, 6x6/9x9, 4 model Gemini.

### Câu chuyển cho Người B

> Sau khi đã nắm paper đánh giá như thế nào và nhóm tái hiện trong phạm vi nào, phần tiếp theo sẽ trình bày pipeline thực nghiệm cụ thể của nhóm: dữ liệu được lưu ra sao, prompt được tạo thế nào, model được gọi thế nào và validator kiểm tra kết quả như thế nào.

---

## Người B - Pipeline, 6x6 Và Demo

**Phạm vi chính: Slide 17-28 và Slide 37-40**

Người B là người phụ trách chính phần demo và 6x6.

### Slide phụ trách

| Slide | Tiêu đề | Ghi chú |
|---:|---|---|
| 17 | Dataset | Giải thích JSON puzzle, solution, cages |
| 18 | Pipeline Tổng Quát | Luồng Puzzle JSON -> LLM -> Validator -> Evaluation |
| 19 | Single-Prompt Evaluation | Cách gọi model giải một lần |
| 20 | Multi-Step Evaluation | Cách model đi từng bước |
| 21 | Định Dạng Output Multi-Step | JSON output của một bước |
| 22 | Killer Sudoku Cheat Sheet | Cheat sheet là context, không phải solver |
| 23 | Validator | Vì sao cần kiểm chứng bằng solution |
| 24 | Kết Quả Single-Prompt 6x6 Hiện Tại | Bảng kết quả 6x6 single |
| 25 | Chi Tiết Single-Prompt 6x6 | Có thể nói nhanh hoặc bỏ nếu thiếu thời gian |
| 27 | Kết Quả Multi-Step 6x6 Hiện Tại | Bảng kết quả 6x6 multi |
| 28 | Chi Tiết Multi-Step 6x6 | Có thể nói nhanh hoặc bỏ nếu thiếu thời gian |
| 37 | Demo Pipeline | Kịch bản demo |
| 38 | Demo Single-Prompt | Demo output single-prompt |
| 39 | Demo Multi-Step | Demo log từng bước |
| 40 | Nếu Demo Trực Tiếp Gặp Lỗi | Phương án dự phòng |

### Mục tiêu phần nói

Người B cần làm rõ:

- Dataset của nhóm có ground truth, nên kết quả không đánh giá cảm tính.
- Single-prompt ít tốn chi phí nhưng khó phân tích lỗi.
- Multi-step tốn nhiều lượt gọi hơn nhưng có log reasoning từng bước.
- Validator không giúp model suy nghĩ, chỉ kiểm tra đúng/sai.
- Cheat sheet không cho đáp án, chỉ cung cấp tổ hợp cage hợp lệ.
- Kết quả 6x6:
  - Gemini 2.5 Pro và Gemini 3.5 Flash đạt 5/5 ở single-prompt.
  - Gemini 3.5 Flash đạt 5/5 ở multi-step.
  - Gemini 3.1 Flash Lite fail toàn bộ, dùng được như baseline yếu.
- Demo nên ưu tiên replay output/log đã lưu, không gọi API lại toàn bộ.

### Gợi ý nếu thiếu thời gian

Nếu bị thiếu thời gian, Người B có thể:

- Gộp Slide 19-21 thành một đoạn nói ngắn.
- Bỏ Slide 25 và Slide 28 khỏi phần trình bày chính, chỉ để backup.
- Demo tập trung vào một log multi-step thành công thay vì mở quá nhiều file.

### Câu chuyển cho Người C

> Ở 6x6, các model mạnh đã giải khá tốt, nên phần tiếp theo sẽ quan trọng hơn: khi tăng lên 9x9 hard, single-prompt và multi-step khác nhau rõ rệt như thế nào, và kết quả đó nói gì về khả năng reasoning của LLM.

---

## Người C - 9x9, Phân Tích Và Kết Luận

**Phạm vi chính: Slide 26, 29-36, 41-44**

Người C là người phụ trách chính phần 9x9.

### Slide phụ trách

| Slide | Tiêu đề | Ghi chú |
|---:|---|---|
| 26 | Kết Quả Single-Prompt 9x9 | Nói single-prompt 9x9 hầu hết fail |
| 29 | Kết Quả Multi-Step 9x9 | Nói kết quả 9x9 multi-step cuối |
| 30 | So Sánh Single-Prompt Và Multi-Step | Bảng tổng hợp 6x6/9x9 |
| 31 | Ví Dụ Single-Prompt Fail | Có thể nói nhanh nếu còn thời gian |
| 32 | Ví Dụ Multi-Step Thành Công | Case reasoning đúng |
| 33 | Phân Tích Lỗi | Incorrect Solution, No Certain Move |
| 34 | Vì Sao 9x9 Khó Hơn? | Giải thích vì sao 9x9 phân tách model tốt hơn |
| 35 | Nhận Định Từ Kết Quả Hiện Tại | Tổng hợp insight |
| 36 | So Sánh Với Paper Gốc | Liên hệ lại paper |
| 41 | Đóng Góp Của Nhóm | Tóm lại nhóm đã làm gì |
| 42 | Hạn Chế Của Đồ Án | Nói rõ phạm vi rút gọn |
| 43 | Hướng Phát Triển | Mở rộng dataset/model/variant |
| 44 | Kết Luận | Chốt thông điệp |

### Mục tiêu phần nói

Người C cần làm rõ:

- 9x9 là phần phân tách rõ nhất:
  - single-prompt 9x9: chỉ Gemini 3.5 Flash đạt 1/2;
  - multi-step 9x9: Gemini 2.5 Pro và Gemini 3.5 Flash đạt 2/2;
  - Gemini 2.5 Flash và Gemini 3.1 Flash Lite bị kẹt ở `No Certain Move`.
- Multi-step không chỉ để tăng solve rate, mà còn giúp phân tích model đi được bao xa qua `average correct placements`.
- Kết quả nhóm phù hợp tinh thần paper:
  - puzzle lớn khó hơn;
  - LLM có thể reasoning nghe hợp lý nhưng vẫn sai;
  - cần validator và error analysis.
- Hạn chế cần nói thẳng:
  - dataset nhỏ hơn paper;
  - chỉ tập trung Killer Sudoku;
  - chỉ dùng model Gemini;
  - 9x9 chỉ có 2 puzzle.
- Kết luận: nhóm đã tái hiện được thực nghiệm chính của paper trong phạm vi đồ án.

### Gợi ý nếu thiếu thời gian

Nếu bị thiếu thời gian, Người C có thể:

- Bỏ Slide 31 hoặc chỉ nói một câu: “single-prompt fail thì khó biết sai từ bước nào”.
- Gộp Slide 35 và Slide 36.
- Nói Slide 41-44 theo dạng chốt nhanh, mỗi slide khoảng 30-45 giây.

---

## Backup Slides Và Người Nên Trả Lời Khi Vấn Đáp

| Backup | Nội dung | Người trả lời chính |
|---|---|---|
| Backup 1 | Phân công thành viên | Người A |
| Backup 2 | Vì sao không chạy full benchmark | Người A hoặc C |
| Backup 3 | Multi-step có hỗ trợ AI quá nhiều không | Người B |
| Backup 4 | Vì sao dùng cheat sheet | Người B |
| Backup 5 | Kết quả 9x9 | Người C |
| Backup 6 | Câu hỏi vấn đáp nhanh | Tùy câu hỏi |

---

## Timeline Gợi Ý 20-25 Phút

| Mốc thời gian | Người | Nội dung |
|---:|---|---|
| 0:00-0:45 | A | Trang bìa, mục lục |
| 0:45-3:00 | A | Vấn đề nghiên cứu, câu hỏi nghiên cứu |
| 3:00-5:30 | A | Paper Sudoku-Bench, Sudoku variants, Killer Sudoku |
| 5:30-7:30 | A | Thiết kế đánh giá paper và phạm vi tái hiện |
| 7:30-10:30 | B | Dataset, pipeline, single/multi, validator |
| 10:30-13:30 | B | Kết quả 6x6 |
| 13:30-16:00 | B | Demo/replay log |
| 16:00-19:30 | C | Kết quả 9x9 và so sánh single/multi |
| 19:30-21:30 | C | Phân tích lỗi, vì sao 9x9 khó hơn |
| 21:30-23:30 | C | So sánh với paper, đóng góp, hạn chế |
| 23:30-25:00 | C | Hướng phát triển, kết luận |

Nếu chỉ có 20 phút:

- Người A rút còn 6 phút.
- Người B rút demo còn 2 phút.
- Người C gộp phân tích lỗi và so sánh paper còn 4-5 phút.

---

## Slide Nên Đưa Vào Backup Khi Làm Deck Chính

Nếu slide deck quá dài, nên đưa các slide sau xuống backup:

- Slide 25. Chi Tiết Single-Prompt 6x6
- Slide 28. Chi Tiết Multi-Step 6x6
- Slide 31. Ví Dụ Single-Prompt Fail
- Slide 40. Nếu Demo Trực Tiếp Gặp Lỗi

Các slide này vẫn hữu ích khi vấn đáp, nhưng không bắt buộc phải nói kỹ trong mạch chính.
