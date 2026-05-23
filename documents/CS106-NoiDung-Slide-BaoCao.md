# Nội Dung Slide Báo Cáo CS106 - Sudoku-Bench

File này là bản nội dung chi tiết để copy-paste vào Canva/PowerPoint.  
Không có phần lời thoại. Nếu một slide quá dài, có thể tự tách thành 2 slide cùng tiêu đề.

Quy định mới:

- 20-25 phút trình bày slide + demo.
- 5-10 phút vấn đáp.
- Nếu demo/thực nghiệm chưa hoàn tất, có thể quay video bổ sung trước 21/06.
- Sau báo cáo, nhóm chỉnh slide/demo theo góp ý của GV và nộp lại trước 21/06.

Ghi chú trạng thái kết quả:

- Benchmark 6x6 hiện có 5 puzzle easy.
- Nhóm đã mở rộng benchmark 6x6 sang 4 model:
  - Gemini 2.5 Flash;
  - Gemini 2.5 Pro;
  - Gemini 3.1 Flash Lite;
  - Gemini 3.5 Flash.
- 6x6 đã có output single-prompt và multi-step cho nhóm Gemini 2.5 và Gemini 3.x.
- 9x9 hiện có 2 puzzle hard; pipeline 9x9 đã tách riêng ở `cs106/9x9`.
- 9x9 đã có một kết quả thành công ban đầu: Gemini 2.5 Pro giải thành công puzzle 06 bằng multi-step.
- Các lượt 9x9 còn lại đang tiếp tục chạy vì mỗi lượt benchmark 4 model trên 2 map tốn nhiều thời gian.
- Kết quả Gemini 3.5 Flash single-prompt 6x6 đã được cập nhật đúng thư mục và đạt 5/5.

---

# Slide 1. Trang Bìa

**ĐÁNH GIÁ KHẢ NĂNG SUY LUẬN VÀ GIẢI QUYẾT BÀI TOÁN THỎA MÃN RÀNG BUỘC (CSP) CỦA LLM THÔNG QUA SUDOKU-BENCH**

Môn học: CS106 - Trí tuệ nhân tạo  
Giảng viên hướng dẫn: Lương Ngọc Hoàng  
Nhóm thực hiện: Nhóm 4  
Thời gian thực hiện: 05/2026

Thành viên:

- Đặng Anh Khoa
- Phạm Minh Bảo Khang
- Nguyễn Khang Hy
- Phan Công Nam

Media:

- Logo UIT.
- Nền lưới Sudoku/Killer Sudoku.
- Có thể thêm ảnh minh họa cage Sudoku mờ phía sau.

---

# Slide 2. Table Of Contents

**Nội dung trình bày theo các phần lớn**

1. **Vấn đề nghiên cứu và paper tham chiếu**
   - Vấn Đề Nghiên Cứu
   - Câu Hỏi Nghiên Cứu
   - Paper Tham Chiếu
   - Vì Sao Chọn Sudoku-Bench?

2. **Cơ sở lý thuyết**
   - CSP Là Gì?
   - Sudoku Dưới Góc Nhìn CSP
   - Sudoku Variants
   - Killer Sudoku
   - Break-In
   - Vì Sao CSP Khó Với LLM?

3. **Thiết kế đánh giá và phạm vi tái hiện**
   - Thiết Kế Đánh Giá Của Paper
   - Chỉ Số Đánh Giá
   - Phạm Vi Tái Hiện Của Nhóm
   - Vì Sao Không Chạy Toàn Bộ Benchmark?

4. **Pipeline thực nghiệm của nhóm**
   - Dataset
   - Pipeline Tổng Quát
   - Single-Prompt Evaluation
   - Multi-Step Evaluation
   - Định Dạng Output Multi-Step
   - Killer Sudoku Cheat Sheet
   - Validator

5. **Kết quả và phân tích**
   - Kết Quả Single-Prompt 6x6 Hiện Tại
   - Chi Tiết Single-Prompt 6x6
   - Trạng Thái 9x9 Hiện Tại
   - Kết Quả Multi-Step 6x6 Hiện Tại
   - Chi Tiết Multi-Step 6x6
   - Kết Quả 9x9 Multi-Step Ban Đầu
   - So Sánh Single-Prompt Và Multi-Step
   - Ví Dụ Single-Prompt Fail
   - Ví Dụ Multi-Step Thành Công
   - Phân Tích Lỗi
   - Vì Sao 9x9 Khó Hơn?
   - So Sánh Với Paper Gốc

6. **Demo, kết luận và hướng phát triển**
   - Demo Pipeline
   - Demo Single-Prompt
   - Demo Multi-Step
   - Nếu Demo Trực Tiếp Gặp Lỗi
   - Đóng Góp Của Nhóm
   - Hạn Chế Của Đồ Án
   - Hướng Phát Triển
   - Kết Luận

Media:

- Dùng timeline ngang 6 phần theo đúng thứ tự ở trên.
- Có thể đặt icon cho từng phần: research question, theory, benchmark design, pipeline, results, demo/conclusion.

---

# Slide 3. Vấn Đề Nghiên Cứu

**LLM có thật sự suy luận logic, hay chỉ đang nhận diện mẫu?**

Các mô hình ngôn ngữ lớn hiện nay thể hiện năng lực rất mạnh trong nhiều tác vụ:

- trả lời câu hỏi tự nhiên;
- sinh văn bản;
- hỗ trợ lập trình;
- giải thích kiến thức;
- thực hiện các bài toán ngắn có dạng quen thuộc.

Tuy nhiên, với các bài toán logic có ràng buộc chặt, yêu cầu không chỉ là "nghe hợp lý" mà phải **đúng tuyệt đối**.

Trong bài toán CSP:

- mỗi bước đi phải thỏa tất cả ràng buộc liên quan;
- một lựa chọn sai có thể làm toàn bộ trạng thái sau đó sai;
- lời giải cuối cùng cần được kiểm tra bằng nghiệm chuẩn;
- reasoning bằng ngôn ngữ tự nhiên chưa đủ để đảm bảo đáp án đúng.

Thông điệp của slide:

> LLM có thể giải thích rất thuyết phục, nhưng bài toán ràng buộc cần một cơ chế kiểm chứng hình thức.

Media:

| Pattern Matching | Constraint Reasoning |
|---|---|
| Dựa vào mẫu quen thuộc | Dựa vào luật và ràng buộc |
| Câu trả lời có thể nghe hợp lý | Câu trả lời phải đúng hình thức |
| Khó phát hiện sai nếu không có ground truth | Có thể validate tự động |
| Phù hợp với tác vụ ngôn ngữ | Phù hợp với CSP, Sudoku, lập lịch |

---

# Slide 4. Câu Hỏi Nghiên Cứu

**Nhóm tập trung trả lời các câu hỏi sau**

1. LLM có thể đọc hiểu và áp dụng luật của Sudoku variants không?
2. LLM có duy trì được tính nhất quán toàn cục khi có nhiều ràng buộc giao nhau không?
3. Single-prompt và multi-step khác nhau như thế nào về kết quả và khả năng phân tích lỗi?
4. Khi tăng kích thước từ 6x6 lên 9x9, độ khó và chi phí thay đổi ra sao?
5. Việc bổ sung prompt context như Killer Sudoku cheat sheet có giúp mô hình ổn định hơn không?

Kỳ vọng của nhóm:

- Không chỉ chạy LLM để lấy đáp án.
- Cần có pipeline tự động để đọc đề, gọi model, parse kết quả và validate.
- Cần có log để biết mô hình sai ở đâu, thay vì chỉ biết đáp án cuối đúng hay sai.

