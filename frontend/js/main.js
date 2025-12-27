const slides = document.getElementById("slides");
let posicao = 0;

// simulação: dias liberados
const diasLiberados = 3;

for (let dia = 1; dia <= 30; dia++) {
  const card = document.createElement("div");
  card.className = "aula-card";

  if (dia > diasLiberados) {
    card.classList.add("locked");
    card.innerHTML = `Dia ${dia}<br>🔒`;
  } else {
    card.innerHTML = `Dia ${dia}<br>▶`;
    card.onclick = () => abrirAula(dia);
  }

  slides.appendChild(card);
}

function avancar() {
  posicao -= 200;
  slides.style.transform = `translateX(${posicao}px)`;
}

function voltar() {
  posicao += 200;
  slides.style.transform = `translateX(${posicao}px)`;
}

function abrirAula(dia) {
  document.querySelector(".video-box").innerHTML =
    `<p>🎥 Vídeo da Aula ${dia}</p>`;
}

function logout() {
  localStorage.removeItem("token");
  window.location.href = "login.html";
}
