from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


def find_repo_root(start: Path | None = None) -> Path:
    cur = (start or Path.cwd()).resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / "cs106").exists() and (candidate / "documents").exists():
            return candidate
    return cur


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def to_int(value: Any) -> int | None:
    if value in (None, "", "."):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def normalize_board(board: Any) -> list[list[int | None]]:
    if not isinstance(board, list):
        return []
    normalized: list[list[int | None]] = []
    for row in board:
        if not isinstance(row, list):
            return []
        normalized.append([to_int(cell) for cell in row])
    return normalized


def font(size: int, bold: bool = False):
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        try:
            if Path(candidate).exists():
                return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def infer_block_shape(size: int) -> tuple[int, int]:
    if size == 4:
        return 2, 2
    if size == 6:
        return 2, 3
    if size == 9:
        return 3, 3
    return 1, size


def board_size(board: list[list[int | None]], fallback: int | None = None) -> int:
    if board:
        return len(board)
    if fallback:
        return fallback
    return 9


def mismatch_cells(
    prediction: list[list[int | None]],
    solution: list[list[int | None]],
) -> set[tuple[int, int]]:
    mismatches: set[tuple[int, int]] = set()
    for r, row in enumerate(solution):
        for c, sol_value in enumerate(row):
            pred_value = prediction[r][c] if r < len(prediction) and c < len(prediction[r]) else None
            if pred_value != sol_value:
                mismatches.add((r, c))
    return mismatches


