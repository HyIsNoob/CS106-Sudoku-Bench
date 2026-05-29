const MODELS = [
	{
		id: "gemini-2.5-flash",
		label: "Gemini 2.5 Flash",
		logDir: "../data/log/gemini-2.5/multi_prompt/flash",
	},
	{
		id: "gemini-2.5-pro",
		label: "Gemini 2.5 Pro",
		logDir: "../data/log/gemini-2.5/multi_prompt/pro",
	},
	{
		id: "gemini-3.1-flash-lite",
		label: "Gemini 3.1 Flash Lite",
		logDir: "../data/log/gemini-3.x/multi-prompt/lite",
	},
	{
		id: "gemini-3.5-flash",
		label: "Gemini 3.5 Flash",
		logDir: "../data/log/gemini-3.x/multi-prompt/flash",
	},
];

const PUZZLES = [1, 2, 3, 4, 5, 6, 7];
const CAGE_FILL_COUNT = 6;

let currentStep = 0;
let simInterval = null;
let logData = null;
let puzzleData = null;
let currentPuzzleId = 1;
let currentModelId = "gemini-3.5-flash";
let simulationDelay = 1000;
let hasFinished = false;

const currentBoardEl = document.getElementById("current-board");
const solutionBoardEl = document.getElementById("solution-board");
const reasoningEl = document.getElementById("reasoning-container");
const counterEl = document.getElementById("step-counter");
const statusBadge = document.getElementById("status-badge");
const modelSelect = document.getElementById("model-select");
const puzzleSelect = document.getElementById("puzzle-select");
const themeToggle = document.getElementById("theme-toggle");
const speedRange = document.getElementById("speed-range");
const speedLabel = document.getElementById("speed-label");
const startButton = document.getElementById("btn-start");
const resetButton = document.getElementById("btn-reset");
const stepButton = document.getElementById("btn-step");
const prevButton = document.getElementById("btn-prev");
const nextButton = document.getElementById("btn-next");

function currentModel() {
	return MODELS.find((model) => model.id === currentModelId) ?? MODELS[0];
}

function padPuzzleId(puzzleId) {
	return String(puzzleId).padStart(2, "0");
}

function setTheme(theme) {
	document.body.classList.toggle("theme-light", theme === "light");
	document.body.classList.toggle("theme-dark", theme === "dark");
	localStorage.setItem("sudoku-demo-theme", theme);
	updateThemeToggle(theme);
}

function themeIcon(theme) {
	if (theme === "dark") {
		return `
			<svg viewBox="0 0 24 24" aria-hidden="true">
				<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79Z"></path>
			</svg>
		`;
	}

	return `
		<svg viewBox="0 0 24 24" aria-hidden="true">
			<circle cx="12" cy="12" r="4"></circle>
			<path d="M12 2v2"></path>
			<path d="M12 20v2"></path>
			<path d="m4.93 4.93 1.41 1.41"></path>
			<path d="m17.66 17.66 1.41 1.41"></path>
			<path d="M2 12h2"></path>
			<path d="M20 12h2"></path>
			<path d="m6.34 17.66-1.41 1.41"></path>
			<path d="m19.07 4.93-1.41 1.41"></path>
		</svg>
	`;
}

function updateThemeToggle(theme) {
	themeToggle.innerHTML = themeIcon(theme);
	themeToggle.dataset.theme = theme;
	themeToggle.setAttribute("aria-label", theme === "light" ? "Switch to dark theme" : "Switch to light theme");
	themeToggle.title = theme === "light" ? "Switch to dark theme" : "Switch to light theme";
}

function populateControls() {
	modelSelect.innerHTML = MODELS.map(
		(model) => `<option value="${model.id}">${model.label}</option>`,
	).join("");
	modelSelect.value = currentModelId;

	puzzleSelect.innerHTML = PUZZLES.map(
		(id) => `<option value="${id}">Puzzle ${padPuzzleId(id)}</option>`,
	).join("");
	puzzleSelect.value = String(currentPuzzleId);

	const savedTheme = localStorage.getItem("sudoku-demo-theme") || "light";
	setTheme(savedTheme);

	speedRange.value = String(simulationDelay);
	updateSpeedLabel();
}