Media:

Checklist 5 câu hỏi nghiên cứu.

---

# Slide 5. Paper Tham Chiếu

**Paper gốc: Sudoku-Bench**

**Sudoku-Bench: Evaluating Creative Reasoning with Sudoku Variants**  
Sakana AI, 2025

Mục tiêu của paper:

- đánh giá năng lực creative reasoning của LLM;
- dùng Sudoku variants thay vì Sudoku chuẩn;
- yêu cầu mô hình đọc luật mới và áp dụng vào từng puzzle;
- giảm khả năng mô hình chỉ dựa vào mẫu Sudoku quen thuộc;
- đánh giá bằng nghiệm chuẩn và phân tích lỗi.

Điểm quan trọng:

- Paper không chỉ hỏi "model có trả lời được không?".
- Paper kiểm tra việc mô hình có thể **suy luận dưới các ràng buộc mới** hay không.
- Sudoku variants có vai trò như một môi trường kiểm tra reasoning có luật rõ ràng.

Media:

- Ảnh trang đầu paper.
- Ảnh trích từ paper:
  - ![Paper title / Sakana AI](paper-assets/paper-page-01-image-01.png)
- Citation box:

```text
Sudoku-Bench: Evaluating Creative Reasoning with Sudoku Variants
Sakana AI, 2025
```

---

# Slide 6. Vì Sao Chọn Sudoku-Bench?

**Sudoku-Bench phù hợp với yêu cầu đồ án CS106**

Lý do chọn:

- Có bài báo khoa học cụ thể làm reference.
- Có liên hệ trực tiếp với bài toán CSP trong Trí tuệ nhân tạo.
- Có thực nghiệm rõ ràng để tái hiện một phần.
- Có thể xây dựng pipeline đánh giá tự động.
- Có thể phân tích lỗi của LLM dựa trên ground truth.

Điểm mạnh của Sudoku variants:

- luật chơi rõ ràng;
- nghiệm có thể kiểm chứng;
- không gian ràng buộc phong phú;
- dễ minh họa trong slide và demo;
- phù hợp để so sánh single-prompt và multi-step.

Thông điệp:

> Sudoku-Bench là cầu nối tốt giữa lý thuyết CSP và đánh giá thực nghiệm LLM.

---

# Slide 7. CSP Là Gì?

**Constraint Satisfaction Problem (CSP)**

Một CSP gồm ba thành phần:

- **Variables (X):** tập các biến cần gán giá trị.
- **Domains (D):** miền giá trị hợp lệ của từng biến.
- **Constraints (C):** tập ràng buộc giữa các biến.

Mục tiêu:

> Tìm một phép gán giá trị cho toàn bộ biến sao cho mọi ràng buộc đều được thỏa mãn.

Ví dụ CSP trong thực tế:

- Sudoku;
- lập lịch thi;
- tô màu bản đồ;
- phân công tài nguyên;
- định tuyến có ràng buộc.

Biểu diễn ngắn gọn:

```text
CSP = <X, D, C>
```

Media:

Sơ đồ 3 khối:

```text
Variables  ->  Domains  ->  Constraints
       \           |           /
        \          |          /
         Valid Assignment
```

---

# Slide 8. Sudoku Dưới Góc Nhìn CSP

**Mô hình hóa Sudoku thành CSP**

Trong Sudoku:

- mỗi ô trên bảng là một biến;
- miền giá trị là các chữ số hợp lệ;
- các ràng buộc đảm bảo không có số lặp trong các vùng liên quan.

Với từng kích thước:

| Kích thước | Số ô | Miền giá trị |
|---:|---:|---|
| 4x4 | 16 | 1-4 |
| 6x6 | 36 | 1-6 |
| 9x9 | 81 | 1-9 |

Ràng buộc Sudoku chuẩn:

- mỗi hàng chứa các số không lặp;
- mỗi cột chứa các số không lặp;
- mỗi khối con chứa các số không lặp.

Ý nghĩa đối với LLM:

- Mô hình phải ghi nhớ trạng thái toàn bảng.
- Mô hình phải kiểm tra nhiều ràng buộc trước khi điền một ô.
- Một ô có thể chịu ảnh hưởng đồng thời từ hàng, cột, khối và luật phụ.

Media:

- Lưới Sudoku 6x6 hoặc 9x9.
- Highlight một hàng, một cột, một block.
- Có thể dùng ảnh text-representation từ paper nếu muốn nối sang phần benchmark:
  - ![Figure 3 - Text representation example](paper-assets/paper-page-07-image-01.jpg)

---

# Slide 9. Sudoku Variants

**Sudoku variants thêm ràng buộc mới vào Sudoku chuẩn**

Một số biến thể phổ biến:

| Variant | Ràng buộc bổ sung |
|---|---|
| Knight's Move | Các ô cách nhau như nước đi quân mã không được trùng số |
| Arrow | Tổng các ô trên thân mũi tên bằng số ở vòng tròn gốc |
| Thermometer | Các số tăng dần dọc theo nhiệt kế |
| Killer Cage | Tổng các ô trong cage bằng một giá trị cho trước |

Vì sao variants khó hơn Sudoku chuẩn?

- Một ô chịu nhiều loại ràng buộc cùng lúc.
- Có nhiều ràng buộc cục bộ nhưng ảnh hưởng toàn cục.
- Bước đầu không phải lúc nào cũng hiển nhiên.
- Cần tìm "điểm mở khóa" để bắt đầu suy luận.

Thông điệp:

> Sudoku variants làm lộ rõ hơn năng lực suy luận ràng buộc của mô hình.

Media:

- Ảnh Figure 1 từ paper, minh họa nhiều Sudoku variants có luật riêng:
  - ![Figure 1 example 1](paper-assets/paper-page-02-image-01.jpg)
  - ![Figure 1 example 2](paper-assets/paper-page-02-image-02.jpg)
  - ![Figure 1 example 3](paper-assets/paper-page-02-image-03.jpg)
  - ![Figure 1 example 4](paper-assets/paper-page-02-image-04.jpg)
  - ![Figure 1 example 5](paper-assets/paper-page-02-image-05.jpg)

Gợi ý dùng trong slide:

- Chọn 2-3 ảnh nổi bật, không cần đưa cả 5 ảnh lên cùng một slide.
- Caption: "Figure 1 trong paper: mỗi Sudoku variant có một bộ luật riêng được mô tả bằng ngôn ngữ tự nhiên."

---

# Slide 10. Killer Sudoku

**Biến thể nhóm chọn: Killer Sudoku**

Killer Sudoku = Sudoku chuẩn + ràng buộc cage.

Mỗi cage gồm:

- một nhóm ô;
- một tổng mục tiêu;
- điều kiện tổng các ô bằng tổng mục tiêu;
- điều kiện các số trong cage không được lặp.

Ví dụ:

```text
Cage: r1c1 + r2c1 = 3
Digits allowed in 6x6: 1..6
Possible combination: {1,2}
```

Tuy nhiên:

- biết cage là `{1,2}` chưa đủ;
- cần xác định ô nào là 1, ô nào là 2;
- phải kết hợp với hàng, cột, khối và các cage khác.

Media:

- Hình một bảng Killer Sudoku.
- Highlight một cage và ghi target sum.
- Có thể dùng ảnh Figure 5 trong paper nếu muốn minh họa puzzle 6x6:
  - ![Figure 5 - Sumthings 6x6 example](paper-assets/paper-page-10-image-01.jpg)

