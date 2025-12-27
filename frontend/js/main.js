const slides = document.getElementById("slides");
const progressoTexto = document.getElementById("progressoTexto");
const videoBox = document.getElementById("videoBox");

let diasLiberados = 0;
let posicao = 0;

// Mapa de vídeos
const videos = {
  1: "https://www.youtube.com/embed/dQw4w9WgXcQ",
  2: "https://www.youtube.com/embed/dQw4w9WgXcQ",
  3: "https://www.youtube.com/embed/dQw4w9WgXcQ",
  4: "https://www.youtube.com/embed/dQw4w9WgXcQ",
  5: "https://www.youtube.com/embed/dQw4w9WgXcQ"
};

// Buscar progresso real
fetch("http://127.0.0.1:8000/progresso")
  .then(res => res.json())
  .then(data => {
    diasLiberados = data.dias_liberados;
    progressoTexto.innerText = `${diasLiberados} / ${data.total_dias} dias liberados`;
    gerarAulas();
  });

function gerarAulas() {
  slides.innerHTML = "";

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
}

function abrirAula(dia) {
  if (!videos[dia]) {
    videoBox.innerHTML = "<p>Vídeo ainda não disponível</p>";
    return;
  }

  videoBox.innerHTML = `
    <iframe src="${videos[dia]}" allowfullscreen></iframe>
  `;
}

function avancar() {
  posicao -= 200;
  slides.style.transform = `translateX(${posicao}px)`;
}

function voltar() {
  posicao += 200;
  slides.style.transform = `translateX(${posicao}px)`;
}

function logout() {
  localStorage.removeItem("token");
  window.location.href = "login.html";
}
