// Biến toàn cục quản lý state
let currentStep = 0;
let simInterval = null;
let logData = null;
let puzzleData = null;
let currentPuzzleId = 1;
let currentModel = "pro";

const currentBoardEl = document.getElementById("current-board");
const solutionBoardEl = document.getElementById("solution-board");
const reasoningEl = document.getElementById("reasoning-container");
const counterEl = document.getElementById("step-counter");
const statusBadge = document.getElementById("status-badge");

function animateFilledValue(valSpan, baseColorClass, isError = false) {
	if (!valSpan) return;
	if (baseColorClass) {
		valSpan.classList.remove(baseColorClass);
	}
	valSpan.classList.add(
		isError ? "text-ctp-red" : "text-ctp-green",
		"scale-125",
	);
	setTimeout(() => {
		valSpan.classList.remove(
			"scale-125",
			isError ? "text-ctp-red" : "text-ctp-green",
		);
		if (baseColorClass) {
			valSpan.classList.add(baseColorClass);
		}
	}, 300);
}

// ==== [ HÀM LOAD DỮ LIỆU TỪ FOLDER THEO YÊU CẦU CỦA BẠN ] ====
// Để sử dụng file json thật của bạn, hãy uncomment hàm tải này và gọi nó ở cuối script.

async function fetchPuzzleData(puzzleId, model = "pro") {
	const puzzleStr = puzzleId.toString().padStart(2, "0");
	try {
		const [puzzleRes, logRes] = await Promise.all([
			fetch(`../data/dataset/puzzle_${puzzleStr}.json`),
			fetch(
				`../data/log/gemini-2.5/multi_prompt/${model}/log_puzzle_${puzzleStr}.json`,
			),
		]);

		if (!puzzleRes.ok) throw new Error("Missing puzzle file");
		if (!logRes.ok) throw new Error("Missing log file");

		puzzleData = await puzzleRes.json();
		logData = await logRes.json();
		console.log("Loaded Puzzle Data:", puzzleData);
		console.log("Loaded Log Data:", logData);
		await initBoard();
		// Update badge immediately if final_status exists and no execution steps (edge case)
		updateStatusBadge(logData.final_status);
	} catch (err) {
		console.error("Failed to load files:", err);
		reasoningEl.innerHTML = `<div class="bg-ctp-crust p-3 rounded-lg border border-ctp-surface0 text-sm">Error loading puzzle or log: ${err.message}</div>`;
	}
}

// ==== [ KHỞI TẠO BẢNG ] ====
async function initBoard() {
	const size = puzzleData.grid_size; // vd: 6
	currentBoardEl.style.gridTemplateColumns = `repeat(${size}, minmax(0, 1fr))`;
	solutionBoardEl.style.gridTemplateColumns = `repeat(${size}, minmax(0, 1fr))`;
	currentBoardEl.innerHTML = ""; // Clear bảng
	solutionBoardEl.innerHTML = "";

	document.getElementById("puzzle-title-solution").innerText =
		`Puzzle ID: ${logData.puzzle_id} | Size: ${size}x${size} | Solution Board`;
	document.getElementById("puzzle-title-current").innerText =
		`Model: ${currentModel === "pro" ? "Gemini 2.5 Pro" : "Gemini 2.5 Flash"} | Current Board`;
	counterEl.innerText = `Step 0/${logData.execution_log.length}`;

	// Tạo các ô lưới (Cells) cho cả current và solution boards
	for (let r = 0; r < size; r++) {
		for (let c = 0; c < size; c++) {
			// current board cell
			const curCell = document.createElement("div");
			curCell.id = `cell-cur-${r}-${c}`;
			curCell.className =
				"sudoku-cell relative w-14 h-14 flex items-center justify-center text-2xl font-bold transition-all duration-300 bg-ctp-base";

			// solution board cell
			const solCell = document.createElement("div");
			solCell.id = `cell-sln-${r}-${c}`;
			solCell.className =
				"sudoku-cell relative w-14 h-14 flex items-center justify-center text-2xl font-bold transition-all duration-300 bg-ctp-base";

			// Vẽ các đường viền dày cho các block (2x3 cho lưới 6x6)
			if (size === 6) {
				if (r === 0) {
					curCell.classList.add("thick-top");
					solCell.classList.add("thick-top");
				}
				if (c === 0) {
					curCell.classList.add("thick-left");
					solCell.classList.add("thick-left");
				}
				if (r === 1 || r === 3 || r === 5) {
					curCell.classList.add("thick-bottom");
					solCell.classList.add("thick-bottom");
				}
				if (c === 2 || c === 5) {
					curCell.classList.add("thick-right");
					solCell.classList.add("thick-right");
				}
			}

			// Thẻ để chứa số điền vào (current)
			const curValue = document.createElement("span");
			curValue.className = "value text-ctp-text z-10";
			curCell.appendChild(curValue);

			// Thẻ để chứa số solution (solution board)
			const solValue = document.createElement("span");
			solValue.className = "value text-ctp-text z-10";
			// fill solution from puzzleData if available
			if (
				puzzleData &&
				puzzleData.solution &&
				puzzleData.solution[r] &&
				typeof puzzleData.solution[r][c] !== "undefined"
			) {
				solValue.innerText = puzzleData.solution[r][c];
			}
			solCell.appendChild(solValue);

			currentBoardEl.appendChild(curCell);
			solutionBoardEl.appendChild(solCell);
		}
	}

	// Vẽ Cages (Lồng)
	drawCages();
	resetSimulation();
}

