const TOTAL_DIAS = 30;
const DIA_LIBERADO = 5; // depois vem do backend

function verificarLogin() {
  if (!localStorage.getItem("token")) {
    window.location.href = "login.html";
  }
}

function logout() {
  localStorage.clear();
  window.location.href = "login.html";
}

function gerarDias() {
  const carrossel = document.getElementById("diasCarrossel");

  for (let i = 1; i <= TOTAL_DIAS; i++) {
    const card = document.createElement("div");
    card.className = "dia-card";
    card.innerText = `Dia ${i}`;

    if (i > DIA_LIBERADO) {
      card.classList.add("bloqueado");
    } else {
      card.onclick = () => carregarVideos(i);
    }

    carrossel.appendChild(card);
  }
}

function carregarVideos(dia) {
  const container = document.getElementById("videosContainer");

  container.innerHTML = `
    <div class="video-card">
      <h3>Aula ${dia} – Parte 1</h3>
      <iframe width="100%" height="315"
        src="https://www.youtube.com/embed/VIDEO_ID"
        frameborder="0" allowfullscreen>
      </iframe>
    </div>
  `;
}

function scrollDias(direcao) {
  const carrossel = document.getElementById("diasCarrossel");
  carrossel.scrollLeft += direcao * 300;
}

gerarDias();
