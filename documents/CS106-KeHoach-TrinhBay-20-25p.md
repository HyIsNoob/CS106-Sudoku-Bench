# Kế hoạch trình bày CS106 - Sudoku-Bench theo quy định mới

## 1. Quy định mới cần bám

- Mỗi nhóm có **20-25 phút** để trình bày slide **kèm demo**.
- Sau đó có **5-10 phút vấn đáp**.
- Nếu thực nghiệm/demo chưa hoàn thành tại ngày báo cáo, nhóm có thể **quay video bổ sung**.
- Hạn chót bổ sung video và nộp lại slide/demo sau góp ý của giảng viên: **21/06**.

## 2. Chiến lược trình bày đề xuất

Với thời lượng mới, nhóm không nên chỉ nói nhanh theo kiểu 15 phút nữa. Nên chia bài thành ba tầng:

1. **Lý thuyết và paper gốc:** giải thích rõ vì sao Sudoku-Bench là benchmark cho suy luận CSP.
2. **Tái hiện thực nghiệm:** trình bày rõ nhóm đã làm phần nào, pipeline chạy ra sao, giới hạn vì chi phí API.
3. **Demo và phân tích:** cho thấy notebook/log/validator thật sự hoạt động, rồi kết luận từ kết quả.

Thông điệp chính:

> Nhóm tái hiện rút gọn Sudoku-Bench trên Killer Sudoku để đánh giá khả năng suy luận ràng buộc của LLM. Kết quả chính nằm ở các bài 6x6; 9x9 dùng như stress-test để quan sát khi quy mô tăng.

## 3. Phân bổ thời gian 20-25 phút

| Phần | Thời lượng | Nội dung |
|---|---:|---|
| Mở đầu và vấn đề | 2 phút | Vì sao cần benchmark suy luận logic cho LLM |
| Paper và lý thuyết CSP | 5 phút | Sudoku-Bench, CSP, Sudoku variants, Killer Sudoku |
| Thiết kế thực nghiệm | 5 phút | Dataset, prompt, single-shot, multi-step, validator |
| Kết quả và phân tích lỗi | 6 phút | 6x6, 9x9, lỗi, so sánh với paper |
| Demo | 4-5 phút | Notebook/pipeline/log/validator |
| Kết luận | 1-2 phút | Đóng góp, hạn chế, hướng phát triển |

Nếu chỉ còn 20 phút, rút phần lý thuyết còn 4 phút và demo còn 3 phút.

## 4. Cấu trúc slide đề xuất

Mục tiêu: **26 slide chính + 3 slide dự phòng**. Khi nói, không cần dừng lâu ở mọi slide; các slide pipeline/demo/kết quả mới là phần nói kỹ.

### Slide 1. Trang bìa

**Nội dung:** tên đề tài, môn học, nhóm, giảng viên, thời gian.

**Media:** logo UIT, nền lưới Sudoku nhẹ.

### Slide 2. Vấn đề nghiên cứu

**Nội dung:** LLM mạnh ở ngôn ngữ, nhưng CSP cần đúng tuyệt đối; một bước sai làm toàn bộ lời giải sai.

**Media:** sơ đồ `Pattern matching` vs `Constraint reasoning`.

### Slide 3. Câu hỏi nghiên cứu của nhóm

**Nội dung:** LLM có thể đọc luật mới, tìm bước mở khóa, và duy trì ràng buộc toàn cục khi giải Sudoku variants không?

**Media:** 3 câu hỏi dạng checklist.

### Slide 4. Paper tham chiếu

**Nội dung:** *Sudoku-Bench: Evaluating Creative Reasoning with Sudoku Variants*; mục tiêu, benchmark, ý nghĩa.

**Media:** ảnh/citation box của paper.

### Slide 5. Sudoku-Bench đánh giá điều gì?

**Nội dung:** creative reasoning, break-in, giải luật mới, không chỉ nhớ mẫu Sudoku chuẩn.

**Media:** sơ đồ từ puzzle mới -> luật mới -> lời giải.

### Slide 6. CSP là gì?

**Nội dung:** biến `X`, miền giá trị `D`, ràng buộc `C`; mục tiêu là gán giá trị thỏa toàn bộ ràng buộc.

