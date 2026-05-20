# Nội dung slide thuyết trình CS106 - Sudoku-Bench

## Gợi ý tổng thể

- **Thời lượng mục tiêu:** 15-18 phút.
- **Số slide đề xuất:** 22 slide.
- **Thông điệp chính:** Nhóm tái hiện rút gọn Sudoku-Bench trên Killer Sudoku để kiểm tra khả năng suy luận ràng buộc của LLM. Kết quả chính nằm ở 5 bài 6x6; 2 bài 9x9 là stress-test.
- **Tông trình bày:** học thuật, rõ phạm vi, không nói quá kết quả.

---

## Slide 1. Trang bìa

**Title:**  
Đánh giá khả năng suy luận và giải quyết bài toán CSP của LLM thông qua Sudoku-Bench

**Nội dung trên slide:**
- Môn học: CS106 - Trí tuệ nhân tạo
- Nhóm thực hiện
- Giảng viên hướng dẫn
- Thời gian thực hiện

**Media:**
- Logo UIT.
- Có thể thêm nền rất nhẹ dạng lưới Sudoku mờ.

**Ghi chú nói:**
- Giới thiệu tên đề tài, paper tham chiếu và mục tiêu tổng quát của nhóm.

---

## Slide 2. Vấn đề nghiên cứu

**Title:**  
LLM có thật sự suy luận logic hay chỉ nhận diện mẫu?

**Nội dung trên slide:**
- LLM mạnh ở sinh văn bản, code, trả lời câu hỏi.
- Nhưng CSP yêu cầu tính đúng/sai tuyệt đối.
- Một bước sai có thể làm toàn bộ lời giải sai.
- Câu hỏi của nhóm: LLM xử lý Sudoku biến thể tốt đến đâu?

**Media:**
- Sơ đồ đối chiếu: `Pattern matching` vs `Constraint reasoning`.
- Có thể dùng icon não/logic/checklist.

**Ghi chú nói:**
- Dẫn vào lý do chọn Sudoku: có nghiệm chuẩn, dễ kiểm chứng, nhưng cần suy luận nhiều bước.

---

## Slide 3. Paper tham chiếu

**Title:**  
Paper gốc: Sudoku-Bench

**Nội dung trên slide:**
- Paper: *Sudoku-Bench: Evaluating Creative Reasoning with Sudoku Variants*.
- Mục tiêu: đánh giá suy luận sáng tạo của LLM.
- Dùng Sudoku variants thay vì Sudoku chuẩn.
- Mô hình phải đọc luật mới, tìm break-in, duy trì tính nhất quán.

**Media:**
- Ảnh trang đầu paper hoặc citation box.
- Một hình Sudoku variant từ paper nếu có.

**Ghi chú nói:**
- Nhấn mạnh nhóm chọn một paper cụ thể, không phải survey.

---

## Slide 4. Vì sao Sudoku variants phù hợp?

**Title:**  
Sudoku variants là bài kiểm tra tốt cho suy luận

**Nội dung trên slide:**
- Có nghiệm đúng duy nhất hoặc nghiệm chuẩn để kiểm tra.
- Luật rõ ràng, có thể biểu diễn thành ràng buộc.
- Khó dựa vào ghi nhớ mẫu.
- Cần kết hợp nhiều luật cùng lúc.

**Media:**
- Minh họa Sudoku chuẩn vs Sudoku có luật bổ sung.
- Bảng nhỏ: hàng/cột/khối/cage.

**Ghi chú nói:**
- Nói rằng Sudoku không chỉ là trò chơi; dưới góc nhìn AI, nó là CSP.

---

## Slide 5. CSP là gì?

**Title:**  
Constraint Satisfaction Problem (CSP)

**Nội dung trên slide:**
- Một CSP gồm:
  - Biến `X`
  - Miền giá trị `D`
  - Tập ràng buộc `C`
- Mục tiêu: gán giá trị cho biến sao cho mọi ràng buộc đều thỏa.

**Media:**
- Công thức: `<X, D, C>`.
- Sơ đồ 3 khối: Variables - Domains - Constraints.

**Ghi chú nói:**
- Đây là phần liên hệ trực tiếp với môn CS106.

---

## Slide 6. Sudoku dưới góc nhìn CSP

**Title:**  
Mô hình hóa Sudoku thành CSP

**Nội dung trên slide:**
- Biến: mỗi ô trên lưới.
- Miền giá trị:
  - 6x6: `{1,...,6}`
  - 9x9: `{1,...,9}`
- Ràng buộc:
  - Không lặp trong hàng.
  - Không lặp trong cột.
  - Không lặp trong khối.