---

# Slide 11. Break-In

**Break-in: điểm mở khóa lời giải**

Trong nhiều Sudoku variants:

- không thể bắt đầu bằng cách nhìn một ô đơn giản;
- cần phát hiện một ràng buộc then chốt;
- sau bước mở khóa, các ràng buộc khác bắt đầu lan truyền;
- người giải phải biết nên bắt đầu từ đâu.

Break-in trong bối cảnh LLM:

- kiểm tra khả năng chọn hướng suy luận;
- kiểm tra khả năng kết hợp nhiều luật;
- kiểm tra việc mô hình có thể tạo ra một bước đi chắc chắn thay vì đoán.

Flow:

```text
Puzzle ban đầu
    ↓
Nhiều khả năng còn mở
    ↓
Tìm break-in
    ↓
Thu hẹp ứng viên
    ↓
Điền các ô tiếp theo
```

Media:

- Ảnh Figure 2 từ paper về puzzle Ascension và break-in:
  - ![Figure 2a - Ascension initial board](paper-assets/paper-page-04-image-01.jpg)
  - ![Figure 2b - Ascension highlighted constraints](paper-assets/paper-page-04-image-02.jpg)
  - ![Figure 2c - Ascension intermediate reasoning](paper-assets/paper-page-04-image-03.jpg)
  - ![Figure 2d - Ascension break-in conclusion](paper-assets/paper-page-04-image-04.jpg)
- Gợi ý dùng 2 ảnh: initial board và highlighted/break-in board.
- Caption: "Figure 2 trong paper: ví dụ break-in từ puzzle Ascension."

---

# Slide 12. Vì Sao CSP Khó Với LLM?

**Những hạn chế thường gặp của LLM khi giải CSP**

1. **Khó duy trì trạng thái toàn cục**
   - Board có nhiều ô.
   - Mỗi ô liên quan tới nhiều ràng buộc.
   - Context dài dễ làm mô hình bỏ sót thông tin.

2. **Khó quay lui**
   - LLM sinh câu trả lời tuần tự.
   - Khi đã chọn sai, các bước sau dễ dựa trên trạng thái sai.

3. **Reasoning tự nhiên không đảm bảo đúng hình thức**
   - Lời giải thích có thể nghe hợp lý.
   - Nhưng chỉ cần sai một ràng buộc là đáp án fail.

4. **Dễ nhầm giữa "có thể" và "bắt buộc"**
   - Một giá trị là ứng viên chưa chắc là đáp án.
   - CSP yêu cầu bước đi phải được chứng minh chắc chắn.

Thông điệp:

> Với CSP, validator quan trọng không kém prompt.

---

# Slide 13. Thiết Kế Đánh Giá Của Paper

**Hai chế độ đánh giá chính**

| Tiêu chí | Single-shot / Single-prompt | Multi-step |
|---|---|---|
| Cách gọi model | Một lần cho toàn bộ puzzle | Nhiều vòng tương tác |
| Output | Grid hoàn chỉnh | Một bước đi mỗi vòng |
| Chi phí API | Thấp hơn | Cao hơn nhiều |
| Phân tích quá trình | Hạn chế | Chi tiết hơn |
| Biết bước sai đầu tiên | Khó | Có |

Single-shot phù hợp để kiểm tra:

- khả năng giải trực tiếp;
- chất lượng prompt tổng quát;
- chi phí thấp.

Multi-step phù hợp để kiểm tra:

- quá trình suy luận;
- khả năng duy trì trạng thái;
- lỗi xuất hiện ở bước nào.

Media:

- Có thể chèn bảng leaderboard của paper để minh họa cách paper báo cáo multi-step và single-shot:
  - trích nội dung từ `documents/paper.md`, đoạn Table 1.
- Nếu muốn dùng ảnh trực tiếp từ paper, chụp/cắt trang chứa Table 1 từ PDF.
- Caption gợi ý: "Paper đánh giá bằng cả multi-step solve rate và single-shot solve rate, phân theo kích thước puzzle."

---

# Slide 14. Chỉ Số Đánh Giá

**Các chỉ số nhóm sử dụng**

1. **Solve Rate**
   - Tỷ lệ puzzle được giải đúng hoàn toàn.

2. **Final Status**
   - Success hoặc Failed.

3. **Error Type**
   - Incorrect Solution;
   - Surrender;
   - Claimed Contradiction;
   - Missing Information.

4. **Number of Steps**
   - Áp dụng cho multi-step.
   - Cho biết mô hình đi được bao lâu trước khi thành công hoặc thất bại.

5. **Execution Time**
   - Áp dụng cho single-prompt output.
   - Cho biết thời gian gọi API và xử lý.

6. **Execution Log**
   - Lưu reasoning, ô được chọn, giá trị điền và board state.

Media:

- Có thể dùng Figure 4 từ paper để minh họa error categorization trong single-shot:
  - ![Figure 4 - Response categorization](paper-assets/paper-page-09-image-01.png)
- Caption: "Figure 4 trong paper: phân loại phản hồi ở single-shot theo đúng/sai và loại lỗi."

---

# Slide 15. Phạm Vi Tái Hiện Của Nhóm

**Nhóm tái hiện rút gọn Sudoku-Bench**

Nhóm không tái hiện toàn bộ benchmark gốc, mà tập trung vào phạm vi phù hợp với đồ án:

- biến thể chính: **Killer Sudoku**;
- model benchmark hiện tại:
  - Gemini 2.5 Flash;
  - Gemini 2.5 Pro;
  - Gemini 3.1 Flash Lite;
  - Gemini 3.5 Flash;
- chế độ đánh giá:
  - single-prompt;
  - multi-step;
- dataset hiện tại:
  - 5 puzzle 6x6 easy;
  - 2 puzzle 9x9 hard;
- 6x6 đã chạy trên 4 model với cả single-prompt và multi-step;
- 9x9 đã có pipeline riêng và đang tiếp tục benchmark;
- 9x9 hiện đã có một run thành công trên Gemini 2.5 Pro với puzzle 06.

Lý do chọn phạm vi rút gọn:

- giới hạn thời gian;
- giới hạn chi phí API;
- multi-step cần rất nhiều lượt gọi model, đặc biệt khi mở rộng lên 4 model và 2 map 9x9;
- đồ án yêu cầu có thực nghiệm, không bắt buộc tái hiện 100% paper.

---

# Slide 16. Vì Sao Không Chạy Toàn Bộ Benchmark?

**Chi phí multi-step tăng rất nhanh**

Trong multi-step hiện tại:

- mỗi ô thường có 2 lượt gọi LLM:
  - một lượt analysis;
  - một lượt fill;
- nếu điền sai thì dừng;
- nếu điền đúng đến cuối, số lượt gọi tăng theo số ô.

Ước lượng:

| Kích thước | Số ô | Số lượt gọi tối đa |
|---:|---:|---:|
| 6x6 | 36 | 72 |
| 9x9 | 81 | 162 |

Nếu chạy nhiều puzzle và nhiều model:

```text
Tổng chi phí ≈ số puzzle × số model × số ô × 2 lượt gọi
```

Kết luận:

> Nhóm ưu tiên chạy tập nhỏ nhưng có log, validator và phân tích rõ.

---

# Slide 17. Dataset

**Cấu trúc dữ liệu đầu vào**

Mỗi puzzle được lưu trong file JSON:

```json
{
  "id": 1,
  "difficulty": "easy",
  "grid_size": 6,
  "puzzle": [[0,0,0,0,0,0], ...],
  "solution": [[1,3,5,2,6,4], ...],
  "cages": [
    {"cells": [[0,0],[1,0]], "sum": 3}
  ]
}
```

Ý nghĩa các trường:

| Trường | Ý nghĩa |
|---|---|
| `id` | mã puzzle |
| `difficulty` | độ khó |
| `grid_size` | kích thước lưới |
| `puzzle` | board ban đầu |
| `solution` | nghiệm chuẩn |
| `cages` | danh sách cage và tổng mục tiêu |

Dataset hiện tại:

| Puzzle | Size | Difficulty |
|---:|---:|---|
| 1-5 | 6x6 | easy |
| 6-7 | 9x9 | hard |

---

# Slide 18. Pipeline Tổng Quát

**Pipeline đánh giá tự động**

```text
Puzzle JSON
    ↓
Prompt Builder
    ↓
Gemini API
    ↓
JSON Parser
    ↓
Validator
    ↓
Result Log
    ↓
Analysis / Chart
```

Các thành phần:

- **Data Loader:** đọc puzzle, solution và cages.
- **Prompt Builder:** tạo prompt từ luật, board, cages và cheat sheet.
- **LLM API:** gọi các model Gemini 2.5 và Gemini 3.x.
- **Parser:** trích output JSON từ phản hồi.
- **Validator:** so sánh với nghiệm chuẩn.
- **Logger:** lưu từng bước để phân tích.

Thông điệp:

> Pipeline biến phản hồi ngôn ngữ tự nhiên của LLM thành kết quả có thể kiểm chứng.

---

# Slide 19. Single-Prompt Evaluation

**Cách đánh giá single-prompt**

Input cho model:

- luật Sudoku chuẩn;
- luật Killer Sudoku;
- board ban đầu;
- danh sách cages;
- cheat sheet các tổ hợp Killer cage;
- yêu cầu trả về grid hoàn chỉnh.

Output mong muốn:

- một bảng hoàn chỉnh;
- đúng định dạng để parser đọc;
- tất cả ô phải khớp nghiệm chuẩn.

Ưu điểm:

- ít lượt gọi API;
- dễ chạy cho nhiều puzzle;
- phù hợp để có baseline nhanh.

Hạn chế:

- khó biết mô hình sai từ bước nào;
- nếu grid cuối sai, cần phân tích thủ công nhiều hơn;
- mô hình có thể đưa ra lời giải gần đúng nhưng vẫn fail.

---

# Slide 20. Multi-Step Evaluation

**Cách đánh giá multi-step**

Mỗi vòng gồm hai giai đoạn:

1. **Analysis**
   - Mô hình phân tích trạng thái hiện tại.
   - Xem xét luật Sudoku, cage, các ô đã điền.

2. **Fill**
   - Mô hình chọn đúng một ô để điền.
   - Trả về cell, value, reasoning và độ chắc chắn.

Sau mỗi bước fill:

- board được cập nhật;
- validator kiểm tra ngay;
- nếu đúng thì tiếp tục;
- nếu sai thì dừng phiên chạy.

Luật quan trọng:

> Điền rồi không hoàn tác. Sai một ô là phiên chạy thất bại.

---

# Slide 21. Định Dạng Output Multi-Step

**Output JSON của bước Fill**

Ví dụ:

```json
{
  "cell": "r2c5",
  "value": 1,
  "reasoning": "The cage sum forces this cell to be 1.",
  "is_certain": true
}
```

Các trường chính:

| Trường | Ý nghĩa |
|---|---|
| `cell` | ô được chọn |
| `value` | giá trị điền |
| `reasoning` | lý do mô hình đưa ra |
| `is_certain` | mô hình có chắc chắn không |

Vì sao cần JSON:

- dễ parse tự động;
- tránh output lan man;
- dễ validate;
- dễ lưu log từng bước;
- dễ trích ví dụ cho phân tích lỗi.

---

# Slide 22. Killer Sudoku Cheat Sheet

**Cheat sheet trong prompt**

Cheat sheet cung cấp các tổ hợp cage hợp lệ.

Ví dụ:

```text
2-cell cage sum 3: {1,2}
2-cell cage sum 5: {1,4}, {2,3}
3-cell cage sum 6: {1,2,3}
```

Vai trò:

- giúp model giảm lỗi tính toán tổ hợp cơ bản;
- cung cấp context rõ hơn cho Killer Sudoku;
- hỗ trợ model tập trung vào việc kết hợp ràng buộc;
- không trực tiếp cho biết lời giải của puzzle.

Điểm cần nhấn mạnh:

> Cheat sheet không solve thay mô hình. Nó chỉ đưa các tổ hợp hợp lệ; mô hình vẫn phải suy luận ô nào nhận giá trị nào.

Trạng thái hiện tại:

- Cheat sheet 6x6 đã dùng trong benchmark 4 model.
- Cheat sheet/prompt 9x9 đã được tách riêng trong `cs106/9x9`.
- Run 9x9 đầu tiên trên Gemini 2.5 Pro đã giải thành công puzzle 06.
- Các run 9x9 còn lại đang tiếp tục chạy và sẽ cập nhật vào bảng kết quả cuối.

---

# Slide 23. Validator

**Validator là phần bắt buộc để tránh đánh giá cảm tính**

Validator kiểm tra:

- ô được chọn có hợp lệ không;
- giá trị có nằm trong miền không;
- giá trị có khớp nghiệm chuẩn không;
- board hiện tại có còn đúng không;
- grid cuối có hoàn toàn đúng không.

Với single-prompt:

- kiểm tra toàn bộ grid cuối;
- status = Success nếu prediction khớp solution.

Với multi-step:

- kiểm tra sau từng bước fill;
- nếu sai một ô thì dừng ngay;
- lưu error type và số bước đã đi.

Flow:

```text
Model Output
    ↓
Parse JSON
    ↓
Compare with Ground Truth
    ↓
Success / Failed
```

---

# Slide 24. Kết Quả Single-Prompt 6x6 Hiện Tại

**Single-prompt đã chạy trên 5 puzzle 6x6 easy**

| Model | Kết quả 6x6 | Solve rate | Ghi chú |
|---|---:|---:|---|
| Gemini 2.5 Flash | 4/5 solved | 80% | Sai puzzle 01 |
| Gemini 2.5 Pro | 5/5 solved | 100% | Đạt 100% ở single-prompt |
| Gemini 3.1 Flash Lite | 0/5 solved | 0% | Output hiện tại fail toàn bộ |
| Gemini 3.5 Flash | 5/5 solved | 100% | Cùng đạt 100% với Gemini 2.5 Pro |

Nhận xét chính:

- Gemini 2.5 Pro và Gemini 3.5 Flash cùng đạt kết quả tốt nhất ở single-prompt 6x6.
- Gemini 2.5 Flash vẫn giải được phần lớn puzzle 6x6 nhưng có một ca fail.
- Gemini 3.1 Flash Lite single-prompt chưa giải được puzzle nào trong output hiện tại.
- Single-prompt có chi phí thấp, nhưng khi fail thì khó biết mô hình sai ở bước suy luận nào.

---

# Slide 25. Chi Tiết Single-Prompt 6x6

**Kết quả single-prompt theo từng puzzle**