// Vẽ đường viền đứt đoạn cho các khối cage
function drawCages() {
	puzzleData.cages.forEach((cage) => {
		// Sắp xếp các ô trong lồng để tìm ô trên cùng bên trái (đặt số SUM)
		const cells = [...cage.cells].sort((a, b) =>
			a[0] !== b[0] ? a[0] - b[0] : a[1] - b[1],
		);
		const topCell = cells[0];

		cells.forEach(([r, c]) => {
			// target both current and solution cells
			const curEl = document.getElementById(`cell-cur-${r}-${c}`);
			const slnEl = document.getElementById(`cell-sln-${r}-${c}`);

			// Function to create border for a given cell element
			const attachBorder = (cellEl) => {
				if (!cellEl) return;
				const cageBorder = document.createElement("div");
				cageBorder.className = "cage-border absolute inset-0";

				const hasTop = cells.some(
					(neighbor) => neighbor[0] === r - 1 && neighbor[1] === c,
				);
				const hasBottom = cells.some(
					(neighbor) => neighbor[0] === r + 1 && neighbor[1] === c,
				);
				const hasLeft = cells.some(
					(neighbor) => neighbor[0] === r && neighbor[1] === c - 1,
				);
				const hasRight = cells.some(
					(neighbor) => neighbor[0] === r && neighbor[1] === c + 1,
				);

				if (!hasTop) cageBorder.style.borderTopWidth = "2px";
				if (!hasBottom) cageBorder.style.borderBottomWidth = "2px";
				if (!hasLeft) cageBorder.style.borderLeftWidth = "2px";
				if (!hasRight) cageBorder.style.borderRightWidth = "2px";

				cellEl.appendChild(cageBorder);
			};

			attachBorder(curEl);
			attachBorder(slnEl);

			// Thêm số đích (sum) vào ô top-left của lồng (với cả 2 bảng)
			if (r === topCell[0] && c === topCell[1]) {
				const sumSpan1 = document.createElement("span");
				sumSpan1.className =
					"absolute top-[3px] left-[5px] text-[10px] text-ctp-text z-10";
				sumSpan1.innerText = cage.sum;
				if (curEl) curEl.appendChild(sumSpan1);

				const sumSpan2 = document.createElement("span");
				sumSpan2.className =
					"absolute top-[3px] left-[5px] text-[10px] text-ctp-text z-10";
				sumSpan2.innerText = cage.sum;
				if (slnEl) slnEl.appendChild(sumSpan2);
			}
		});
	});
}