**Media:**
- Hình lưới Sudoku có highlight một hàng, một cột, một khối.
- Nếu chưa có hình, tạo bằng PowerPoint cũng được.

**Ghi chú nói:**
- Từ đây chuyển sang biến thể nhóm dùng: Killer Sudoku.

---

## Slide 7. Killer Sudoku

**Title:**  
Biến thể nhóm chọn: Killer Sudoku

**Nội dung trên slide:**
- Ngoài luật Sudoku chuẩn, có thêm các cage.
- Mỗi cage gồm một nhóm ô.
- Tổng các chữ số trong cage phải bằng tổng mục tiêu.
- Chữ số trong cùng cage không được lặp.

**Media:**
- Hình minh họa một lưới 6x6 với cage.
- Có thể dùng ví dụ: `r1c1 + r2c1 = 3`.

**Ghi chú nói:**
- Giải thích cage bằng ví dụ nhỏ: tổng 3 thì chỉ có cặp `{1,2}`.

---

## Slide 8. Break-in

**Title:**  
Break-in: điểm mở khóa lời giải

**Nội dung trên slide:**
- Nhiều Sudoku variants không có bước đầu hiển nhiên.
- Người giải cần tìm một suy luận then chốt.
- Sau break-in, các ràng buộc lan truyền dần.
- Đây là phần paper gọi là creative reasoning.

**Media:**
- Sơ đồ 3 bước:
  - Ban đầu nhiều ô trống.
  - Tìm break-in.
  - Các ô tiếp theo được suy ra.

**Ghi chú nói:**
- Liên hệ với LLM: mô hình không chỉ cần tính toán, mà phải biết “bắt đầu từ đâu”.

---

## Slide 9. Giới hạn của LLM với CSP

**Title:**  
Vì sao CSP khó với LLM?

**Nội dung trên slide:**
- LLM sinh từng token theo ngữ cảnh.
- Dễ tạo lập luận nghe hợp lý nhưng sai.
- Khó duy trì trạng thái toàn cục.
- Khó quay lui khi đã chọn sai.

**Media:**
- Flow nhỏ: `Sai một ô -> trạng thái sai -> lập luận sau sai theo`.
- Icon warning/check.

**Ghi chú nói:**
- Đây là lý do cần benchmark có kiểm tra nghiệm tự động.

---

## Slide 10. Thiết kế đánh giá của Sudoku-Bench

**Title:**  
Paper đánh giá như thế nào?

**Nội dung trên slide:**
- **Single-shot:** model trả lời toàn bộ nghiệm trong một lần.
- **Multi-step:** model đi từng bước, hệ thống cập nhật trạng thái.
- Chỉ số chính: solve rate.
- Multi-step giúp phân tích quá trình sai/đúng.

**Media:**
- Bảng hai cột: Single-shot vs Multi-step.
- Sơ đồ vòng lặp multi-step.

**Ghi chú nói:**
- Nhóm ưu tiên multi-step vì có log để phân tích lỗi.

---

## Slide 11. Phạm vi tái hiện của nhóm

**Title:**  
Nhóm tái hiện phần nào?

**Nội dung trên slide:**
- Không tái hiện toàn bộ benchmark vì giới hạn thời gian và chi phí API.
- Tập trung vào Killer Sudoku.
- Tập chính: 5 bài 6x6.
- Tập mở rộng: 2 bài 9x9.
- Mô hình: Gemini 2.5 Flash và Gemini 2.5 Pro.

**Media:**
- Bảng so sánh:
  - Paper gốc
  - Đồ án nhóm

**Ghi chú nói:**
- Nói rõ 9x9 là stress-test, không phải kết luận chính.

---

## Slide 12. Vì sao không dùng 4x4?

**Title:**  
Vì sao bỏ 4x4 khỏi kết quả chính?

**Nội dung trên slide:**
- 4x4 quá nhỏ, số ràng buộc ít.
- Tỷ lệ giải thành công cao, khó phân biệt năng lực model.
- 6x6 cân bằng hơn:
  - đủ chạy được trong đồ án;
  - đủ tạo áp lực suy luận.
- 9x9 dùng để quan sát khi mở rộng quy mô.

**Media:**
- Biểu đồ/infographic so sánh số ô:
  - 4x4 = 16 ô
  - 6x6 = 36 ô
  - 9x9 = 81 ô

**Ghi chú nói:**
- Slide này giúp trả lời trước câu hỏi “sao không làm đúng y paper 100%?”.

---

## Slide 13. Dữ liệu thực nghiệm

**Title:**  
Tập dữ liệu nhóm sử dụng

