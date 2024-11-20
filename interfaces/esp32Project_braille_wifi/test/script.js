document.getElementById('getMessageButton').addEventListener('click', function() {
  fetch('/getMessage')
    .then(response => response.text())
    .then(data => {
      document.getElementById('messageDisplay').textContent = 'Mensagem: ' + data;
    })
    .catch(error => {
      console.error('Erro:', error);
    });
});

