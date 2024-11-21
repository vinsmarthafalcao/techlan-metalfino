// importações

// Funcionamento Menu hamburguer
function toggleMenu() {
    const menu = document.getElementById("mobile-menu");
    menu.classList.toggle("hidden");
}

// chamada de métodos por evento
document.addEventListener("DOMContentLoaded", () => {    
    document.getElementById("btMenu").addEventListener("click", toggleMenu)
});

// Dropdown apontamento
document.getElementById("btListApt").onclick = function () {
    const menu = document.getElementById("listApt");
    menu.classList.toggle("hidden");
};

// Dropdown apontamento mobile
document.getElementById("btListAptM").onclick = function () {
    const menu = document.getElementById("listAptM");
    menu.classList.toggle("hidden");
};

