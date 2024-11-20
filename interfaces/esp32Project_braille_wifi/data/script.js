document.getElementById('setMessageButton').addEventListener('click', function() {
  const messageInput = document.getElementById('messageInput').value;
  fetch('/setMessage', {
    method: 'POST',
    body: new URLSearchParams('message=' + messageInput)
  })
  .then(response => response.text())
  .then(data => {
    console.log('Resposta do servidor:', data);
    document.getElementById('messageDisplay').textContent = 'Mensagem: ' + messageInput;
  })
  .catch(error => {
    console.error('Erro:', error);
  });
});

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

// Função para obter e exibir o valor de intervalo
document.getElementById('intervalInput').addEventListener('focus', function() {
  fetch('/getIntervalo')
    .then(response => response.text())
    .then(data => {
      document.getElementById('intervalInput').value = data;
    })
    .catch(error => {
      console.error('Erro:', error);
    });
});

document.getElementById('increaseButton').addEventListener('click', function() {
  var input = document.getElementById('intervalInput');
  var currentValue = parseInt(input.value);
  if (currentValue < 2000) {
    input.value = currentValue + 100;
  }
});

document.getElementById('decreaseButton').addEventListener('click', function() {
  var input = document.getElementById('intervalInput');
  var currentValue = parseInt(input.value);
  if (currentValue > 200) {
    input.value = currentValue - 100;
  }
});

document.getElementById('saveButton').addEventListener('click', function() {
  var input = document.getElementById('intervalInput');
  var valueToSend = input.value;
  fetch('/setIntervalo', {
    method: 'POST',
    body: new URLSearchParams('intervalo=' + valueToSend)
  })
  .then(response => response.text())
  .then(data => {
    console.log('Resposta do servidor:', data);
    document.getElementById('intervalDisplay').textContent = 'Intervalo: ' + valueToSend + ' ms';
  })
  .catch(error => {
    console.error('Erro:', error);
  });
});

document.getElementById('clearMessageButton').addEventListener('click', function() {
  document.getElementById('messageInput').value = ''; // Limpa o campo de entrada
});