function updateSpeedLabel() {
	speedLabel.textContent = `${(simulationDelay / 1000).toFixed(1)}s`;
}

function setRunning(isRunning) {
	startButton.textContent = isRunning ? "Pause" : "Start";
}

function clearFinishEffect() {
	document.body.classList.remove("run-success", "run-failed");
	statusBadge.classList.remove("status-pop");
}

function stopSimulation() {
	if (simInterval) clearInterval(simInterval);
	simInterval = null;
	setRunning(false);
}

function playFinishEffect(status) {
	clearFinishEffect();
	const normalized = String(status || "").toLowerCase();
	const effectClass = normalized === "success" ? "run-success" : "run-failed";

	requestAnimationFrame(() => {
		document.body.classList.add(effectClass);
		statusBadge.classList.add("status-pop");
	});
}

function finishSimulation() {
	if (!logData || hasFinished) return;

	hasFinished = true;
	stopSimulation();
	updateStatusBadge(logData.final_status);
	playFinishEffect(logData.final_status);
}

async function fetchPuzzleData(puzzleId, modelId) {
	const puzzleStr = padPuzzleId(puzzleId);
	const model = MODELS.find((item) => item.id === modelId);
	if (!model) throw new Error(`Unknown model: ${modelId}`);

	try {
		stopSimulation();
		hasFinished = false;
		clearFinishEffect();
		updateStatusBadge(null);
		reasoningEl.innerHTML = `<div class="empty-state">Loading ${model.label} on Puzzle ${puzzleStr}...</div>`;

		const [puzzleRes, logRes] = await Promise.all([
			fetch(`../data/dataset/puzzle_${puzzleStr}.json`),
			fetch(`${model.logDir}/log_puzzle_${puzzleStr}.json`),
		]);

		if (!puzzleRes.ok) throw new Error(`Missing dataset puzzle_${puzzleStr}.json`);
		if (!logRes.ok) throw new Error(`Missing log for ${model.label}, puzzle ${puzzleStr}`);

		puzzleData = await puzzleRes.json();
		logData = await logRes.json();
		initBoard();
		updateStatusBadge(logData.final_status);
	} catch (err) {
		console.error(err);
		logData = null;
		puzzleData = null;
		currentBoardEl.innerHTML = "";
		solutionBoardEl.innerHTML = "";
		counterEl.textContent = "Step 0/0";
		document.getElementById("puzzle-meta").textContent = "Unavailable";
		document.getElementById("model-meta").textContent = currentModel().label;
		reasoningEl.innerHTML = `<div class="reasoning-card error-card"><strong>Load error</strong>${escapeHtml(err.message)}</div>`;
	}
}

function inferBlockShape(size) {
	if (size === 4) return [2, 2];
	if (size === 6) return [2, 3];
	if (size === 9) return [3, 3];
	return [1, size];
}

function initBoard() {
	if (!puzzleData || !logData) return;

	const size = puzzleData.grid_size;
	const [blockRows, blockCols] = inferBlockShape(size);
	const cellSize = size >= 9 ? "44px" : "58px";

	for (const boardEl of [currentBoardEl, solutionBoardEl]) {
		boardEl.innerHTML = "";
		boardEl.style.gridTemplateColumns = `repeat(${size}, var(--cell-size))`;
		boardEl.style.setProperty("--cell-size", cellSize);
	}

	document.getElementById("puzzle-title-solution").textContent = "Solution Board";
	document.getElementById("puzzle-title-current").textContent = "Current Board";
	document.getElementById("puzzle-meta").textContent =
		`Puzzle ${padPuzzleId(logData.puzzle_id)} | ${size}x${size} | ${puzzleData.difficulty}`;
	document.getElementById("model-meta").textContent = currentModel().label;
	counterEl.textContent = `Step 0/${logData.execution_log.length}`;

	for (let r = 0; r < size; r++) {
		for (let c = 0; c < size; c++) {
			currentBoardEl.appendChild(createCell("cur", r, c, size, blockRows, blockCols));
			solutionBoardEl.appendChild(createCell("sln", r, c, size, blockRows, blockCols));
		}
	}

	drawCages();
	fillSolutionBoard();
	resetSimulation();
	requestAnimationFrame(syncReasoningHeight);
}

