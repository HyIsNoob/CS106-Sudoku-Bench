# CS106-Sudoku-Bench

## Thông tin đồ án

- Trường: Trường Đại học Công nghệ Thông tin - ĐHQG TP.HCM
- Khoa: Khoa Khoa học Máy tính
- Môn học: CS106 - Trí tuệ nhân tạo
- Giảng viên hướng dẫn: Lương Ngọc Hoàng
- Nhóm thực hiện: Nhóm 4
- Đề tài: Tái hiện và đánh giá khả năng suy luận của LLM thông qua Sudoku-Bench
- Bài báo tham chiếu: *Sudoku-Bench: Evaluating Creative Reasoning with Sudoku Variants*
- Thời gian thực hiện: 05/2026

## Thành viên

| STT | Họ và tên | MSSV | Vai trò |
|---:|---|---|---|
| 1 | Đặng Anh Khoa | 23520732 | Trưởng nhóm |
| 2 | Phạm Minh Bảo Khang | 23520705 | Thành viên |
| 3 | Nguyễn Khang Hy | 23520662 | Thành viên |
| 4 | Phan Công Nam | 23520986 | Thành viên |

Đồ án cuối kỳ môn CS106 - Trí tuệ nhân tạo. Nhóm tái hiện rút gọn bài báo *Sudoku-Bench: Evaluating Creative Reasoning with Sudoku Variants* bằng cách đánh giá khả năng suy luận của các mô hình Gemini trên Killer Sudoku.

Trọng tâm của repo không phải là xây dựng solver CSP để giải hộ mô hình. Hệ thống chỉ chuẩn bị dữ liệu, tạo prompt, gọi LLM, ghi log, kiểm chứng lời giải bằng nghiệm chuẩn và tổng hợp kết quả thực nghiệm.

## Nội dung thực nghiệm

- Bài toán: Killer Sudoku.
- Dataset: 5 bài 6x6 easy và 2 bài 9x9 hard.
- Mô hình: Gemini 2.5 Flash, Gemini 2.5 Pro, Gemini 3.1 Flash Lite, Gemini 3.5 Flash.
- Chế độ chạy: single-prompt và multi-step.
- Chỉ số đánh giá: solve rate, final status, error type, average correct placements, số bước và thời gian chạy nếu có log.

## Cấu trúc thư mục

```text
cs106/
  6x6/                 Notebook chạy benchmark 6x6
  9x9/                 Notebook chạy benchmark 9x9
  dataset/             Puzzle JSON đã chuẩn hóa
  outputs/             Kết quả và log từ các lần gọi mô hình
  evaluation/          Script/notebook tổng hợp kết quả, xuất CSV và biểu đồ
  map/                 File puzzle gốc
  prompts/             Prompt rời nếu cần tham khảo

demo/                  Web demo trực quan quá trình multi-step
documents/             Paper, slide content, kế hoạch trình bày
bao-cao-latex/         Báo cáo LaTeX và PDF đã build
```

## Cài đặt nhanh

Python 3.12 được dùng trong quá trình chạy notebook và evaluation.

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install google-genai pydantic pandas matplotlib pillow nbformat nbclient
```

Các notebook gọi Gemini cần cấu hình Google GenAI/Vertex AI credential trên máy chạy. Không commit API key hoặc credential vào repo.

## Chạy benchmark

Các notebook chính:

```text
cs106/6x6/single_prompt_eval.ipynb
cs106/6x6/api_llm.ipynb
cs106/9x9/single_prompt_eval_9x9.ipynb
cs106/9x9/api_llm_9x9.ipynb
```

Kết quả sau khi chạy được lưu trong `cs106/outputs/`, phân theo model, chế độ single-prompt hoặc multi-step.

## Tổng hợp kết quả

Chạy evaluation từ thư mục gốc repo:

```powershell
python cs106/evaluation/evaluate_results.py
```

Output được ghi vào:

```text
cs106/evaluation/eval_outputs/
```

Thư mục này chứa các bảng CSV và biểu đồ dùng cho báo cáo/slide, ví dụ `summary_by_model_mode.csv`, `all_results.csv`, `solve_rate_by_model_mode.png`, `error_type_summary.png`.

Để render hình minh họa bảng dự đoán, nghiệm chuẩn và ô sai khác từ một file kết quả:

```powershell
python cs106/evaluation/render_sudoku_result.py cs106/outputs/gemini-2.5/single_prompt/flash/result_puzzle_01.json
```

## Demo web

Demo là trang web tĩnh trong thư mục `demo/`. Nếu cần build lại CSS:

```powershell
cd demo
npm install
npm run build
```

Để mở demo bằng local server:

```powershell
cd demo
python -m http.server 8000
```

Sau đó mở `http://localhost:8000/src/`.

## Báo cáo và slide

- Báo cáo LaTeX: `bao-cao-latex/main.tex`
- File PDF đã build: `bao-cao-latex/main.pdf`
- Nội dung slide: `documents/CS106-NoiDung-Slide-BaoCao.md`
- Link Canva slide: https://canva.link/1ulwst58droe42i

Build lại báo cáo bằng XeLaTeX:

```powershell
cd bao-cao-latex
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

Chạy hai lần để cập nhật mục lục và cross-reference.