def draw_board(
    board: list[list[int | None]],
    *,
    title: str,
    subtitle: str = "",
    highlight_cells: set[tuple[int, int]] | None = None,
    highlight_label: str | None = None,
    cages: list[dict[str, Any]] | None = None,
    output_path: Path,
    cell_size: int = 86,
) -> Path:
    size = board_size(board)
    block_r, block_c = infer_block_shape(size)
    margin = 46
    title_h = 105 if subtitle else 82
    caption_h = 54 if highlight_label else 28
    grid_px = cell_size * size
    width = grid_px + margin * 2
    height = title_h + grid_px + caption_h + margin

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    title_font = font(34, bold=True)
    subtitle_font = font(18)
    digit_font = font(int(cell_size * 0.46), bold=True)
    cage_font = font(max(13, int(cell_size * 0.16)), bold=True)
    note_font = font(18)

    draw.text((margin, 26), title, fill="#111111", font=title_font)
    if subtitle:
        draw.text((margin, 70), subtitle, fill="#555555", font=subtitle_font)

    x0 = margin
    y0 = title_h
    highlights = highlight_cells or set()
    for r in range(size):
        for c in range(size):
            x1 = x0 + c * cell_size
            y1 = y0 + r * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            fill = "#FADDDD" if (r, c) in highlights else "#FFFFFF"
            draw.rectangle([x1, y1, x2, y2], fill=fill)
            value = board[r][c] if r < len(board) and c < len(board[r]) else None
            if value not in (None, 0):
                text = str(value)
                tw, th = text_size(draw, text, digit_font)
                draw.text(
                    (x1 + (cell_size - tw) / 2, y1 + (cell_size - th) / 2 - 4),
                    text,
                    fill="#111111",
                    font=digit_font,
                )

    if cages:
        cage_color = "#7A3E9D"
        cage_width = max(3, cell_size // 22)
        label_pad = max(5, cell_size // 14)
        for cage in cages:
            cells = [tuple(cell) for cell in cage.get("cells", [])]
            cell_set = set(cells)
            if not cell_set:
                continue

            for r, c in cell_set:
                x1 = x0 + c * cell_size
                y1 = y0 + r * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                if (r - 1, c) not in cell_set:
                    draw.line([x1, y1, x2, y1], fill=cage_color, width=cage_width)
                if (r + 1, c) not in cell_set:
                    draw.line([x1, y2, x2, y2], fill=cage_color, width=cage_width)
                if (r, c - 1) not in cell_set:
                    draw.line([x1, y1, x1, y2], fill=cage_color, width=cage_width)
                if (r, c + 1) not in cell_set:
                    draw.line([x2, y1, x2, y2], fill=cage_color, width=cage_width)

            label_cell = min(cell_set)
            lr, lc = label_cell
            label = str(cage.get("sum", ""))
            if label:
                draw.text(
                    (x0 + lc * cell_size + label_pad, y0 + lr * cell_size + label_pad),
                    label,
                    fill=cage_color,
                    font=cage_font,
                )

    thin = "#B8B8B8"
    thick = "#111111"
    for i in range(size + 1):
        x = x0 + i * cell_size
        line_color = thick if i % block_c == 0 else thin
        line_w = 4 if i % block_c == 0 else 1
        draw.line([x, y0, x, y0 + grid_px], fill=line_color, width=line_w)

    for i in range(size + 1):
        y = y0 + i * cell_size
        line_color = thick if i % block_r == 0 else thin
        line_w = 4 if i % block_r == 0 else 1
        draw.line([x0, y, x0 + grid_px, y], fill=line_color, width=line_w)

    if highlight_label:
        draw.rectangle([margin, y0 + grid_px + 22, margin + 24, y0 + grid_px + 46], fill="#FADDDD")
        draw.text((margin + 34, y0 + grid_px + 20), highlight_label, fill="#333333", font=note_font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    return output_path.resolve()


def render_result(result_path: Path, output_dir: Path | None = None, cell_size: int = 86) -> list[Path]:
    repo_root = find_repo_root(result_path)
    result = load_json(result_path)
    puzzle_id = result.get("puzzle_id") or result.get("id")
    if puzzle_id is None:
        raise ValueError("Cannot infer puzzle_id from result file.")

    dataset_path = repo_root / "cs106" / "dataset" / f"puzzle_{int(puzzle_id):02d}.json"
    dataset = load_json(dataset_path) if dataset_path.exists() else {}

    prediction = normalize_board(result.get("prediction") or result.get("final_board"))
    solution = normalize_board(result.get("solution") or dataset.get("solution"))
    if not prediction:
        raise ValueError(f"No prediction/final_board found in {result_path}")
    if not solution:
        raise ValueError(f"No solution found in result or dataset for puzzle {puzzle_id}")

    model = result.get("model", "unknown-model")
    status = result.get("status") or result.get("final_status") or "Unknown"
    size = board_size(solution, result.get("grid_size"))
    output_dir = output_dir or repo_root / "cs106" / "evaluation" / "sudoku_renders"
    stem = f"puzzle_{int(puzzle_id):02d}_{str(model).replace('/', '-')}"
    mismatches = mismatch_cells(prediction, solution)
    cages = dataset.get("cages") or None

    subtitle = f"Puzzle {int(puzzle_id):02d} | {size}x{size} | {model} | {status}"
    saved = [
        draw_board(
            prediction,
            title="Model Prediction",
            subtitle=subtitle,
            cages=cages,
            output_path=output_dir / f"{stem}_prediction.png",
            cell_size=cell_size,
        ),
        draw_board(
            solution,
            title="Ground Truth Solution",
            subtitle=f"Puzzle {int(puzzle_id):02d} | {size}x{size}",
            cages=cages,
            output_path=output_dir / f"{stem}_solution.png",
            cell_size=cell_size,
        ),
        draw_board(
            prediction,
            title="Prediction vs Solution",
            subtitle=subtitle,
            highlight_cells=mismatches,
            highlight_label=f"Mismatched cells: {len(mismatches)}",
            cages=cages,
            output_path=output_dir / f"{stem}_comparison.png",
            cell_size=cell_size,
        ),
    ]
    return saved


def parse_cell(cell: Any) -> tuple[int, int] | None:
    if not isinstance(cell, str):
        return None
    cell = cell.strip().lower()
    if not cell.startswith("r") or "c" not in cell:
        return None
    try:
        row_text, col_text = cell[1:].split("c", 1)
        return int(row_text) - 1, int(col_text) - 1
    except ValueError:
        return None


def render_log_step(
    log_path: Path,
    *,
    step_number: int,
    output_dir: Path | None = None,
    cell_size: int = 86,
) -> list[Path]:
    repo_root = find_repo_root(log_path)
    data = load_json(log_path)
    puzzle_id = data.get("puzzle_id") or data.get("id")
    if puzzle_id is None:
        raise ValueError("Cannot infer puzzle_id from log file.")

    dataset_path = repo_root / "cs106" / "dataset" / f"puzzle_{int(puzzle_id):02d}.json"
    dataset = load_json(dataset_path) if dataset_path.exists() else {}
    cages = dataset.get("cages") or None
    execution_log = data.get("execution_log") or []
    entry = next((item for item in execution_log if item.get("step") == step_number), None)
    if entry is None:
        raise ValueError(f"Step {step_number} not found in {log_path}")

    board = normalize_board(entry.get("board_state"))
    if not board:
        raise ValueError(f"Step {step_number} does not contain board_state.")

    model = data.get("model", "unknown-model")
    cell = entry.get("chosen_cell")
    value = entry.get("value")
    parsed_cell = parse_cell(cell)
    highlights = {parsed_cell} if parsed_cell is not None else set()
    size = board_size(board, data.get("grid_size") or dataset.get("grid_size"))

    output_dir = output_dir or repo_root / "cs106" / "evaluation" / "sudoku_renders"
    stem = f"puzzle_{int(puzzle_id):02d}_{str(model).replace('/', '-')}_step_{step_number:02d}"
    subtitle = f"Puzzle {int(puzzle_id):02d} | {size}x{size} | {model} | step {step_number}: {cell} = {value}"
    saved = [
        draw_board(
            board,
            title="Multi-Step Successful Placement",
            subtitle=subtitle,
            highlight_cells=highlights,
            highlight_label=f"Chosen move: {cell} = {value}",
            cages=cages,
            output_path=output_dir / f"{stem}_board.png",
            cell_size=cell_size,
        )
    ]

    reasoning = entry.get("reasoning") or ""
    reasoning_path = output_dir / f"{stem}_reasoning.txt"
    reasoning_path.parent.mkdir(parents=True, exist_ok=True)
    reasoning_path.write_text(str(reasoning), encoding="utf-8")
    saved.append(reasoning_path.resolve())
    return saved


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Sudoku prediction/solution/comparison images from a JSON result file.")
    parser.add_argument("result_json", type=Path, help="Path to result_puzzle_XX.json or log_puzzle_XX.json")
    parser.add_argument("--out", type=Path, default=None, help="Output directory. Default: cs106/evaluation/sudoku_renders")
    parser.add_argument("--cell-size", type=int, default=86, help="Cell size in pixels.")
    parser.add_argument("--step", type=int, default=None, help="Render a specific multi-step log entry instead of final prediction/solution.")
    args = parser.parse_args()

    if args.step is not None:
        saved = render_log_step(args.result_json.resolve(), step_number=args.step, output_dir=args.out, cell_size=args.cell_size)
    else:
        saved = render_result(args.result_json.resolve(), args.out, args.cell_size)
    print("Saved:")
    for path in saved:
        print(f"- {path}")


if __name__ == "__main__":
    main()