// ==== [ LOGIC SIMULATION ] ====
function processNextStep() {
	if (currentStep >= logData.execution_log.length) {
		clearInterval(simInterval);
		// At the end of execution, show final status badge if present
		if (logData && logData.final_status) {
			updateStatusBadge(logData.final_status);
		}
		return;
	}

	const stepObj = logData.execution_log[currentStep];

	// Xoá highlight cũ
	document
		.querySelectorAll(".sudoku-cell")
		.forEach((el) => el.classList.remove("bg-ctp-surface2"));

	if (!stepObj.chosen_cell) {
		const p = document.createElement("div");
		p.className =
			"bg-ctp-crust p-3 rounded-lg border border-ctp-surface0 slide-in text-sm leading-relaxed";
		p.innerHTML = `<span class="text-ctp-blue font-bold uppercase tracking-wider text-xs">Step ${stepObj.step}: ${stepObj.chosen_cell} = ${stepObj.value}</span><br/>
                           <span class="text-ctp-subtext1">${stepObj.error_type}</span>`;

		// Nếu là bước đầu tiên thì xoá text hướng dẫn
		if (currentStep === 0) reasoningEl.innerHTML = "";

		reasoningEl.appendChild(p);
		// Tự động scroll xuống cuối log
		reasoningEl.scrollTop = reasoningEl.scrollHeight;

		currentStep++;
		counterEl.innerText = `Step ${currentStep}/${logData.execution_log.length}`;
		return;
	}
	// Parse 'rXcY' thành mảng index [row, col]
	const isError =
		logData.final_status.toLowerCase() === "failed" &&
		currentStep === logData.execution_log.length - 1;
	const match = stepObj.chosen_cell.match(/r(\d+)c(\d+)/);
	if (match) {
		// Json của user là 1-indexed (r1c1...), ta cần đổi về 0-indexed cho thẻ HTML
		const r = parseInt(match[1]) - 1;
		const c = parseInt(match[2]) - 1;

		const cellEl = document.getElementById(`cell-cur-${r}-${c}`);
		if (cellEl) {
			// Highlight ô hiện tại & cập nhật giá trị (current board only)
			cellEl.classList.add("bg-ctp-surface2");
			const valSpan = cellEl.querySelector(".value");
			valSpan.innerText = stepObj.value;

			// Thêm một chút animation khi fill số mới
			animateFilledValue(valSpan, "text-ctp-text", isError);

			const solutionCellEl = document.getElementById(`cell-sln-${r}-${c}`);
			if (solutionCellEl) {
				const solutionValSpan = solutionCellEl.querySelector(".value");
				animateFilledValue(solutionValSpan, "text-ctp-text", isError);
			}
		}
	}

	// Append text vào khối Reasoning
	const p = document.createElement("div");
	p.className =
		"bg-ctp-crust p-3 rounded-lg border border-ctp-surface0 slide-in text-sm leading-relaxed";
	p.innerHTML = `<span class="text-ctp-blue font-bold uppercase tracking-wider text-xs">Step ${stepObj.step}: ${stepObj.chosen_cell} = ${stepObj.value}</span><br/>
                           <span class="text-ctp-subtext1">${stepObj.reasoning}</span>`;

	// Nếu là bước đầu tiên thì xoá text hướng dẫn
	if (currentStep === 0) reasoningEl.innerHTML = "";

	reasoningEl.appendChild(p);
	// Tự động scroll xuống cuối log
	reasoningEl.scrollTop = reasoningEl.scrollHeight;

	currentStep++;
	counterEl.innerText = `Step ${currentStep}/${logData.execution_log.length}`;
}

function resetSimulation() {
	clearInterval(simInterval);
	currentStep = 0;
	counterEl.innerText = `Step 0/${logData.execution_log.length}`;
	// clear only the current board values, keep solution visible
	document
		.querySelectorAll("#current-board .sudoku-cell .value")
		.forEach((el) => {
			el.innerText = "";
			el.classList.remove("text-ctp-green");
		});
	// remove highlight from both boards
	document
		.querySelectorAll(".sudoku-cell")
		.forEach((el) => el.classList.remove("bg-ctp-surface2"));
	// hide badge on reset
	updateStatusBadge(null);
}

document.getElementById("btn-start").addEventListener("click", () => {
	clearInterval(simInterval);
	// 1.5 giây cho mỗi bước suy luận để người dùng kịp đọc
	simInterval = setInterval(processNextStep, 1000);
});

document.getElementById("btn-reset").addEventListener("click", resetSimulation);

// UI controls: prev/next puzzle and model select
document.getElementById("btn-prev").addEventListener("click", () => {
	if (currentPuzzleId > 1) {
		currentPuzzleId--;
		loadCurrent();
	}
});
document.getElementById("btn-next").addEventListener("click", () => {
	currentPuzzleId++;
	loadCurrent();
});
document.getElementById("model-select").addEventListener("change", (e) => {
	currentModel = e.target.value;
	loadCurrent();
});

function loadCurrent() {
	// stop any running sim, clear board and fetch new data
	clearInterval(simInterval);
	reasoningEl.innerHTML = "";
	fetchPuzzleData(currentPuzzleId, currentModel);
}

function updateStatusBadge(status) {
	if (!status) {
		statusBadge.classList.add("hidden");
		statusBadge.className =
			"ml-3 hidden text-xs font-semibold px-2 py-1 rounded-full";
		statusBadge.innerText = "";
		return;
	}
	statusBadge.classList.remove("hidden");
	if (status.toLowerCase() === "failed") {
		statusBadge.className =
			"ml-3 inline-block text-xs font-semibold px-2 py-1 rounded-full bg-ctp-rosewater text-ctp-base";
		statusBadge.innerText = "Failed";
	} else {
		statusBadge.className =
			"ml-3 inline-block text-xs font-semibold px-2 py-1 rounded-full bg-ctp-green text-ctp-base";
		statusBadge.innerText = status;
	}
}

// --- Khởi chạy ban đầu với dữ liệu Mock ---
window.onload = () => {
	initBoard();
	// set initial model select and puzzle id
	document.getElementById("model-select").value = currentModel;
	currentPuzzleId = 1;
	fetchPuzzleData(currentPuzzleId, currentModel);
};
