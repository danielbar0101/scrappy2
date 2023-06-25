function scanWebsite() {
  var website = document.getElementById('website').value;
  var keywords = document.getElementById('keywords').value;

  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/scan', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var response = JSON.parse(xhr.responseText);
      showResults(response);
    }
  };
  xhr.send('website=' + encodeURIComponent(website) + '&keywords=' + encodeURIComponent(keywords));
}

function showResults(result) {
  var terminal = document.getElementById('terminal');
  terminal.innerHTML = '';

  for (var keyword in result) {
    var count = result[keyword];
    var line = document.createElement('div');
    line.innerHTML = 'Keyword: ' + keyword + ', Count: ' + count;
    terminal.appendChild(line);
  }
}
