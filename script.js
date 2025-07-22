function scrapeRSS() {
    const url = document.getElementById('urlInput').value.trim();
    if (!url) return;

    const progressBar = document.getElementById('progressBar');
    const loadingContainer = document.getElementById('loadingContainer');
    const resultContainer = document.getElementById('resultContainer');
    progressBar.value = 0;
    loadingContainer.style.display = 'flex';
    resultContainer.style.display = 'none';

    let progress = 0;
    const interval = setInterval(() => {
        progress = Math.min(progress + 5, 95);
        progressBar.value = progress;
    }, 200);

    fetch('http://localhost:5000/scrape_rss?url=' + encodeURIComponent(url))
        .then(response => response.json())
        .then(data => displayRSSLinks(data))
        .catch(() => {
            const rssOutput = document.getElementById('rssOutput');
            rssOutput.textContent = 'Error retrieving RSS links.';
        })
        .finally(() => {
            clearInterval(interval);
            progressBar.value = 100;
            loadingContainer.style.display = 'none';
            resultContainer.style.display = 'flex';
        });
}

function displayRSSLinks(response) {
    const rssOutput = document.getElementById('rssOutput');
    rssOutput.textContent = '';
    if (Array.isArray(response.rss_links) && response.rss_links.length > 0) {
        rssOutput.textContent = response.rss_links
            .map(link => `${link.title}: ${link.link}`)
            .join('\n');
    } else {
        rssOutput.textContent = 'No RSS links found.';
    }
}

function copyToClipboard() {
    const rssOutput = document.getElementById('rssOutput');
    navigator.clipboard.writeText(rssOutput.textContent);
}
