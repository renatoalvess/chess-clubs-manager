document.getElementById('nome').addEventListener('blur', function () {
    var clubName = this.value;
    if (clubName) {
        fetch(checkClubURL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: clubName })
        })
            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    alert('Nome já cadastrado!');
                    document.getElementById('nome').value = '';
                }
            })
            .catch(error => console.error('Erro:', error));
    }
});

document.getElementById('clubForm').addEventListener('submit', function (event) {
    var clubName = document.getElementById('nome').value;
    if (clubName) {
        fetch(checkClubURL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: clubName })
        })
            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    alert('Nome já cadastrado!');
                    event.preventDefault();
                }
            })
            .catch(error => console.error('Erro:', error));
    }
});