| Puzzle | Gemini 2.5 Flash | Gemini 2.5 Pro | Gemini 3.1 Flash Lite | Gemini 3.5 Flash |
|---:|---|---|---|---|
| 1 | Failed | Success | Failed | Success |
| 2 | Success | Success | Failed | Success |
| 3 | Success | Success | Failed | Success |
| 4 | Success | Success | Failed | Success |
| 5 | Success | Success | Failed | Success |

Solve rate:

```text
Gemini 2.5 Flash:      4/5 = 80%
Gemini 2.5 Pro:        5/5 = 100%
Gemini 3.1 Flash Lite: 0/5 = 0%
Gemini 3.5 Flash:      5/5 = 100%
```

Nhận xét:

- 6x6 là mức mà model mạnh có thể giải trực tiếp bằng single-prompt.
- Kết quả giữa các model khác biệt rõ rệt.
- Gemini 2.5 Pro và Gemini 3.5 Flash cùng đạt 5/5, cho thấy 6x6 easy có thể đã hơi dễ với model mạnh.
- Validator vẫn cần thiết vì có model trả về grid hoàn chỉnh nhưng sai nghiệm chuẩn.

---

# Slide 26. Trạng Thái 9x9 Hiện Tại

**9x9 đã chuyển từ "chưa ổn định" sang "đang benchmark có pipeline riêng"**

Pipeline 9x9 hiện nằm ở:

```text
cs106/9x9
```

Các file chính:

```text
cs106/9x9/api_llm_9x9.ipynb
cs106/9x9/analysis_template_9x9.md
cs106/9x9/killer_sudoku_cheat_sheet_9x9.md
```

Kết quả đã có:

| Puzzle | Model | Mode | Status | Steps |
|---:|---|---|---|---:|
| 6 | Gemini 2.5 Pro | Multi-step | Success | 83 |

Trạng thái đang cập nhật:

- 9x9 có 2 puzzle hard: puzzle 06 và puzzle 07.
- Các lượt benchmark 9x9 cho nhiều model đang tiếp tục chạy.
- Mỗi lượt chạy 4 model trên 2 map tốn nhiều thời gian, nên bảng 9x9 cuối sẽ cập nhật sau.

---

# Slide 27. Kết Quả Multi-Step 6x6 Hiện Tại

**Multi-step đã chạy trên 5 puzzle 6x6 easy**

| Model | Kết quả 6x6 | Solve rate | Ghi chú |
|---|---:|---:|---|
| Gemini 2.5 Flash | 4/5 solved | 80% | Fail puzzle 02 ở bước 5 |
| Gemini 2.5 Pro | 4/5 solved | 80% | Fail puzzle 05 ở bước 5 |
| Gemini 3.1 Flash Lite | 0/5 solved | 0% | Fail sớm hoặc giữa chừng |
| Gemini 3.5 Flash | 5/5 solved | 100% | Tốt nhất trong multi-step 6x6 hiện tại |

Nhận xét:

- Gemini 3.5 Flash multi-step đạt 5/5 trên 6x6.
- Gemini 2.5 Flash và Gemini 2.5 Pro đều đạt 4/5.
- Gemini 3.1 Flash Lite chưa giải được puzzle nào trong multi-step 6x6 hiện tại.
- Multi-step giúp thấy rõ số bước trước khi fail, nên hữu ích cho error analysis.

---

# Slide 28. Chi Tiết Multi-Step 6x6

**Kết quả multi-step theo từng puzzle**

| Puzzle | 2.5 Flash | 2.5 Pro | 3.1 Flash Lite | 3.5 Flash |
|---:|---|---|---|---|
| 1 | Success / 37 steps | Success / 36 steps | Failed / 14 steps | Success / 36 steps |
| 2 | Failed / 5 steps | Success / 36 steps | Failed / 13 steps | Success / 36 steps |
| 3 | Success / 36 steps | Success / 36 steps | Failed / 1 step | Success / 36 steps |
| 4 | Success / 36 steps | Success / 37 steps | Failed / 14 steps | Success / 36 steps |
| 5 | Success / 36 steps | Failed / 5 steps | Failed / 1 step | Success / 36 steps |

Solve rate:

```text
Gemini 2.5 Flash:      4/5 = 80%
Gemini 2.5 Pro:        4/5 = 80%
Gemini 3.1 Flash Lite: 0/5 = 0%
Gemini 3.5 Flash:      5/5 = 100%
```

Nhận xét:

- Khi success, số bước xấp xỉ số ô cần điền.
- Gemini 3.5 Flash là model multi-step 6x6 tốt nhất hiện tại.
- Gemini 3.1 Flash Lite thường fail sớm, cho thấy model yếu hơn hoặc prompt chưa phù hợp.
- Số bước trước khi fail là dữ liệu tốt để so sánh độ bền suy luận của model.

---

# Slide 29. Kết Quả 9x9 Multi-Step Ban Đầu

**Run 9x9 đầu tiên đã có kết quả thành công**

| Puzzle | Model | Status | Steps | Error type |
|---:|---|---|---:|---|
| 6 | Gemini 2.5 Pro | Success | 83 | None |

Ví dụ các bước đầu trong log:

```text
Step 1: r1c5 = 5
Reasoning: tổng hàng 1 là 45; các cage trong hàng đã chiếm 40; ô còn lại phải là 5.

Step 2: r2c5 = 2
Reasoning: cage r1c5 + r2c5 = 7; r1c5 = 5 nên r2c5 = 2.

Step 3: r1c4 = 9
Reasoning: kết hợp tổng box 2 và các tổ hợp cage để suy ra r1c4.
```

Nhận xét:

- Kết quả này cho thấy 9x9 không còn chỉ là fail trong cấu hình mới.
- Prompt/cheat sheet 9x9 mới có thể giúp model tìm được các bước suy luận chắc chắn.
- Tuy nhiên, mới chỉ có một run thành công; cần thêm kết quả trên puzzle 07 và các model khác trước khi kết luận rộng.

---

# Slide 30. So Sánh Single-Prompt Và Multi-Step

**So sánh kết quả 6x6 hiện tại**

| Model | Single-prompt 6x6 | Multi-step 6x6 | Nhận xét |
|---|---:|---:|---|
| Gemini 2.5 Flash | 4/5 | 4/5 | Hai mode tương đương về solve rate |
| Gemini 2.5 Pro | 5/5 | 4/5 | Single-prompt tốt hơn trong tập hiện tại |
| Gemini 3.1 Flash Lite | 0/5 | 0/5 | Chưa phù hợp với prompt hiện tại |
| Gemini 3.5 Flash | 5/5 | 5/5 | Ổn định nhất trong cả hai mode hiện tại |

Nhận xét:

- Multi-step không luôn vượt single-prompt, nhưng cho log chi tiết để phân tích lỗi.
- Với Gemini 3.5 Flash, cả single-prompt và multi-step đều đạt 5/5 trên 6x6.
- Với Gemini 2.5 Pro, single-prompt lại rất mạnh trên 6x6.
- Kết quả cho thấy prompt, mode đánh giá và model đều ảnh hưởng mạnh tới solve rate.

Kết luận tạm:

> Đánh giá LLM trên Sudoku variants cần so sánh theo cả model lẫn chế độ tương tác; chỉ nhìn một mode sẽ không đủ.

---

# Slide 31. Ví Dụ Single-Prompt Fail

**Ví dụ: Flash single-prompt fail ở puzzle 1**

Status:

```text
Model: gemini-2.5-flash
Puzzle: 1
Size: 6x6
Status: Failed
```

Ý nghĩa:

- Mô hình trả về một grid hoàn chỉnh.
- Grid có vẻ hợp lệ ở một số vùng.
- Nhưng khi so với nghiệm chuẩn, có ô sai.
- Vì Sudoku/Killer Sudoku yêu cầu đúng toàn bộ, chỉ một ô sai cũng tính là Failed.

Thông điệp:

> Với CSP, "gần đúng" vẫn là sai.

Nên minh họa:

- Bảng prediction của model.
- Bảng solution chuẩn.
- Highlight vị trí khác nhau.

---

# Slide 32. Ví Dụ Multi-Step Thành Công

**Ví dụ một bước reasoning đúng trong multi-step**

Từ log puzzle 1:

```text
Chosen cell: r2c5
Value: 1
```

Reasoning rút gọn:

```text
r1c5 and r1c6 must contain {4,6}.
The cage r1c5 + r1c6 + r2c5 has sum 11.
Therefore, r2c5 must be 1.
```

Điểm đáng chú ý:

- Mô hình dùng thông tin từ cage sum.
- Mô hình kết hợp với khả năng còn lại của hàng.
- Bước đi có lý do rõ ràng.
- Validator xác nhận giá trị đúng.

Ý nghĩa:

> Log multi-step cho phép quan sát reasoning cụ thể, không chỉ nhìn đáp án cuối.

---

# Slide 33. Phân Tích Lỗi

**Error type hiện tại**

Trong các log multi-step hiện tại, lỗi chính là:

```text
Incorrect Solution
```

Tức là:

- mô hình chọn một ô;
- điền một giá trị;
- giá trị đó không khớp nghiệm chuẩn;
- phiên chạy dừng ngay.

Các nguyên nhân có thể:

- bỏ sót một ràng buộc cage;
- bỏ sót ràng buộc hàng/cột/khối;
- nhầm giữa ứng viên có thể và giá trị bắt buộc;
- reasoning cục bộ đúng nhưng không đúng toàn cục;
- context quá dài làm mô hình mất thông tin.

Các loại lỗi theo paper:

| Error Type | Mô tả |
|---|---|
| Incorrect Solution | Lời giải hoặc bước đi sai |
| Surrender | Mô hình bỏ cuộc |
| Claimed Contradiction | Mô hình nói đề mâu thuẫn |
| Missing Information | Mô hình nói đề thiếu dữ kiện |

---

# Slide 34. Vì Sao 9x9 Khó Hơn?

**9x9 tăng độ khó theo nhiều hướng**

So sánh 6x6 và 9x9:

| Tiêu chí | 6x6 | 9x9 |
|---|---:|---:|
| Số ô | 36 | 81 |
| Miền giá trị | 1-6 | 1-9 |
| Lượt gọi multi-step tối đa | 72 | 162 |
| Số tổ hợp cage | Ít hơn | Nhiều hơn |
| Context prompt | Ngắn hơn | Dài hơn |

Vì sao 9x9 dễ fail hơn hoặc cần nhiều bước hơn?

- Nhiều ứng viên hơn cho mỗi ô.
- Cage có nhiều tổ hợp hơn.
- Ràng buộc chồng chéo phức tạp hơn.
- Prompt và cheat sheet cần thiết kế riêng cho 9x9.

Trạng thái:

> Nhóm đã tách pipeline 9x9 riêng và đã có một run thành công ban đầu trên Gemini 2.5 Pro. Các run 9x9 còn lại vẫn đang tiếp tục chạy để có bảng benchmark đầy đủ.

---

# Slide 35. Nhận Định Từ Kết Quả Hiện Tại

**Các quan sát chính**

1. **6x6 là phạm vi khả thi**
   - Single-prompt và multi-step đều có model giải được tốt trên 6x6.
   - Tuy nhiên kết quả phân hóa rõ theo từng model và từng mode.

2. **Single-prompt 6x6: Gemini 2.5 Pro và Gemini 3.5 Flash mạnh nhất**
   - Gemini 2.5 Pro đạt 5/5.
   - Gemini 3.5 Flash đạt 5/5.
   - Gemini 2.5 Flash đạt 4/5.
   - Gemini 3.1 Flash Lite đạt 0/5.

3. **Multi-step 6x6: Gemini 3.5 Flash đang nổi bật nhất**
   - Gemini 3.5 Flash đạt 5/5 ở multi-step.
   - Gemini 2.5 Flash và Gemini 2.5 Pro đều đạt 4/5.
   - Gemini 3.1 Flash Lite đạt 0/5, nên có thể dùng như một baseline yếu.

4. **9x9 cần pipeline và prompt riêng**
   - Pipeline 9x9 đã được tách trong `cs106/9x9`.
   - Gemini 2.5 Pro đã giải thành công puzzle 06 bằng multi-step trong 83 bước.
   - Chưa nên kết luận tổng quát cho 9x9 vì các run còn lại chưa hoàn tất.

5. **Validator là bắt buộc**
   - Reasoning nghe hợp lý vẫn có thể sai.
   - Ground truth giúp đánh giá khách quan.

---

# Slide 36. So Sánh Với Paper Gốc

**Kết quả nhóm phù hợp với tinh thần của Sudoku-Bench**

Nhận định từ paper:

- Sudoku variants là benchmark tốt cho creative reasoning.
- LLM có thể gặp khó khi cần duy trì ràng buộc toàn cục.
- Lời giải thích tự nhiên không đảm bảo nghiệm đúng.
- Multi-step giúp quan sát quá trình suy luận.
- Các bài lớn và nhiều ràng buộc khó hơn rõ rệt.

Quan sát của nhóm:

- 6x6 có thể giải được với prompt phù hợp.
- 6x6 cho thấy kết quả khác nhau rõ giữa single-prompt và multi-step.
- Gemini 2.5 Pro và Gemini 3.5 Flash cùng đạt 5/5 ở single-prompt 6x6.
- Gemini 3.5 Flash cũng đạt 5/5 ở multi-step 6x6.
- 9x9 ban đầu khó hơn, nhưng pipeline 9x9 mới đã có một run thành công trên Gemini 2.5 Pro.
- Multi-step log cho thấy lỗi xuất hiện ở bước cụ thể.
- Validator phát hiện sai ngay cả khi output có vẻ hợp lý.
- Chi phí API là một rào cản thực nghiệm đáng kể.

Thông điệp:

> Nhóm tái hiện được một phần tinh thần thực nghiệm của paper trong phạm vi đồ án.

Media:

- Dùng Figure 4 của paper để nối phần phân tích lỗi:
  - ![Figure 4 - Paper response categorization](paper-assets/paper-page-09-image-01.png)
- Có thể đặt cạnh bảng kết quả của nhóm để so sánh:
  - paper: nhiều model, nhiều puzzle, nhiều loại lỗi;
  - nhóm: 4 model Gemini, 6x6/9x9 Killer Sudoku, log single-prompt và multi-step.

---

# Slide 37. Demo Pipeline

**Kịch bản demo**

1. Mở notebook:

```text
cs106/api_llm.ipynb
```

2. Chỉ file dataset:

```text
cs106/dataset/puzzle_01.json
```

3. Chỉ prompt/cheat sheet:

```text
cs106/killer_sudoku_cheat_sheet.md
cs106/analysis_template.md
```

4. Chỉ output single-prompt:

```text
cs106/outputs/gemini-2.5/single_prompt/flash/result_puzzle_01.json
cs106/outputs/gemini-2.5/single_prompt/pro/result_puzzle_01.json
cs106/outputs/gemini-3.x/single-prompt/lite/result_puzzle_01.json
```

5. Chỉ log multi-step:

```text
cs106/outputs/gemini-2.5/multi_prompt/flash/log_puzzle_01.json
cs106/outputs/gemini-3.x/multi-prompt/flash/log_puzzle_01.json
cs106/9x9/outputs/Pro/log_puzzle_06_pro.json
```

6. Chỉ biểu đồ:

```text
cs106/outputs/benchmark_results_comparison.png
cs106/outputs/advanced_analysis.png
```

Demo nên ưu tiên:

- replay output/log có sẵn;
- không gọi API quá nhiều trực tiếp;
- tránh rủi ro mạng/rate limit/chi phí.

---

# Slide 38. Demo Single-Prompt

**Demo single-prompt**

Mục tiêu demo:

- cho thấy model nhận toàn bộ puzzle;
- trả về một grid hoàn chỉnh;
- hệ thống kiểm tra grid với solution;
- lưu status Success/Failed.

File minh họa:

```text
cs106/outputs/gemini-2.5/single_prompt/flash/result_puzzle_02.json
cs106/outputs/gemini-2.5/single_prompt/pro/result_puzzle_01.json
cs106/outputs/gemini-3.x/single-prompt/lite/result_puzzle_01.json
```

Nội dung cần highlight:

```json
{
  "puzzle_id": 1,
  "model": "gemini-2.5-pro",
  "status": "Success",
  "prediction": [...]
}
```

Điểm cần nhấn:

- Single-prompt đơn giản hơn multi-step.
- Ít lượt gọi API.
- Nhưng khi fail, khó biết mô hình sai ở bước nào.

---

# Slide 39. Demo Multi-Step

**Demo multi-step**

Mục tiêu demo:

- cho thấy mô hình điền từng ô;
- mỗi bước có reasoning;
- board được cập nhật;
- validator kiểm tra từng bước;
- log lưu lại toàn bộ quá trình.

File minh họa:

```text
cs106/outputs/gemini-3.x/multi-prompt/flash/log_puzzle_01.json
cs106/9x9/outputs/Pro/log_puzzle_06_pro.json
```

Một entry log gồm:

```json
{
  "step": 1,
  "chosen_cell": "r2c5",
  "value": 1,
  "reasoning": "...",
  "is_certain": true,
  "board_state": [...]
}
```

Điểm cần nhấn:

- Multi-step giúp phân tích lỗi tốt hơn.
- Nếu sai một bước, phiên chạy dừng.
- Không có cơ chế hoàn tác hoặc solver sửa giúp.

---

# Slide 40. Nếu Demo Trực Tiếp Gặp Lỗi

**Phương án dự phòng**

Vì demo phụ thuộc vào API và môi trường chạy, nhóm chuẩn bị:

- notebook đã chạy sẵn;
- output JSON đã lưu;
- log multi-step đã lưu;
- biểu đồ kết quả;
- video demo bổ sung nếu cần.

Theo quy định mới:

- nếu thực nghiệm/demo chưa hoàn tất, nhóm có thể quay video bổ sung;
- hạn chót bổ sung video: 21/06;
- sau báo cáo, nhóm chỉnh slide/demo theo góp ý của GV và nộp lại.

Thông điệp:

> Demo chính là pipeline và log thực nghiệm, không nhất thiết phải gọi API lại toàn bộ trong lúc trình bày.

---

# Slide 41. Đóng Góp Của Nhóm

**Nhóm đã thực hiện**

Về lý thuyết:

- đọc paper Sudoku-Bench;
- tìm hiểu Sudoku variants;
- mô hình hóa Sudoku/Killer Sudoku dưới góc nhìn CSP;
- liên hệ hạn chế của LLM với suy luận ràng buộc.

Về thực nghiệm:

- xây dựng dataset JSON cho Killer Sudoku;
- xây dựng single-prompt evaluation;
- xây dựng multi-step evaluation;
- benchmark 6x6 trên 4 model Gemini: 2.5 Flash, 2.5 Pro, 3.1 Flash Lite, 3.5 Flash;
- tách pipeline 9x9 riêng và có run thành công ban đầu trên Gemini 2.5 Pro;
- xây parser và validator;
- lưu output/log;
- tổng hợp kết quả và biểu đồ.

Về báo cáo/demo:

- chuẩn bị slide;
- chuẩn bị notebook demo;
- chuẩn bị log để phân tích lỗi;
- chuẩn bị video bổ sung nếu cần.

---

# Slide 42. Hạn Chế Của Đồ Án

**Hạn chế**

1. **Dataset nhỏ hơn paper gốc**
   - Nhóm chỉ chạy một tập rút gọn.
   - Chưa bao phủ toàn bộ Sudoku-Bench.

2. **Chủ yếu tập trung Killer Sudoku**
   - Chưa thử nhiều variant khác như Arrow, Thermometer, Knight.

3. **Số model còn hạn chế**
   - Đã mở rộng lên 4 model Gemini.
   - Tuy nhiên vẫn nằm trong cùng hệ sinh thái Gemini, chưa so sánh với GPT/Claude/model mã nguồn mở.

4. **9x9 chưa có bảng benchmark đầy đủ**
   - Đã có một run thành công trên Gemini 2.5 Pro với puzzle 06.
   - Các run còn lại cho 4 model và 2 map vẫn đang tiếp tục chạy.
   - Vì vậy chưa nên kết luận solve rate cuối cùng cho 9x9.

5. **Chi phí multi-step cao**
   - 6x6 có thể cần tới 72 lượt gọi/puzzle.
   - 9x9 có thể cần tới 162 lượt gọi/puzzle.

6. **Prompt ảnh hưởng mạnh tới kết quả**
   - Cùng model nhưng prompt khác có thể cho kết quả khác.

---

# Slide 43. Hướng Phát Triển

**Hướng phát triển tiếp theo**

1. **Hoàn thiện 9x9**
   - Chạy đủ 4 model trên 2 puzzle 9x9;
   - cập nhật bảng kết quả cuối;
   - phân tích khác biệt giữa puzzle 06 và puzzle 07;
   - kiểm tra các lỗi fail nếu có.

2. **Mở rộng dataset**
   - thêm nhiều puzzle 6x6;
   - thêm nhiều puzzle 9x9;
   - kiểm tra độ khó đa dạng hơn.

3. **Thử thêm model**
   - model ngoài hệ Gemini để tăng tính khách quan;
   - model mã nguồn mở nếu có API phù hợp;
   - model nhỏ hơn để tạo baseline yếu rõ hơn.

4. **Thử thêm Sudoku variants**
   - Arrow;
   - Thermometer;
   - Knight's Move;
   - kết hợp nhiều luật.

5. **Kết hợp symbolic solver**
   - LLM đề xuất suy luận;
   - solver kiểm tra ràng buộc;
   - hướng Neuro-Symbolic AI.

---

# Slide 44. Kết Luận

**Kết luận chính**

- Sudoku-Bench là một benchmark phù hợp để đánh giá suy luận ràng buộc của LLM.
- Killer Sudoku có thể được mô hình hóa rõ ràng như một bài toán CSP.
- Nhóm đã tái hiện rút gọn thực nghiệm bằng pipeline riêng.
- Trên 6x6, Gemini 2.5 Pro và Gemini 3.5 Flash nổi bật ở single-prompt; Gemini 3.5 Flash nổi bật nhất ở multi-step.
- Multi-step giúp quan sát quá trình suy luận, nhưng không luôn vượt single-prompt về solve rate.
- 9x9 khó hơn rõ rệt, nhưng pipeline 9x9 mới đã có một kết quả thành công ban đầu với Gemini 2.5 Pro.
- Validator là thành phần bắt buộc để đánh giá khách quan.