function createCell(kind, r, c, size, blockRows, blockCols) {
	const cell = document.createElement("div");
	cell.id = `cell-${kind}-${r}-${c}`;
	cell.className = "sudoku-cell";

	if (r === 0) cell.classList.add("thick-top");
	if (c === 0) cell.classList.add("thick-left");
	if ((r + 1) % blockRows === 0) cell.classList.add("thick-bottom");
	if ((c + 1) % blockCols === 0) cell.classList.add("thick-right");
	if (r === size - 1) cell.classList.add("thick-bottom");
	if (c === size - 1) cell.classList.add("thick-right");

	const value = document.createElement("span");
	value.className = "value";
	cell.appendChild(value);
	return cell;
}

function drawCages() {
	if (!puzzleData?.cages) return;

	puzzleData.cages.forEach((cage, cageIndex) => {
		const cells = [...cage.cells].sort((a, b) =>
			a[0] !== b[0] ? a[0] - b[0] : a[1] - b[1],
		);
		const topCell = cells[0];
		const fillClass = `cage-fill-${cageIndex % CAGE_FILL_COUNT}`;

		cells.forEach(([r, c]) => {
			for (const prefix of ["cur", "sln"]) {
				const cellEl = document.getElementById(`cell-${prefix}-${r}-${c}`);
				if (!cellEl) continue;

				cellEl.classList.add(fillClass);
				attachCageBorder(cellEl, cells, r, c);

				if (r === topCell[0] && c === topCell[1]) {
					const sumSpan = document.createElement("span");
					sumSpan.className = "cage-sum";
					sumSpan.textContent = cage.sum;
					cellEl.appendChild(sumSpan);
				}
			}
		});
	});
}

function attachCageBorder(cellEl, cells, r, c) {
	const cageBorder = document.createElement("div");
	cageBorder.className = "cage-border";

	const hasTop = cells.some(([nr, nc]) => nr === r - 1 && nc === c);
	const hasBottom = cells.some(([nr, nc]) => nr === r + 1 && nc === c);
	const hasLeft = cells.some(([nr, nc]) => nr === r && nc === c - 1);
	const hasRight = cells.some(([nr, nc]) => nr === r && nc === c + 1);

	if (!hasTop) cageBorder.style.borderTopWidth = "2px";
	if (!hasBottom) cageBorder.style.borderBottomWidth = "2px";
	if (!hasLeft) cageBorder.style.borderLeftWidth = "2px";
	if (!hasRight) cageBorder.style.borderRightWidth = "2px";

	cellEl.appendChild(cageBorder);
}

function fillSolutionBoard() {
	const solution = puzzleData.solution || [];
	for (let r = 0; r < solution.length; r++) {
		for (let c = 0; c < solution[r].length; c++) {
			setCellValue("sln", r, c, solution[r][c], false);
		}
	}
}

