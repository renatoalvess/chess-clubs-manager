document.getElementById('nome').addEventListener('blur', function () {
    var playerName = this.value;
    if (playerName) {
        fetch(checkPlayerURL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: playerName })
        })
            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    alert('Nome já cadastrado!');
                    document.getElementById('nome').value = '';
                }
            });
    }
});

document.getElementById('playerForm').addEventListener('submit', function (event) {
    var playerName = document.getElementById('nome').value;
    if (playerName) {
        fetch(checkPlayerURL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: playerName })
        })
            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    alert('Nome já cadastrado!');
                    event.preventDefault();
                }
            });
    }
});
