from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path
from typing import Any

import pandas as pd


PAPER_ERROR_TYPES = {
    "incorrect solution": "Incorrect Solution",
    "incorrect": "Incorrect Solution",
    "wrong": "Incorrect Solution",
    "surrender": "Surrender",
    "give up": "Surrender",
    "missing information": "Missing Information",
    "claimed contradiction": "Claimed Contradiction",
    "contradiction": "Claimed Contradiction",
    "no reasoning trace": "No Reasoning Trace",
    "no certain move": "No Certain Move",
    "parse": "Invalid Output / Format Error",
    "json": "Invalid Output / Format Error",
    "format": "Invalid Output / Format Error",
    "validation": "Incorrect Solution",
}


def find_repo_root(start: Path | None = None) -> Path:
    cur = (start or Path.cwd()).resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / "cs106").exists() and (candidate / "documents").exists():
            return candidate
    return cur


def find_outputs_dir(repo_root: Path | None = None) -> Path:
    repo_root = repo_root or find_repo_root()
    candidates = [
        Path.cwd() / "outputs",
        Path.cwd() / "cs106" / "outputs",
        repo_root / "cs106" / "outputs",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    raise FileNotFoundError("Cannot find cs106/outputs. Set OUTPUT_DIRS manually in the notebook.")


def find_dataset_dir(repo_root: Path | None = None) -> Path | None:
    repo_root = repo_root or find_repo_root()
    candidates = [
        Path.cwd() / "dataset",
        Path.cwd() / "cs106" / "dataset",
        repo_root / "cs106" / "dataset",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return None


def default_export_dir(repo_root: Path | None = None) -> Path:
    repo_root = repo_root or find_repo_root()
    candidates = [
        Path.cwd() / "eval_outputs",
        Path(__file__).resolve().parent / "eval_outputs",
        repo_root / "cs106" / "evaluation" / "eval_outputs",
    ]
    for candidate in candidates:
        parent = candidate.parent
        if parent.exists():
            return candidate
    return Path.cwd() / "eval_outputs"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_dataset(dataset_dir: Path | None) -> dict[int, dict[str, Any]]:
    if dataset_dir is None:
        return {}

    puzzles: dict[int, dict[str, Any]] = {}
    for path in sorted(dataset_dir.glob("puzzle_*.json")):
        try:
            data = load_json(path)
        except Exception:
            continue
        puzzle_id = data.get("id") or data.get("puzzle_id")
        if puzzle_id is None:
            match = re.search(r"puzzle_(\d+)", path.stem)
            puzzle_id = int(match.group(1)) if match else None
        if puzzle_id is not None:
            puzzles[int(puzzle_id)] = data
    return puzzles


def infer_mode(path: Path) -> str:
    lowered = str(path).lower()
    if "single_prompt" in lowered or "single-prompt" in lowered:
        return "single"
    if "multi_prompt" in lowered or "multi-prompt" in lowered:
        return "multi"
    if path.name.startswith("result_"):
        return "single"
    if path.name.startswith("log_"):
        return "multi"
    return "unknown"


def infer_model_from_path(path: Path) -> str:
    parts = [p.lower() for p in path.parts]
    if "pro" in parts:
        return "gemini-2.5-pro"
    if "lite" in parts:
        return "gemini-3.1-flash-lite"
    if "flash" in parts:
        if "gemini-3.x" in parts or "gemini-3.5" in parts:
            return "gemini-3.5-flash"
        return "gemini-2.5-flash"
    return "unknown"


def normalize_model(model: Any, path: Path) -> str:
    if isinstance(model, str) and model.strip():
        return model.strip()
    return infer_model_from_path(path)


def normalize_status(status: Any) -> str:
    if status is None:
        return "Unknown"
    text = str(status).strip()
    if not text:
        return "Unknown"
    return "Success" if text.lower() == "success" else "Failed" if text.lower() == "failed" else text


def is_success(status: Any) -> bool:
    return str(status).strip().lower() == "success"


def to_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def normalize_board(board: Any) -> list[list[int | None]] | None:
    if not isinstance(board, list):
        return None
    normalized: list[list[int | None]] = []
    for row in board:
        if not isinstance(row, list):
            return None
        normalized.append([to_int(cell) for cell in row])
    return normalized


def board_shape(board: Any) -> tuple[int, int] | None:
    normalized = normalize_board(board)
    if not normalized:
        return None
    return len(normalized), len(normalized[0]) if normalized[0] else 0


def count_solution_cells(solution: Any) -> int | None:
    normalized = normalize_board(solution)
    if not normalized:
        return None
    return sum(1 for row in normalized for cell in row if cell is not None)


def count_empty_cells(initial_board: Any, fallback_size: int | None = None) -> int | None:
    normalized = normalize_board(initial_board)
    if normalized:
        return sum(1 for row in normalized for cell in row if cell in (None, 0))
    if fallback_size:
        return fallback_size * fallback_size
    return None


def compare_boards(
    prediction: Any,
    solution: Any,
    initial_board: Any | None = None,
    only_filled_prediction: bool = False,
) -> tuple[int | None, int | None, float | None, list[str]]:
    pred = normalize_board(prediction)
    sol = normalize_board(solution)
    initial = normalize_board(initial_board) if initial_board is not None else None
    if not pred or not sol:
        return None, None, None, []

    correct = 0
    total = 0
    mismatches: list[str] = []
    for r, sol_row in enumerate(sol):
        for c, sol_value in enumerate(sol_row):
            if r >= len(pred) or c >= len(pred[r]):
                mismatches.append(f"r{r + 1}c{c + 1}: missing != {sol_value}")
                total += 1
                continue

            pred_value = pred[r][c]
            if only_filled_prediction and pred_value in (None, 0):
                continue
            if initial and r < len(initial) and c < len(initial[r]) and initial[r][c] not in (None, 0):
                continue

            total += 1
            if pred_value == sol_value:
                correct += 1
            elif len(mismatches) < 10:
                mismatches.append(f"r{r + 1}c{c + 1}: {pred_value} != {sol_value}")

    accuracy = correct / total if total else None
    return correct, total, accuracy, mismatches


def parse_cell(cell: Any) -> tuple[int, int] | None:
    if not isinstance(cell, str):
        return None
    match = re.fullmatch(r"\s*r(\d+)c(\d+)\s*", cell, flags=re.IGNORECASE)
    if not match:
        return None
    return int(match.group(1)) - 1, int(match.group(2)) - 1


def canonical_error_type(
    error_type: Any,
    *,
    status: str,
    mode: str,
    prediction: Any = None,
    validation_errors: Any = None,
    error_message: Any = None,
) -> str:
    if is_success(status):
        return "Success"

    candidates = [error_type, error_message]
    if validation_errors:
        candidates.append("validation")
    if prediction is None and mode == "single":
        candidates.append("format")

    joined = " ".join(str(x) for x in candidates if x not in (None, "", "None")).lower()
    if not joined:
        return "Incorrect Solution"

    for key, canonical in PAPER_ERROR_TYPES.items():
        if key in joined:
            return canonical
    return str(error_type or error_message or "Other Failure")


def get_dataset_field(dataset: dict[int, dict[str, Any]], puzzle_id: int | None, field: str) -> Any:
    if puzzle_id is None:
        return None
    return dataset.get(int(puzzle_id), {}).get(field)


def infer_grid_size(data: dict[str, Any], dataset: dict[int, dict[str, Any]], puzzle_id: int | None) -> int | None:
    grid_size = data.get("grid_size") or get_dataset_field(dataset, puzzle_id, "grid_size")
    if grid_size:
        return int(grid_size)

    for key in ("solution", "prediction", "final_board", "puzzle"):
        shape = board_shape(data.get(key) or get_dataset_field(dataset, puzzle_id, key))
        if shape:
            return shape[0]
    return None


def get_solution(data: dict[str, Any], dataset: dict[int, dict[str, Any]], puzzle_id: int | None) -> Any:
    return data.get("solution") or get_dataset_field(dataset, puzzle_id, "solution")


def get_initial_board(data: dict[str, Any], dataset: dict[int, dict[str, Any]], puzzle_id: int | None) -> Any:
    return data.get("puzzle") or get_dataset_field(dataset, puzzle_id, "puzzle")


def multi_correct_placements(
    data: dict[str, Any],
    dataset: dict[int, dict[str, Any]],
    puzzle_id: int | None,
    grid_size: int | None,
    status: str,
) -> tuple[int | None, int | None, float | None]:
    solution = get_solution(data, dataset, puzzle_id)
    initial_board = get_initial_board(data, dataset, puzzle_id)
    target = count_empty_cells(initial_board, grid_size)

    if is_success(status) and target is not None:
        return target, target, 1.0

    final_board = data.get("final_board")
    if final_board is not None and solution is not None:
        correct, total, accuracy, _ = compare_boards(
            final_board,
            solution,
            initial_board=initial_board,
            only_filled_prediction=True,
        )
        denominator = target if target is not None else total
        placement_accuracy = correct / denominator if correct is not None and denominator else None
        return correct, denominator, placement_accuracy

    log = data.get("execution_log") or []
    seen: dict[str, int] = {}
    solution_board = normalize_board(solution)
    for entry in log:
        if not isinstance(entry, dict):
            continue
        cell = entry.get("chosen_cell")
        value = to_int(entry.get("value"))
        parsed = parse_cell(cell)
        if parsed is None or value is None:
            continue
        r, c = parsed
        if solution_board and r < len(solution_board) and c < len(solution_board[r]):
            if value == solution_board[r][c]:
                seen[str(cell).lower()] = value
        else:
            step_error = str(entry.get("error_type") or "None").lower()
            if step_error in ("", "none"):
                seen[str(cell).lower()] = value

    denominator = target if target is not None else (grid_size * grid_size if grid_size else None)
    placement_accuracy = len(seen) / denominator if denominator else None
    return len(seen), denominator, placement_accuracy


def parse_result_file(path: Path, outputs_dir: Path, dataset: dict[int, dict[str, Any]]) -> dict[str, Any] | None:
    try:
        data = load_json(path)
    except Exception as exc:
        return {
            "file": str(path),
            "relative_path": str(path),
            "mode": infer_mode(path),
            "model": infer_model_from_path(path),
            "status": "Failed",
            "is_solved": False,
            "error_type": "Invalid Output / Format Error",
            "error_message": str(exc),
        }

    mode = infer_mode(path)
    puzzle_id = data.get("puzzle_id") or data.get("id")
    puzzle_id = int(puzzle_id) if puzzle_id is not None else None
    model = normalize_model(data.get("model"), path)
    grid_size = infer_grid_size(data, dataset, puzzle_id)
    difficulty = data.get("difficulty") or get_dataset_field(dataset, puzzle_id, "difficulty")
    solution = get_solution(data, dataset, puzzle_id)
    initial_board = get_initial_board(data, dataset, puzzle_id)

    if mode == "single":
        status = normalize_status(data.get("status"))
        correct_cells, total_cells, cell_accuracy, mismatches = compare_boards(data.get("prediction"), solution)
        correct_placements = None
        placement_denominator = None
        placement_accuracy = None
        total_steps = None
    else:
        status = normalize_status(data.get("final_status") or data.get("status"))
        total_steps = data.get("total_steps")
        correct_placements, placement_denominator, placement_accuracy = multi_correct_placements(
            data,
            dataset,
            puzzle_id,
            grid_size,
            status,
        )
        correct_cells, total_cells, cell_accuracy, mismatches = compare_boards(
            data.get("final_board"),
            solution,
            initial_board=initial_board,
            only_filled_prediction=True,
        )

    error_type = canonical_error_type(
        data.get("error_type"),
        status=status,
        mode=mode,
        prediction=data.get("prediction"),
        validation_errors=data.get("validation_errors"),
        error_message=data.get("error_message"),
    )

    try:
        relative_path = path.relative_to(outputs_dir)
    except ValueError:
        relative_path = path

    return {
        "file": path.name,
        "relative_path": str(relative_path).replace("\\", "/"),
        "mode": mode,
        "puzzle_id": puzzle_id,
        "difficulty": difficulty,
        "grid_size": grid_size,
        "model": model,
        "status": status,
        "is_solved": is_success(status),
        "error_type": error_type,
        "total_steps": total_steps,
        "correct_placements": correct_placements,
        "placement_denominator": placement_denominator,
        "placement_accuracy": placement_accuracy,
        "correct_cells": correct_cells,
        "total_cells": total_cells,
        "cell_accuracy": cell_accuracy,
        "time_seconds": data.get("time_seconds") or data.get("execution_time") or data.get("elapsed_seconds"),
        "time_minutes": (data.get("time_seconds") or data.get("execution_time") or data.get("elapsed_seconds") or 0) / 60
        if (data.get("time_seconds") or data.get("execution_time") or data.get("elapsed_seconds")) is not None
        else None,
        "log_entries": len(data.get("execution_log") or []),
        "mismatch_preview": "; ".join(mismatches[:5]),
    }


def collect_results(
    output_dirs: list[Path] | None = None,
    dataset_dir: Path | None = None,
) -> pd.DataFrame:
    repo_root = find_repo_root()
    output_dirs = output_dirs or [find_outputs_dir(repo_root)]
    dataset = load_dataset(dataset_dir or find_dataset_dir(repo_root))

    records: list[dict[str, Any]] = []
    seen_paths: set[Path] = set()
    for output_dir in output_dirs:
        output_dir = Path(output_dir).resolve()
        if not output_dir.exists():
            continue
        for path in sorted(output_dir.rglob("*.json")):
            if path in seen_paths:
                continue
            seen_paths.add(path)
            record = parse_result_file(path, output_dir, dataset)
            if record:
                records.append(record)

    df = pd.DataFrame(records)
    if df.empty:
        return df

    ordered_cols = [
        "mode",
        "grid_size",
        "puzzle_id",
        "difficulty",
        "model",
        "status",
        "is_solved",
        "error_type",
        "correct_placements",
        "placement_denominator",
        "placement_accuracy",
        "total_steps",
        "correct_cells",
        "total_cells",
        "cell_accuracy",
        "time_seconds",
        "time_minutes",
        "log_entries",
        "relative_path",
        "mismatch_preview",
    ]
    return df[[col for col in ordered_cols if col in df.columns]].sort_values(
        ["grid_size", "mode", "model", "puzzle_id", "relative_path"],
        na_position="last",
    )


def build_summary_tables(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    if df.empty:
        return {}

    data = df.copy()
    data["solve_rate_pct"] = data["is_solved"].astype(float) * 100

    summary = (
        data.groupby(["grid_size", "mode", "model"], dropna=False)
        .agg(
            n_runs=("is_solved", "size"),
            solved=("is_solved", "sum"),
            solve_rate_pct=("solve_rate_pct", "mean"),
            avg_correct_placements=("correct_placements", "mean"),
            avg_placement_accuracy_pct=("placement_accuracy", lambda s: s.dropna().mean() * 100 if not s.dropna().empty else pd.NA),
            avg_total_steps=("total_steps", "mean"),
            avg_time_seconds=("time_seconds", "mean"),
            total_time_minutes=("time_minutes", "sum"),
        )
        .reset_index()
        .sort_values(["grid_size", "mode", "solve_rate_pct", "model"], ascending=[True, True, False, True])
    )

    per_puzzle = data.assign(
        outcome=data.apply(
            lambda row: "Success"
            if row["is_solved"]
            else f"Failed: {row['error_type']}",
            axis=1,
        )
    )[
        [
            "grid_size",
            "puzzle_id",
            "difficulty",
            "mode",
            "model",
            "outcome",
            "correct_placements",
            "total_steps",
            "time_seconds",
            "relative_path",
        ]
    ].sort_values(["grid_size", "puzzle_id", "mode", "model"])

    multi_correct = (
        data[data["mode"] == "multi"]
        .groupby(["grid_size", "model"], dropna=False)
        .agg(
            n_runs=("is_solved", "size"),
            solved=("is_solved", "sum"),
            solve_rate_pct=("solve_rate_pct", "mean"),
            avg_correct_placements=("correct_placements", "mean"),
            median_correct_placements=("correct_placements", "median"),
            max_correct_placements=("correct_placements", "max"),
            avg_steps=("total_steps", "mean"),
        )
        .reset_index()
        .sort_values(["grid_size", "solve_rate_pct", "avg_correct_placements"], ascending=[True, False, False])
    )

    error_summary = (
        data.groupby(["grid_size", "mode", "model", "error_type"], dropna=False)
        .size()
        .reset_index(name="count")
        .sort_values(["grid_size", "mode", "model", "count"], ascending=[True, True, True, False])
    )

    time_summary = (
        data.groupby(["grid_size", "mode", "model"], dropna=False)
        .agg(
            n_with_time=("time_seconds", "count"),
            avg_time_seconds=("time_seconds", "mean"),
            median_time_seconds=("time_seconds", "median"),
            max_time_seconds=("time_seconds", "max"),
            total_time_minutes=("time_minutes", "sum"),
        )
        .reset_index()
        .sort_values(["grid_size", "mode", "avg_time_seconds"], ascending=[True, True, False])
    )

    slowest_runs = data.sort_values("time_seconds", ascending=False, na_position="last").head(15)

    return {
        "all_results": data,
        "summary_by_model_mode_size": summary,
        "per_puzzle_status": per_puzzle,
        "multi_correct_placements": multi_correct,
        "error_summary": error_summary,
        "time_summary": time_summary,
        "slowest_runs": slowest_runs,
    }


def export_tables(tables: dict[str, pd.DataFrame], output_dir: Path | str = "eval_outputs") -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    for name, table in tables.items():
        table.to_csv(output_path / f"{name}.csv", index=False, encoding="utf-8-sig")
    return output_path.resolve()


def _pil_font(size: int, bold: bool = False):
    from PIL import ImageFont

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


def _text_size(draw, text: str, font) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), str(text), font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def _fmt_number(value: Any, suffix: str = "") -> str:
    if pd.isna(value):
        return ""
    value = float(value)
    if abs(value - round(value)) < 1e-9:
        return f"{int(round(value))}{suffix}"
    return f"{value:.1f}{suffix}"


def _wrap_label(label: Any, width: int = 18) -> str:
    return "\n".join(textwrap.wrap(str(label), width=width, break_long_words=False)) or str(label)


def _style_matplotlib_bar_axis(ax, *, rotate: int = 25, wrap_width: int = 18) -> None:
    labels = [_wrap_label(label.get_text(), wrap_width) for label in ax.get_xticklabels()]
    ax.set_xticklabels(labels, rotation=rotate, ha="right", rotation_mode="anchor")
    ax.grid(axis="y", alpha=0.22)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def _draw_grouped_horizontal_bars(
    pivot: pd.DataFrame,
    *,
    title: str,
    subtitle: str,
    x_label: str,
    output_path: Path,
    max_value: float | None = None,
    suffix: str = "",
) -> Path:
    from PIL import Image, ImageDraw

    pivot = pivot.fillna(0)
    colors = ["#3366CC", "#DC3912", "#109618", "#FF9900", "#990099", "#0099C6", "#DD4477", "#66AA00"]
    series = list(pivot.columns)
    rows = list(pivot.index)
    if max_value is None:
        max_value = max(float(pivot.max().max()), 1.0)
    max_value = max(max_value, 1.0)

    width = 1800
    left = 360
    right = 220
    top = 155
    bottom = 80
    bar_h = 22
    bar_gap = 9
    group_gap = 22
    group_h = len(series) * (bar_h + bar_gap) + group_gap
    height = max(720, top + bottom + len(rows) * group_h)
    plot_w = width - left - right

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    title_font = _pil_font(34, bold=True)
    subtitle_font = _pil_font(20)
    label_font = _pil_font(20)
    small_font = _pil_font(17)
    value_font = _pil_font(18, bold=True)

    draw.text((40, 32), title, fill="#111111", font=title_font)
    draw.text((40, 82), subtitle, fill="#555555", font=subtitle_font)

    legend_x = width - right - 460
    legend_y = 35
    for i, name in enumerate(series):
        y = legend_y + i * 27
        draw.rectangle([legend_x, y + 4, legend_x + 22, y + 22], fill=colors[i % len(colors)])
        draw.text((legend_x + 32, y), str(name), fill="#222222", font=small_font)

    axis_y = top - 22
    draw.line([left, axis_y, left + plot_w, axis_y], fill="#CCCCCC", width=1)
    for tick in range(0, 6):
        value = max_value * tick / 5
        x = left + int(plot_w * value / max_value)
        draw.line([x, axis_y - 5, x, height - bottom + 10], fill="#EEEEEE", width=1)
        tick_label = _fmt_number(value, suffix)
        tw, _ = _text_size(draw, tick_label, small_font)
        draw.text((x - tw / 2, axis_y - 30), tick_label, fill="#666666", font=small_font)

    for row_i, row_name in enumerate(rows):
        group_top = top + row_i * group_h
        draw.text((40, group_top + 8), str(row_name), fill="#111111", font=label_font)
        for series_i, name in enumerate(series):
            y = group_top + series_i * (bar_h + bar_gap)
            value = float(pivot.loc[row_name, name])
            bar_w = int(plot_w * value / max_value)
            draw.text((left - 150, y), str(name), fill="#555555", font=small_font)
            draw.rounded_rectangle([left, y, left + bar_w, y + bar_h], radius=5, fill=colors[series_i % len(colors)])
            draw.rectangle([left, y, left + plot_w, y + bar_h], outline="#DDDDDD", width=1)
            draw.text((left + bar_w + 10, y - 2), _fmt_number(value, suffix), fill="#111111", font=value_font)

    draw.text((left, height - 45), x_label, fill="#555555", font=subtitle_font)
    img.save(output_path)
    return output_path.resolve()


def _draw_outcome_heatmap(df: pd.DataFrame, output_path: Path) -> Path:
    from PIL import Image, ImageDraw

    data = df.copy()
    data["row"] = (
        data["grid_size"].astype(str)
        + "x"
        + data["grid_size"].astype(str)
        + " / "
        + data["mode"].astype(str)
        + " / "
        + data["model"].astype(str)
    )
    data["col"] = data["puzzle_id"].astype(int)
    rows = sorted(data["row"].unique())
    cols = sorted(data["col"].unique())
    lookup = {(row["row"], int(row["col"])): bool(row["is_solved"]) for _, row in data.iterrows()}

    cell_w = 92
    cell_h = 46
    left = 480
    top = 150
    width = left + len(cols) * cell_w + 80
    height = top + len(rows) * cell_h + 95

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    title_font = _pil_font(34, bold=True)
    label_font = _pil_font(19)
    small_font = _pil_font(17)
    cell_font = _pil_font(21, bold=True)

    draw.text((40, 32), "Per-puzzle outcome heatmap", fill="#111111", font=title_font)
    draw.text((40, 82), "Green = solved, red = failed, gray = missing output", fill="#555555", font=small_font)

    for c_i, col in enumerate(cols):
        x = left + c_i * cell_w
        label = f"P{col:02d}"
        tw, _ = _text_size(draw, label, label_font)
        draw.text((x + (cell_w - tw) / 2, top - 35), label, fill="#111111", font=label_font)

    for r_i, row in enumerate(rows):
        y = top + r_i * cell_h
        draw.text((40, y + 12), row, fill="#111111", font=small_font)
        for c_i, col in enumerate(cols):
            x = left + c_i * cell_w
            value = lookup.get((row, col))
            if value is True:
                fill, text = "#DFF2E1", "S"
                text_fill = "#0B6B2B"
            elif value is False:
                fill, text = "#F9D6D5", "F"
                text_fill = "#9B1C1C"
            else:
                fill, text = "#EEEEEE", "-"
                text_fill = "#666666"
            draw.rectangle([x, y, x + cell_w - 4, y + cell_h - 4], fill=fill, outline="#FFFFFF")
            tw, th = _text_size(draw, text, cell_font)
            draw.text((x + (cell_w - tw) / 2 - 2, y + (cell_h - th) / 2 - 4), text, fill=text_fill, font=cell_font)

    img.save(output_path)
    return output_path.resolve()


def _plot_tables_with_pil(tables: dict[str, pd.DataFrame], output_dir: Path | str) -> list[Path]:
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print("Neither matplotlib nor PIL is installed; skipping charts.")
        return []

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []

    summary = tables.get("summary_by_model_mode_size")
    if summary is not None and not summary.empty:
        plot_data = summary.copy()
        plot_data["series"] = plot_data["grid_size"].astype(str) + "x" + plot_data["grid_size"].astype(str) + " / " + plot_data["mode"]
        pivot = plot_data.pivot_table(index="model", columns="series", values="solve_rate_pct", aggfunc="mean").fillna(0)
        saved.append(
            _draw_grouped_horizontal_bars(
                pivot,
                title="Solve rate by model, mode, and grid size",
                subtitle="Percentage of puzzles fully solved",
                x_label="Solve rate (%)",
                output_path=output_path / "solve_rate_by_model_mode_size.png",
                max_value=100,
                suffix="%",
            )
        )

    multi = tables.get("multi_correct_placements")
    if multi is not None and not multi.empty:
        plot_data = multi.copy()
        plot_data["series"] = plot_data["grid_size"].astype(str) + "x" + plot_data["grid_size"].astype(str)
        pivot = plot_data.pivot_table(index="model", columns="series", values="avg_correct_placements", aggfunc="mean").fillna(0)
        saved.append(
            _draw_grouped_horizontal_bars(
                pivot,
                title="Average correct placements in multi-step runs",
                subtitle="Average number of correct placements before success or failure",
                x_label="Average correct placements",
                output_path=output_path / "multi_average_correct_placements.png",
            )
        )

    errors = tables.get("error_summary")
    if errors is not None and not errors.empty:
        failed = errors[errors["error_type"] != "Success"].copy()
        if not failed.empty:
            failed["series"] = failed["grid_size"].astype(str) + "x" + failed["grid_size"].astype(str) + " / " + failed["mode"]
            pivot = failed.pivot_table(index="error_type", columns="series", values="count", aggfunc="sum").fillna(0)
            saved.append(
                _draw_grouped_horizontal_bars(
                    pivot,
                    title="Failure type summary",
                    subtitle="Failed runs grouped by error type",
                    x_label="Run count",
                    output_path=output_path / "error_type_summary.png",
                )
            )

    time_summary = tables.get("time_summary")
    if time_summary is not None and not time_summary.empty:
        timed = time_summary[time_summary["n_with_time"].fillna(0).astype(float) > 0].copy()
        if not timed.empty:
            timed["series"] = timed["grid_size"].astype(str) + "x" + timed["grid_size"].astype(str) + " / " + timed["mode"]
            pivot = timed.pivot_table(index="model", columns="series", values="avg_time_seconds", aggfunc="mean").fillna(0)
            saved.append(
                _draw_grouped_horizontal_bars(
                    pivot,
                    title="Average runtime by model, mode, and grid size",
                    subtitle="Based on runs that recorded time_seconds",
                    x_label="Average runtime (seconds)",
                    output_path=output_path / "average_time_seconds_by_model_mode_size.png",
                    suffix="s",
                )
            )

    all_results = tables.get("all_results")
    if all_results is not None and not all_results.empty:
        saved.append(_draw_outcome_heatmap(all_results, output_path / "per_puzzle_outcome_heatmap.png"))

    return saved


def plot_tables(tables: dict[str, pd.DataFrame], output_dir: Path | str = "eval_outputs") -> list[Path]:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib is not installed; using PIL fallback charts.")
        return _plot_tables_with_pil(tables, output_dir)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []

    summary = tables.get("summary_by_model_mode_size")
    if summary is not None and not summary.empty:
        plot_data = summary.copy()
        plot_data["series"] = plot_data["grid_size"].astype(str) + "x" + plot_data["grid_size"].astype(str) + " / " + plot_data["mode"]
        pivot = plot_data.pivot_table(index="model", columns="series", values="solve_rate_pct", aggfunc="mean").fillna(0)
        ax = pivot.plot(kind="bar", figsize=(12, 5))
        ax.set_title("Solve rate by model, mode, and grid size")
        ax.set_ylabel("Solve rate (%)")
        ax.set_xlabel("Model")
        _style_matplotlib_bar_axis(ax, rotate=25, wrap_width=18)
        ax.legend(title="Grid / Mode", bbox_to_anchor=(1.02, 1), loc="upper left")
        plt.tight_layout(rect=[0, 0.08, 0.86, 1])
        chart_path = output_path / "solve_rate_by_model_mode_size.png"
        plt.savefig(chart_path, dpi=180)
        plt.close()
        saved.append(chart_path.resolve())

    multi = tables.get("multi_correct_placements")
    if multi is not None and not multi.empty:
        plot_data = multi.copy()
        plot_data["series"] = plot_data["grid_size"].astype(str) + "x" + plot_data["grid_size"].astype(str)
        pivot = plot_data.pivot_table(index="model", columns="series", values="avg_correct_placements", aggfunc="mean").fillna(0)
        ax = pivot.plot(kind="bar", figsize=(12, 5))
        ax.set_title("Average correct placements in multi-step runs")
        ax.set_ylabel("Average correct placements")
        ax.set_xlabel("Model")
        _style_matplotlib_bar_axis(ax, rotate=25, wrap_width=18)
        ax.legend(title="Grid size", bbox_to_anchor=(1.02, 1), loc="upper left")
        plt.tight_layout(rect=[0, 0.08, 0.86, 1])
        chart_path = output_path / "multi_average_correct_placements.png"
        plt.savefig(chart_path, dpi=180)
        plt.close()
        saved.append(chart_path.resolve())

    errors = tables.get("error_summary")
    if errors is not None and not errors.empty:
        failed = errors[errors["error_type"] != "Success"].copy()
        if not failed.empty:
            failed["series"] = failed["grid_size"].astype(str) + "x" + failed["grid_size"].astype(str) + " / " + failed["mode"]
            pivot = failed.pivot_table(index="error_type", columns="series", values="count", aggfunc="sum").fillna(0)
            ax = pivot.plot(kind="bar", figsize=(12, 5))
            ax.set_title("Failure type summary")
            ax.set_ylabel("Count")
            ax.set_xlabel("Error type")
            _style_matplotlib_bar_axis(ax, rotate=25, wrap_width=20)
            ax.legend(title="Grid / Mode", bbox_to_anchor=(1.02, 1), loc="upper left")
            plt.tight_layout(rect=[0, 0.12, 0.86, 1])
            chart_path = output_path / "error_type_summary.png"
            plt.savefig(chart_path, dpi=180)
            plt.close()
            saved.append(chart_path.resolve())

    time_summary = tables.get("time_summary")
    if time_summary is not None and not time_summary.empty:
        timed = time_summary[time_summary["n_with_time"].fillna(0).astype(float) > 0].copy()
        if not timed.empty:
            timed["series"] = timed["grid_size"].astype(str) + "x" + timed["grid_size"].astype(str) + " / " + timed["mode"]
            pivot = timed.pivot_table(index="model", columns="series", values="avg_time_seconds", aggfunc="mean").fillna(0)
            ax = pivot.plot(kind="bar", figsize=(12, 5))
            ax.set_title("Average runtime by model, mode, and grid size")
            ax.set_ylabel("Average runtime (seconds)")
            ax.set_xlabel("Model")
            _style_matplotlib_bar_axis(ax, rotate=25, wrap_width=18)
            ax.legend(title="Grid / Mode", bbox_to_anchor=(1.02, 1), loc="upper left")
            plt.tight_layout(rect=[0, 0.08, 0.86, 1])
            chart_path = output_path / "average_time_seconds_by_model_mode_size.png"
            plt.savefig(chart_path, dpi=180)
            plt.close()
            saved.append(chart_path.resolve())

    all_results = tables.get("all_results")
    if all_results is not None and not all_results.empty:
        import numpy as np
        from matplotlib.colors import ListedColormap
        from matplotlib.patches import Patch

        heatmap_data = all_results.copy()
        heatmap_data["row"] = (
            heatmap_data["grid_size"].astype(str)
            + "x"
            + heatmap_data["grid_size"].astype(str)
            + " / "
            + heatmap_data["mode"].astype(str)
            + " / "
            + heatmap_data["model"].astype(str)
        )
        heatmap_data["col"] = heatmap_data["puzzle_id"].astype(int)
        rows = sorted(heatmap_data["row"].unique())
        cols = sorted(heatmap_data["col"].unique())
        lookup = {(row["row"], int(row["col"])): bool(row["is_solved"]) for _, row in heatmap_data.iterrows()}
        matrix = np.full((len(rows), len(cols)), -1)
        for r, row_name in enumerate(rows):
            for c, col in enumerate(cols):
                value = lookup.get((row_name, col))
                matrix[r, c] = 1 if value is True else 0 if value is False else -1

        cmap = ListedColormap(["#E8E8E8", "#F4B6B6", "#BFE7C3"])
        fig_h = max(6, 0.38 * len(rows) + 2.2)
        fig_w = max(10, 0.7 * len(cols) + 6.5)
        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        ax.imshow(matrix + 1, cmap=cmap, vmin=0, vmax=2, aspect="auto")
        ax.set_title("Per-puzzle outcome heatmap", pad=14)
        ax.set_xticks(range(len(cols)))
        ax.set_xticklabels([f"P{col:02d}" for col in cols])
        ax.set_yticks(range(len(rows)))
        ax.set_yticklabels(rows)
        ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)
        for r in range(len(rows)):
            for c in range(len(cols)):
                value = matrix[r, c]
                label = "S" if value == 1 else "F" if value == 0 else "-"
                color = "#0B6B2B" if value == 1 else "#9B1C1C" if value == 0 else "#666666"
                ax.text(c, r, label, ha="center", va="center", color=color, fontweight="bold")
        ax.set_xticks(np.arange(-0.5, len(cols), 1), minor=True)
        ax.set_yticks(np.arange(-0.5, len(rows), 1), minor=True)
        ax.grid(which="minor", color="white", linestyle="-", linewidth=2)
        ax.tick_params(which="minor", bottom=False, left=False)
        legend = [
            Patch(facecolor="#BFE7C3", edgecolor="white", label="Solved"),
            Patch(facecolor="#F4B6B6", edgecolor="white", label="Failed"),
            Patch(facecolor="#E8E8E8", edgecolor="white", label="Missing output"),
        ]
        ax.legend(handles=legend, loc="lower center", bbox_to_anchor=(0.5, -0.12), ncol=3)
        plt.tight_layout()
        chart_path = output_path / "per_puzzle_outcome_heatmap.png"
        plt.savefig(chart_path, dpi=180, bbox_inches="tight")
        plt.close()
        saved.append(chart_path.resolve())

    return saved


def run_evaluation(
    output_dirs: list[Path] | None = None,
    dataset_dir: Path | None = None,
    export_dir: Path | str | None = None,
    make_plots: bool = True,
) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    df = collect_results(output_dirs=output_dirs, dataset_dir=dataset_dir)
    tables = build_summary_tables(df)
    export_dir = export_dir or default_export_dir()
    export_path = export_tables(tables, export_dir)
    print(f"Exported tables to: {export_path}")
    if make_plots:
        charts = plot_tables(tables, export_path)
        if charts:
            print("Saved charts:")
            for chart in charts:
                print(f"- {chart}")
    return df, tables


if __name__ == "__main__":
    run_evaluation()