function resetSimulation() {
	stopSimulation();
	currentStep = 0;
	hasFinished = false;
	clearFinishEffect();
	if (!logData || !puzzleData) return;

	document.querySelectorAll(".sudoku-cell").forEach((cell) => {
		cell.classList.remove("active", "error");
		const value = cell.querySelector(".value");
		if (value) value.classList.remove("filled", "error-value");
	});

	document.querySelectorAll("#current-board .sudoku-cell .value").forEach((value) => {
		value.textContent = "";
		value.classList.remove("filled", "error-value");
	});

	const initialBoard = puzzleData.puzzle || [];
	for (let r = 0; r < initialBoard.length; r++) {
		for (let c = 0; c < initialBoard[r].length; c++) {
			const value = Number(initialBoard[r][c]);
			if (value) {
				setCellValue("cur", r, c, value, false);
				document.getElementById(`cell-cur-${r}-${c}`)?.classList.add("given");
			}
		}
	}

	counterEl.textContent = `Step 0/${logData.execution_log.length}`;
	reasoningEl.innerHTML = `<div class="empty-state">Ready. Press Start or Step to replay the reasoning trace.</div>`;
	updateStatusBadge(logData.final_status);
}

function syncReasoningHeight() {
	const boardHeights = Array.from(document.querySelectorAll(".board-panel"))
		.map((panel) => panel.offsetHeight)
		.filter(Boolean);

	if (!boardHeights.length) return;
	document.documentElement.style.setProperty(
		"--reasoning-panel-height",
		`${Math.max(...boardHeights)}px`,
	);
}

function setCellValue(prefix, r, c, value, animate = true, isError = false) {
	const cell = document.getElementById(`cell-${prefix}-${r}-${c}`);
	if (!cell) return;
	const valueEl = cell.querySelector(".value");
	if (!valueEl) return;

	valueEl.textContent = value ?? "";
	if (animate) {
		valueEl.classList.remove("filled", "error-value");
		valueEl.classList.add(isError ? "error-value" : "filled");
		setTimeout(() => valueEl.classList.remove("filled", "error-value"), 360);
	}
}

function processNextStep() {
	if (!logData || currentStep >= logData.execution_log.length) {
		finishSimulation();
		return;
	}

	document.querySelectorAll(".sudoku-cell").forEach((cell) => {
		cell.classList.remove("active", "error");
	});

	const stepObj = logData.execution_log[currentStep];
	const isLastStep = currentStep === logData.execution_log.length - 1;
	const isError =
		String(logData.final_status || "").toLowerCase() === "failed" && isLastStep;

	if (currentStep === 0) reasoningEl.innerHTML = "";

	if (!stepObj.chosen_cell) {
		appendReasoningCard(stepObj, true);
		currentStep++;
		counterEl.textContent = `Step ${currentStep}/${logData.execution_log.length}`;
		if (currentStep >= logData.execution_log.length) finishSimulation();
		return;
	}

	const parsed = parseCell(stepObj.chosen_cell);
	if (parsed) {
		const [r, c] = parsed;
		const currentCell = document.getElementById(`cell-cur-${r}-${c}`);
		const solutionCell = document.getElementById(`cell-sln-${r}-${c}`);
		currentCell?.classList.add(isError ? "error" : "active");
		solutionCell?.classList.add(isError ? "error" : "active");
		setCellValue("cur", r, c, stepObj.value, true, isError);
	}

	appendReasoningCard(stepObj, isError);
	currentStep++;
	counterEl.textContent = `Step ${currentStep}/${logData.execution_log.length}`;
	if (currentStep >= logData.execution_log.length) finishSimulation();
}

function appendReasoningCard(stepObj, isError) {
	document.querySelectorAll(".reasoning-card.current").forEach((card) => {
		card.classList.remove("current");
		card.classList.add("past");
	});

	const card = document.createElement("div");
	card.className = `reasoning-card current slide-in${isError ? " error-card" : ""}`;
	const content = stepObj.reasoning || stepObj.error_type || "No reasoning text recorded.";
	const moveLabel = stepObj.chosen_cell ?? "No move";
	const valueLabel = stepObj.value ? `Value ${stepObj.value}` : "No value";
	card.innerHTML = `
		<div class="reasoning-card-top">
			<span class="step-chip">Step ${currentStep + 1}</span>
			<span class="move-chip">${escapeHtml(moveLabel)}</span>
			<span class="value-chip">${escapeHtml(valueLabel)}</span>
		</div>
		<p class="reasoning-text">${highlightReasoning(content)}</p>
	`;
	reasoningEl.appendChild(card);
	reasoningEl.scrollTop = reasoningEl.scrollHeight;
}

