function validarForm() {
    const jogador1_id = document.getElementById('jogador1_id').value;
    const jogador2_id = document.getElementById('jogador2_id').value;
    if (jogador1_id === jogador2_id) {
        alert('Os jogadores devem ser diferentes.');
        return false; // Impede o envio do formulário
    }
    return true; // Permite o envio do formulário
}

function validarJogadores() {
    const jogador1_nome = document.getElementById('jogador1_nome').value;
    const jogador2_nome = document.getElementById('jogador2_nome').value;
    if (jogador1_nome && jogador1_nome === jogador2_nome) {
        alert('Os jogadores devem ser diferentes.');
        document.getElementById('jogador2_nome').value = '';
    }
}

// Função para configurar o autocomplete
function configurarAutocomplete(inputSelector, hiddenInputSelector, ratingSpanSelector) {
    const input = document.querySelector(inputSelector);

    input.addEventListener('input', function () {
        const value = this.value;

        if (value.length > 0) {
            fetch('/buscar_jogadores?term=' + encodeURIComponent(value)) // Envia o termo digitado
                .then(response => response.json())
                .then(data => {
                    let suggestions = '';
                    data.forEach(jogador => {
                        suggestions += `<div class='autocomplete-suggestion' data-value='${jogador.value}' data-rating='${jogador.rating}'>${jogador.label} (Rating: ${jogador.rating})</div>`;
                    });
                    mostrarSugestoes(suggestions, input);
                });
        } else {
            esconderSugestoes();
        }
    });

    function mostrarSugestoes(suggestions, input) {
        esconderSugestoes(); // Esconder sugestões anteriores
        if (suggestions) {
            const div = document.createElement('div');
            div.className = 'autocomplete-suggestions';
            div.innerHTML = suggestions;

            document.body.appendChild(div);

            div.style.left = input.getBoundingClientRect().left + 'px';
            div.style.top = (input.getBoundingClientRect().bottom + window.scrollY) + 'px';

            div.addEventListener('click', function (e) {
                if (e.target.classList.contains('autocomplete-suggestion')) {
                    const value = e.target.getAttribute('data-value');
                    const rating = e.target.getAttribute('data-rating');
                    input.value = e.target.innerText.split(' (')[0]; // Define o nome do jogador
                    document.querySelector(hiddenInputSelector).value = value; // Define o ID do jogador
                    document.querySelector(ratingSpanSelector).innerText = rating; // Define o rating do jogador
                    esconderSugestoes(); // Esconder sugestões após a seleção
                    validarJogadores();
                }
            });
        }
    }

    function esconderSugestoes() {
        const suggestions = document.querySelector('.autocomplete-suggestions');
        if (suggestions) {
            suggestions.remove();
        }
    }

    document.addEventListener('click', esconderSugestoes); // Esconder sugestões ao clicar fora
}

document.addEventListener('DOMContentLoaded', function () {
    configurarAutocomplete('#jogador1_nome', '#jogador1_id', '#jogador1_rating');
    configurarAutocomplete('#jogador2_nome', '#jogador2_id', '#jogador2_rating');
});
