function scrapeRSS() {
	const urlInput = document.getElementById("urlInput");
	const url = urlInput.value.trim();
	if (!url) return;

	const progressBar = document.getElementById("progressBar");
	const loadingContainer = document.getElementById("loadingContainer");
	const resultContainer = document.getElementById("resultContainer");
	const statsOutput = document.getElementById("statsOutput");
	const rssList = document.getElementById("rssList");
	const errorOutput = document.getElementById("errorOutput");
	const mainContainer = document.getElementById("mainContainer");

	// Reset UI
	progressBar.value = 0;
	loadingContainer.style.display = "flex";
	resultContainer.style.display = "none";
	mainContainer.classList.remove("glass");
	statsOutput.textContent = "";
	rssList.innerHTML = "";
	errorOutput.textContent = "";

	// Fake progress bar
	let progress = 0;
	const interval = setInterval(() => {
		progress = Math.min(progress + 5, 90);
		progressBar.value = progress;
	}, 200);

	fetch("/scrape_rss?url=" + encodeURIComponent(url))
		.then((response) => {
			if (!response.ok) {
				return response.json().then((data) => {
					throw new Error(data.error || `Server error: ${response.status}`);
				});
			}
			return response.json();
		})
		.then((data) => {
			displayResults(data);
		})
		.catch((error) => {
			errorOutput.textContent = error.message;
			errorOutput.textContent = error.message;
			resultContainer.style.display = "flex"; // Show container to show error
			mainContainer.classList.add("glass");
		})
		.finally(() => {
			clearInterval(interval);
			progressBar.value = 100;
			loadingContainer.style.display = "none";
			if (!errorOutput.textContent) {
				resultContainer.style.display = "flex";
				mainContainer.classList.add("glass");
			}
		});
}

function displayResults(data) {
	const rssList = document.getElementById("rssList");
	const statsOutput = document.getElementById("statsOutput");

	// Show stats
	if (data.scan_ms) {
		statsOutput.textContent = `Found ${data.feeds.length} feeds in ${data.scan_ms}ms`;
	}

	if (data.feeds && data.feeds.length > 0) {
		data.feeds.forEach((feed) => {
			const li = document.createElement("li");
			li.className =
				"list-group-item d-flex justify-content-between align-items-center bg-transparent text-white border-light mb-2";
			li.style.backdropFilter = "blur(5px)";

			const textContainer = document.createElement("div");
			textContainer.className = "text-truncate me-3";

			const titleRow = document.createElement("div");
			titleRow.className = "d-flex align-items-center gap-2";

			const title = document.createElement("div");
			title.className = "fw-bold";
			title.textContent = feed.title || "Untitled Feed";

			const badge = document.createElement("span");
			badge.className = "badge rounded-pill bg-white text-dark bg-opacity-25";
			badge.style.fontSize = "0.7em";
			badge.textContent = (feed.type || "RSS").toUpperCase();

			titleRow.appendChild(title);
			titleRow.appendChild(badge);

			const link = document.createElement("div");
			link.className = "small text-light text-opacity-75 text-truncate";
			link.textContent = feed.url;

			textContainer.appendChild(titleRow);
			textContainer.appendChild(link);

			const copyBtn = document.createElement("button");
			copyBtn.className = "btn btn-sm btn-outline-light";
			copyBtn.textContent = "Copy";
			copyBtn.onclick = () => {
				navigator.clipboard.writeText(feed.url);
				const originalText = copyBtn.textContent;
				copyBtn.textContent = "Copied!";
				setTimeout(() => (copyBtn.textContent = originalText), 2000);
			};

			li.appendChild(textContainer);
			li.appendChild(copyBtn);
			rssList.appendChild(li);
		});
	} else {
		const li = document.createElement("li");
		li.className =
			"list-group-item bg-transparent text-white text-center border-0";
		li.textContent = "No RSS feeds found.";
		rssList.appendChild(li);
	}
}