Thông điệp cuối:

> LLM có tiềm năng trong suy luận ràng buộc, nhưng với CSP, cần đánh giá nghiêm ngặt bằng ground truth, log và validator thay vì chỉ dựa vào lời giải thích tự nhiên.

---

# Backup 1. Phân Công Thành Viên

**Phân công nhóm**

| Vai trò | Công việc |
|---|---|
| API / Pipeline | gọi LLM, xử lý response, tích hợp notebook |
| Dataset / Evaluator | chuẩn hóa puzzle, solution, cages, validator |
| Prompt / Testing | single-prompt, multi-step, cheat sheet, chạy thử nghiệm |
| Report / Slide / Analysis | paper, báo cáo, slide, phân tích kết quả và lỗi |

---

# Backup 2. Vì Sao Không Chạy Full Benchmark?

**Lý do không chạy toàn bộ benchmark**

- Paper gốc có phạm vi lớn hơn nhiều so với đồ án môn học.
- Multi-step cực kỳ tốn lượt gọi API.
- Chi phí tăng theo:

```text
số puzzle × số model × số ô × số lượt gọi mỗi ô
```

- Nhóm ưu tiên:
  - pipeline chạy được;
  - kết quả có validator;
  - có log phân tích;
  - có demo rõ ràng;
  - phạm vi đủ để rút nhận xét.

Trả lời ngắn:

> Nhóm tái hiện một phần thực nghiệm theo yêu cầu đồ án, không đặt mục tiêu tái hiện 100% benchmark gốc.

---

# Backup 3. Multi-Step Có Hỗ Trợ AI Quá Nhiều Không?

**Multi-step không solve thay model**

Pipeline chỉ làm:

- gửi trạng thái hiện tại cho model;
- yêu cầu model phân tích;
- yêu cầu model chọn một ô và một giá trị;
- parse output;
- validate đúng/sai;
- lưu log.

Pipeline không làm:

- tự tìm ô tốt nhất;
- tự suy luận đáp án;
- tự sửa lỗi của model;
- cho phép hoàn tác sau khi sai.

Kết luận:

> Quyết định suy luận vẫn đến từ LLM; hệ thống chỉ quản lý trạng thái và kiểm chứng.

---

# Backup 4. Vì Sao Dùng Cheat Sheet?

**Cheat sheet là context, không phải solver**

Cheat sheet cung cấp:

- tổ hợp cage hợp lệ;
- các tổng thường gặp;
- hỗ trợ giảm lỗi tính toán tổ hợp.

Cheat sheet không cung cấp:

- ô nào phải điền số nào;
- thứ tự giải;
- nghiệm hoàn chỉnh;
- bước break-in cụ thể của puzzle.

Ví dụ:

```text
Cage 2 ô tổng 5 có thể là {1,4} hoặc {2,3}
```

Model vẫn phải dùng hàng/cột/khối/cage khác để quyết định đáp án.

---

# Backup 5. Trạng Thái 9x9

**9x9 đã có pipeline riêng và kết quả ban đầu**

Pipeline 9x9:

```text
cs106/9x9/api_llm_9x9.ipynb
cs106/9x9/analysis_template_9x9.md
cs106/9x9/killer_sudoku_cheat_sheet_9x9.md
```

Kết quả đã có:

| Puzzle | Model | Mode | Status | Steps |
|---|---|---|---|---:|
| 06 | Gemini 2.5 Pro | Multi-step | Success | 83 |

Kết quả đang chờ:

- 2 puzzle 9x9 hard: puzzle 06 và puzzle 07;
- 4 model dự kiến benchmark;
- single-prompt và multi-step tùy cấu hình chạy cuối;
- bảng solve rate 9x9 cuối cùng sẽ cập nhật sau khi đủ log.

Điểm cần nói khi vấn đáp:

- 9x9 không còn là "chưa chạy được";
- đã có bằng chứng pipeline giải được ít nhất một puzzle hard;
- nhưng chưa đủ số liệu để kết luận model nào tốt nhất trên 9x9;
- chi phí cao vì multi-step 9x9 có thể cần tới 162 lượt gọi/puzzle.

---

# Backup 6. Câu Hỏi Vấn Đáp Nhanh

**Câu hỏi: Nếu 6x6 single-prompt đã tốt, multi-step còn ý nghĩa không?**

Có. Multi-step không chỉ để tăng solve rate mà để quan sát quá trình suy luận. Nó giúp biết model sai ở bước nào, vì sao sai và loại ràng buộc nào bị bỏ sót.

**Câu hỏi: Vì sao Pro single-prompt tốt hơn multi-step trên 6x6 hiện tại?**

Vì multi-step yêu cầu nhiều quyết định liên tiếp. Chỉ cần một bước sai là fail. Single-prompt có thể tận dụng context toàn cục trong một lần sinh output, còn multi-step bị ràng buộc bởi từng quyết định nhỏ.

**Câu hỏi: Vì sao 9x9 vẫn được xem là khó nếu đã có một run thành công?**

Vì một run thành công chưa đủ để kết luận solve rate. 9x9 có nhiều ô hơn, miền giá trị lớn hơn, cage phức tạp hơn và prompt dài hơn. Kết quả puzzle 06 với Gemini 2.5 Pro chứng minh pipeline có thể giải được, còn bảng benchmark đầy đủ cần thêm các run còn lại.

**Câu hỏi: Nhóm có cải tiến gì?**

Nhóm không tuyên bố cải tiến thuật toán lớn so với paper. Đóng góp nằm ở tái hiện rút gọn, xây pipeline, thiết kế prompt multi-step analysis/fill, dùng cheat sheet Killer Sudoku, lưu log và phân tích lỗi.
Nhóm cũng mở rộng benchmark nội bộ lên 4 model Gemini và tách riêng pipeline 9x9 để thử các puzzle khó hơn.

**Câu hỏi: Vì sao cần validator?**

Vì reasoning của LLM có thể nghe đúng nhưng đáp án vẫn sai. Validator giúp đánh giá khách quan bằng nghiệm chuẩn.

---

# Checklist Chuẩn Bị Slide Cuối

Nội dung cần cập nhật trước khi nộp bản cuối:

- [ ] Kết quả 9x9 đầy đủ cho 4 model và 2 puzzle hard.
- [ ] Biểu đồ cuối cùng nếu số liệu thay đổi.
- [ ] Một ảnh minh họa puzzle 6x6.
- [ ] Một ảnh minh họa output single-prompt success.
- [ ] Một ảnh minh họa output single-prompt fail.
- [ ] Một ảnh minh họa log multi-step success.
- [ ] Một ảnh minh họa log multi-step fail.
- [ ] Video demo dự phòng.

File nên lấy ảnh/chụp màn hình:

- `cs106/dataset/puzzle_01.json`
- `cs106/api_llm.ipynb`
- `cs106/killer_sudoku_cheat_sheet.md`
- `cs106/outputs/gemini-2.5/single_prompt/flash/result_puzzle_01.json`
- `cs106/outputs/gemini-2.5/single_prompt/pro/result_puzzle_01.json`
- `cs106/outputs/gemini-3.x/multi-prompt/flash/log_puzzle_01.json`
- `cs106/9x9/outputs/Pro/log_puzzle_06_pro.json`
- `cs106/outputs/benchmark_results_comparison.png`
- `cs106/outputs/advanced_analysis.png`
