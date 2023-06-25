function scanWebsite() {
  const url = document.getElementById('url-input').value;
  const keywords = document.getElementById('keywords-input').value.split(',');

  const terminal = document.getElementById('terminal');
  terminal.innerHTML = ''; // Clear previous results

  printToTerminal(`Scanning website ${url} for keywords: ${keywords.join(', ')}\n`);

  fetch('/scan', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ url, keywords })
  })
    .then(response => response.json())
    .then(data => {
      printToTerminal('Scan completed.\n');
      if (data.error) {
        printToTerminal(`Error: ${data.error}\n`);
      } else {
        printToTerminal(`Found ${data.keywordMatches.length} keyword(s):\n`);
        data.keywordMatches.forEach(match => {
          printToTerminal(`- Keyword: ${match.keyword}, Found in: ${match.url}\n`);
        });
        printToTerminal(`\nFound ${data.pdfFiles.length} PDF file(s):\n`);
        data.pdfFiles.forEach(file => {
          printToTerminal(`- PDF file: ${file}\n`);
        });
      }
    })
    .catch(error => {
      printToTerminal(`Error: ${error}\n`);
    });
}

function printToTerminal(text) {
  const terminal = document.getElementById('terminal');
  terminal.innerText += text;
  terminal.scrollTop = terminal.scrollHeight; // Scroll to the bottom
}