**Nội dung trên slide:**
- 7 bài Killer Sudoku:
  - 5 bài 6x6 easy.
  - 2 bài 9x9 hard.
- Mỗi puzzle gồm:
  - grid ban đầu;
  - nghiệm chuẩn;
  - danh sách cage;
  - tổng mục tiêu của từng cage.

**Media:**
- Bảng dataset:
  - Puzzle ID
  - Size
  - Difficulty
  - Number of cages
- Trích một đoạn JSON ngắn.

**Ghi chú nói:**
- Nhấn mạnh có nghiệm chuẩn nên có thể chấm tự động.

---

## Slide 14. Pipeline thực nghiệm

**Title:**  
Pipeline đánh giá tự động

**Nội dung trên slide:**
- Data Loader.
- Prompt Builder.
- LLM API.
- JSON Parser.
- Validator.
- Result Log.

**Media:**
- Sơ đồ:
  `Puzzle JSON -> Prompt -> LLM -> Parser -> Validator -> Log`

**Ghi chú nói:**
- Đây là phần “thực nghiệm thật” của đồ án.

---

## Slide 15. Prompt multi-step

**Title:**  
Prompt multi-step của nhóm

**Nội dung trên slide:**
- Một vòng gồm 2 bước:
  - Analysis: phân tích ràng buộc, ứng viên.
  - Fill: chọn đúng một ô để điền.
- Output bắt buộc ở dạng JSON.
- Mục tiêu: giảm trả lời lan man và dễ chấm tự động.

**Media:**
- Snippet JSON:
```json
{
  "cell": "r2c5",
  "value": 1,
  "reasoning": "...",
  "is_certain": true
}
```

**Ghi chú nói:**
- Giải thích vì sao tách analysis/fill: để mô hình “nghĩ” trước rồi mới cam kết.

---

## Slide 16. Tiêu chí chấm điểm

**Title:**  
Chấm điểm và dừng phiên chạy

**Nội dung trên slide:**
- Thành công: grid cuối trùng nghiệm chuẩn.
- Thất bại: model điền một giá trị sai.
- Với 6x6:
  - lưới trống có 36 ô cần điền.
- Với 9x9:
  - lưới trống có 81 ô cần điền.
- Log lưu từng bước để phân tích.

**Media:**
- Flow:
  `Model move -> Update board -> Compare solution -> Continue/Stop`

**Ghi chú nói:**
- Nhấn mạnh hệ thống không “chấm cảm tính”; có ground truth.

---

## Slide 17. Kết quả tổng hợp

**Title:**  
Kết quả multi-step

**Nội dung trên slide:**
- Gemini 2.5 Flash:
  - 6x6: 4/5 đúng.
  - 9x9: 0/2 đúng.
- Gemini 2.5 Pro:
  - 6x6: 4/5 đúng.
  - 9x9: 0/2 đúng.
- Toàn bộ tập: 4/7 cho mỗi model.

**Media:**
- Bảng kết quả chính.
- Biểu đồ `benchmark_results_comparison.png`.

**Ghi chú nói:**
- Nói rõ: kết luận chính dựa trên 6x6; 9x9 là quan sát mở rộng.

---

## Slide 18. Phân tích kết quả 6x6

**Title:**  
6x6: mô hình giải được phần lớn bài

**Nội dung trên slide:**
- Cả hai model đạt 80% trên tập 6x6.
- Multi-step giúp mô hình đi theo từng quyết định nhỏ.
- Các bài thành công thường cần khoảng 36 bước.
- Một lỗi sớm có thể làm cả phiên thất bại.

**Media:**
- Bar chart solve rate 6x6.
- Bảng nhỏ: Flash 4/5, Pro 4/5.

**Ghi chú nói:**
- Đây là kết quả tích cực nhất của nhóm.

---

## Slide 19. Phân tích kết quả 9x9

**Title:**  
9x9: khó hơn rõ rệt

**Nội dung trên slide:**
- Cả hai model thất bại sớm trên 2 bài 9x9.
- Lưới tăng từ 36 lên 81 ô.
- Số chữ số hợp lệ tăng từ 6 lên 9.
- Số cage và tổ hợp ràng buộc tăng.
- Pipeline hiện tại tối ưu chủ yếu cho 6x6.

**Media:**
- Infographic tăng quy mô:
  - 6x6: 36 ô
  - 9x9: 81 ô
- Có thể dùng bảng số bước fail:
  - Flash: 3 và 1 bước
  - Pro: 2 và 3 bước

