document.getElementById('checkBtn').addEventListener('click', () => {
    const email = document.getElementById('emailText').value;
  
    fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email })
    })
      .then(response => response.json())
      .then(data => {
        document.getElementById('result').innerHTML = `
          <b>Prediction:</b> ${data.prediction}<br>
          <b>Phishing Probability:</b> ${data.phishing_probability}%<br>
          <b>Red Flags:</b><br>${data.red_flags.map(flag => `• ${flag}`).join('<br>')}
        `;
      })
      .catch(err => {
        console.error(err);
        document.getElementById('result').innerHTML = `<span style="color: red;">Error: Could not reach backend.</span>`;
      });
  });
  