function parseCell(cell) {
	const match = String(cell || "").match(/^r(\d+)c(\d+)$/i);
	if (!match) return null;
	return [Number(match[1]) - 1, Number(match[2]) - 1];
}

function toggleSimulation() {
	if (!logData) return;
	if (simInterval) {
		stopSimulation();
		return;
	}
	simInterval = setInterval(processNextStep, simulationDelay);
	setRunning(true);
}

function restartIntervalIfRunning() {
	if (!simInterval) return;
	clearInterval(simInterval);
	simInterval = setInterval(processNextStep, simulationDelay);
}

function loadCurrent() {
	currentPuzzleId = Number(puzzleSelect.value);
	currentModelId = modelSelect.value;
	fetchPuzzleData(currentPuzzleId, currentModelId);
}

function updateStatusBadge(status) {
	statusBadge.className = "status-badge hidden";
	statusBadge.textContent = "";
	if (!status) return;

	const normalized = String(status).toLowerCase();
	statusBadge.classList.remove("hidden");
	statusBadge.classList.add(normalized === "success" ? "status-success" : "status-failed");
	statusBadge.textContent = status;
}

function escapeHtml(value) {
	return String(value)
		.replaceAll("&", "&amp;")
		.replaceAll("<", "&lt;")
		.replaceAll(">", "&gt;")
		.replaceAll('"', "&quot;")
		.replaceAll("'", "&#039;");
}

function highlightReasoning(value) {
	const cellRefs = [];
	const placeholderPrefix = "SREFPLACEHOLDER";
	const html = escapeHtml(value)
		.replace(/\b(r\d+c\d+)\b/gi, (match) => {
			const index = cellRefs.length;
			cellRefs.push(`<span class="logic-token cell-token">${match}</span>`);
			return `${placeholderPrefix}${index}`;
		})
		.replace(/\b(row|column|subgrid|cage|cell)\b/gi, '<span class="logic-token">$1</span>')
		.replace(/\b(only|missing|forces|consistent|satisfies|contradiction)\b/gi, '<span class="logic-token key-token">$1</span>');

	return html.replace(new RegExp(`${placeholderPrefix}(\\d+)`, "g"), (_, index) => cellRefs[Number(index)]);
}

themeToggle.addEventListener("click", () => {
	const currentTheme = document.body.classList.contains("theme-dark") ? "dark" : "light";
	setTheme(currentTheme === "light" ? "dark" : "light");
});

modelSelect.addEventListener("change", loadCurrent);
puzzleSelect.addEventListener("change", loadCurrent);

speedRange.addEventListener("input", (event) => {
	simulationDelay = Number(event.target.value);
	updateSpeedLabel();
	restartIntervalIfRunning();
});

startButton.addEventListener("click", toggleSimulation);
resetButton.addEventListener("click", resetSimulation);
stepButton.addEventListener("click", () => {
	stopSimulation();
	processNextStep();
});

prevButton.addEventListener("click", () => {
	const currentIndex = PUZZLES.indexOf(currentPuzzleId);
	const nextIndex = Math.max(0, currentIndex - 1);
	currentPuzzleId = PUZZLES[nextIndex];
	puzzleSelect.value = String(currentPuzzleId);
	loadCurrent();
});

nextButton.addEventListener("click", () => {
	const currentIndex = PUZZLES.indexOf(currentPuzzleId);
	const nextIndex = Math.min(PUZZLES.length - 1, currentIndex + 1);
	currentPuzzleId = PUZZLES[nextIndex];
	puzzleSelect.value = String(currentPuzzleId);
	loadCurrent();
});

window.addEventListener("load", () => {
	populateControls();
	loadCurrent();
});

window.addEventListener("resize", syncReasoningHeight);