**Ghi chú nói:**
- Không nói “Gemini không giải được 9x9 nói chung”; chỉ nói trong cấu hình nhóm thì chưa ổn định.

---

## Slide 20. Phân tích lỗi

**Title:**  
Mô hình sai như thế nào?

**Nội dung trên slide:**
- Lỗi chính trong log: Incorrect Solution.
- Nguyên nhân thường gặp:
  - bỏ sót ràng buộc toàn cục;
  - xem giả định chưa chắc chắn là bước bắt buộc;
  - khó duy trì ứng viên của nhiều ô;
  - lỗi sớm lan sang các bước sau.

**Media:**
- Bảng lỗi:
  - Error type
  - Mô tả
  - Ví dụ ngắn từ log
- Nếu có thời gian, chèn một log sai cụ thể.

**Ghi chú nói:**
- Đây là phần rất quan trọng để chứng minh nhóm không chỉ chạy số liệu mà còn phân tích.

---

## Slide 21. So sánh với paper gốc

**Title:**  
Kết quả nhóm phù hợp với nhận định của Sudoku-Bench

**Nội dung trên slide:**
- LLM có thể làm tốt ở bài nhỏ/vừa.
- Khi ràng buộc nhiều hơn, mô hình dễ mất nhất quán.
- Lập luận nghe hợp lý không đảm bảo đúng hình thức.
- Cần benchmark có nghiệm kiểm chứng tự động.

**Media:**
- Bảng:
  - Nhận định paper
  - Quan sát của nhóm

**Ghi chú nói:**
- Kết nối lại với câu hỏi ban đầu: LLM suy luận được, nhưng còn giới hạn rõ.

---

## Slide 22. Kết luận và hướng phát triển

**Title:**  
Kết luận

**Nội dung trên slide:**
- Nhóm đã tái hiện rút gọn Sudoku-Bench trên Killer Sudoku.
- Xây dựng pipeline tự động và log từng bước.
- 6x6: cả hai model đạt 4/5.
- 9x9: thất bại sớm trong cấu hình hiện tại.
- Hướng phát triển:
  - mở rộng dataset;
  - hỗ trợ 9x9 tốt hơn;
  - thêm model khác;
  - kết hợp symbolic solver.

**Media:**
- Sơ đồ hướng phát triển:
  `LLM + Symbolic Solver -> Neuro-Symbolic reasoning`

**Ghi chú nói:**
- Kết thúc bằng thông điệp: LLM có tiềm năng, nhưng CSP vẫn là bài kiểm tra khó và cần đánh giá nghiêm ngặt.

---

## Slide dự phòng A. Thành viên và phân công

**Title:**  
Phân công công việc

**Nội dung trên slide:**
- Thành viên 1: API integration / pipeline.
- Thành viên 2: dataset / evaluator.
- Thành viên 3: prompt engineering / testing.
- Thành viên 4: paper / report / slide / analysis.

**Media:**
- Bảng phân công.

**Ghi chú nói:**
- Dùng nếu thầy hỏi hoặc cần slide phụ.

---

## Slide dự phòng B. Một ví dụ log multi-step

**Title:**  
Ví dụ một bước suy luận của model

**Nội dung trên slide:**
- Cell được chọn.
- Giá trị điền.
- Lý do model đưa ra.
- Board sau khi cập nhật.
- Hệ thống kiểm tra đúng/sai.

**Media:**
- Trích từ file log JSON.
- Có thể chọn puzzle 1 vì có lời giải thành công.

**Ghi chú nói:**
- Dùng để demo pipeline nếu còn thời gian.

---

## Media cần chuẩn bị

1. Logo UIT: `bao-cao-latex/uit.png`.
2. Ảnh hoặc screenshot paper Sudoku-Bench.
3. Hình minh họa Sudoku chuẩn.
4. Hình minh họa Killer Sudoku có cage.
5. Sơ đồ CSP: Variables - Domains - Constraints.
6. Sơ đồ pipeline.
7. Snippet JSON puzzle.
8. Snippet JSON output của model.
9. Biểu đồ `cs106/outputs/benchmark_results_comparison.png`.
10. Biểu đồ `cs106/outputs/advanced_analysis.png`.
11. Bảng kết quả 6x6/9x9.
12. Một log mẫu thành công hoặc thất bại.

---

## Gợi ý chia người thuyết trình

- **Người 1:** Slide 1-5, giới thiệu vấn đề và CSP.
- **Người 2:** Slide 6-10, Sudoku variants và paper gốc.
- **Người 3:** Slide 11-16, phạm vi tái hiện và pipeline.
- **Người 4:** Slide 17-22, kết quả, phân tích lỗi và kết luận.