**Media:** công thức `<X, D, C>`.

### Slide 7. Sudoku dưới góc nhìn CSP

**Nội dung:** mỗi ô là biến; miền là `{1..n}`; ràng buộc hàng/cột/khối.

**Media:** lưới Sudoku highlight hàng, cột, khối.

### Slide 8. Sudoku variants

**Nội dung:** Knight, Arrow, Thermometer, Killer cage; luật phụ làm tăng độ khó.

**Media:** bảng nhỏ liệt kê variant và ràng buộc.

### Slide 9. Killer Sudoku

**Nội dung:** cage, tổng mục tiêu, không lặp số trong cage, kết hợp với luật Sudoku chuẩn.

**Media:** hình 6x6 có cage; ví dụ cage tổng 3 -> `{1,2}`.

### Slide 10. Break-in

**Nội dung:** bước mở khóa ban đầu; sau đó ràng buộc lan truyền.

**Media:** flow `nhiều khả năng -> break-in -> lan truyền`.

### Slide 11. Vì sao LLM dễ sai?

**Nội dung:** sinh token tuần tự, khó giữ trạng thái toàn cục, khó quay lui, lập luận nghe đúng nhưng có thể sai hình thức.

**Media:** `sai một ô -> trạng thái sai -> suy luận sau sai theo`.

### Slide 12. Paper gốc đánh giá như thế nào?

**Nội dung:** single-shot, multi-step, solve rate, correct placements, error types.

**Media:** bảng Single-shot vs Multi-step.

### Slide 13. Phạm vi tái hiện của nhóm

**Nội dung:** không tái hiện toàn bộ benchmark; tập trung Killer Sudoku; 4x4 là sanity check; 6x6 là chính; 9x9 là stress-test.

**Media:** bảng so sánh paper gốc vs nhóm.

### Slide 14. Vì sao không scale toàn bộ benchmark?

**Nội dung:** chi phí API và số lượt gọi tăng nhanh; 6x6 multi-step tối đa 72 lượt gọi/puzzle; 9x9 tối đa 162 lượt gọi/puzzle.

**Media:** infographic `36 ô -> 72 calls`, `81 ô -> 162 calls`.

### Slide 15. Dataset nhóm sử dụng

**Nội dung:** số lượng puzzle, size, difficulty, grid ban đầu, solution, cages.

**Media:** bảng dataset + snippet JSON ngắn.

### Slide 16. Pipeline tổng quát

**Nội dung:** Data Loader -> Prompt Builder -> Gemini API -> Parser -> Validator -> Log.

**Media:** sơ đồ pipeline.

### Slide 17. Single-shot

**Nội dung:** model nhận toàn bộ đề và trả lời grid hoàn chỉnh trong một lần.

**Media:** prompt rút gọn và output grid.

### Slide 18. Multi-step

**Nội dung:** mỗi vòng gồm Analysis và Fill; sau mỗi fill, hệ thống cập nhật board và kiểm tra ngay.

**Media:** vòng lặp `Analysis -> Fill -> Validate -> Continue/Stop`.

### Slide 19. Prompt engineering

**Nội dung:** luật Killer Sudoku, cage list, cheat sheet tổ hợp cage, JSON schema.

**Media:** snippet prompt hoặc schema JSON.

### Slide 20. Validator và tiêu chí dừng

**Nội dung:** đúng nếu grid cuối trùng solution; sai một ô thì dừng; log từng bước để phân tích.

**Media:** flow `move -> compare solution -> pass/fail`.

### Slide 21. Kết quả tổng hợp

**Nội dung:** bảng kết quả cuối cùng của Flash/Pro trên 6x6 và 9x9. Nếu chưa khóa kết quả, để placeholder rõ.

**Media:** bảng kết quả + biểu đồ cột.

### Slide 22. Phân tích 6x6

**Nội dung:** 6x6 là phần chính; nêu solve rate, số puzzle pass/fail, nhận xét multi-step.

**Media:** bar chart 6x6.

### Slide 23. Phân tích 9x9

**Nội dung:** 9x9 khó hơn do số ô, miền giá trị, cage và số lượt gọi tăng; chỉ kết luận trong cấu hình nhóm.

