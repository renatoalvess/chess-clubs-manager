document.getElementById('mobile-btn').addEventListener('click', function (event) {
    const menu = document.getElementById('menu-links');
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';

    // Impede que o clique no botão feche o menu imediatamente
    event.stopPropagation();
});

// Ocultar o menu ao clicar fora
document.addEventListener('click', function (event) {
    const menu = document.getElementById('menu-links');
    const button = document.getElementById('mobile-btn');

    // Verifica se o clique foi fora do menu e do botão
    if (menu.style.display === 'block' && !menu.contains(event.target) && event.target !== button) {
        menu.style.display = 'none';
    }
});


function toggleMenu(id) {
    var menu = document.getElementById(id);
    if (window.innerWidth <= 768) {
        if (menu.classList.contains('show')) {
            menu.classList.remove('show');
        } else {
            menu.classList.add('show');
        }
    }
}

document.addEventListener('click', function (event) {
    var isClickInsideMenu = event.target.closest('.dropdown');
    if (!isClickInsideMenu) {
        var dropdowns = document.querySelectorAll('.drop-menu.show');
        dropdowns.forEach(function (menu) {
            menu.classList.remove('show');
        });
    }
});