**Media:** bảng số bước trước khi fail hoặc ảnh log fail.

### Slide 24. Phân tích lỗi

**Nội dung:** Incorrect Solution, Surrender, Claimed Contradiction, Missing Information; nhóm gặp lỗi nào thì nêu cụ thể.

**Media:** bảng error type + ví dụ log.

### Slide 25. Demo

**Nội dung trên slide:** đường đi demo:

1. mở notebook `cs106/api_llm.ipynb`;
2. chỉ dataset/puzzle;
3. chạy hoặc chiếu lại một lượt multi-step;
4. xem board cập nhật;
5. xem validator báo đúng/sai;
6. mở output/log/biểu đồ.

**Media:** ảnh chụp notebook hoặc sơ đồ demo.

### Slide 26. Kết luận

**Nội dung:** nhóm đã tái hiện rút gọn, xây pipeline tự động, có demo/log, 6x6 là kết quả chính, 9x9 cho thấy độ khó tăng mạnh.

**Media:** 3 dòng takeaways.

## 5. Slide dự phòng cho vấn đáp

### Backup A. Phân công thành viên

**Nội dung:** ai làm API, dataset/evaluator, prompt/testing, report/slide/analysis.

### Backup B. Một ví dụ log multi-step

**Nội dung:** cell được chọn, value, reasoning, board trước/sau, validator.

### Backup C. Vì sao kết quả không bằng paper gốc?

**Nội dung:** khác model, khác số puzzle, khác biến thể, giới hạn API, paper dùng benchmark lớn hơn.

## 6. Demo nên chuẩn bị thế nào

Demo nên có **hai phương án**:

### Phương án A: Demo trực tiếp

- Mở notebook đã chạy sẵn các cell setup.
- Không gọi API quá nhiều trong lúc báo cáo.
- Chỉ chạy một cell nhỏ hoặc một puzzle ngắn nếu chắc chắn ổn.
- Có sẵn output/log để tránh lỗi mạng/API.

### Phương án B: Video/demo ghi sẵn

- Quay 2-4 phút quy trình chạy pipeline.
- Nội dung video: chọn puzzle -> gọi model -> fill một vài bước -> validator -> kết quả/log.
- Nếu hôm báo cáo thực nghiệm chưa hoàn tất, dùng video này để bổ sung trước **21/06**.

Khuyến nghị: dù có demo trực tiếp, vẫn nên quay sẵn video dự phòng.

## 7. Chia người nói

| Người | Slide | Thời lượng | Nội dung |
|---|---:|---:|---|
| Người 1 | 1-6 | 4-5 phút | Mở đầu, paper, CSP |
| Người 2 | 7-12 | 5 phút | Sudoku variants, Killer Sudoku, giới hạn LLM, cách paper đánh giá |
| Người 3 | 13-20 | 6-7 phút | Phạm vi tái hiện, dataset, pipeline, prompt, validator |
| Người 4 | 21-26 + demo | 7-8 phút | Kết quả, phân tích lỗi, demo, kết luận |

Nếu demo do người khác phụ trách, tách Slide 25 cho người chạy code và người 4 chỉ nói kết luận.

## 8. Việc cần làm trước ngày báo cáo

- Chốt số liệu 6x6 và 9x9 trong bảng kết quả.
- Chọn một log thành công và một log thất bại để đưa vào slide.
- Chụp ảnh notebook/pipeline/validator.
- Quay video demo dự phòng.
- Chuẩn bị câu trả lời cho các câu hỏi:
  - Vì sao không tái hiện toàn bộ benchmark?
  - Vì sao chỉ dùng Gemini 2.5 Flash/Pro?
  - Multi-step có phải đang hỗ trợ AI quá nhiều không?
  - Kết quả nhóm khác paper gốc ở điểm nào?
  - Nếu có thêm thời gian, nhóm sẽ cải tiến gì?

## 9. Sau khi báo cáo

- Ghi lại góp ý của giảng viên trong phần vấn đáp.
- Sửa slide/demo theo góp ý.
- Nếu cần, quay hoặc cập nhật video demo bổ sung.
- Nộp lại bản cuối trên courses trước **21/06**.
