const TOTAL_DIAS = 30;
const DIA_LIBERADO = 5; // depois vem do backend
const VIDEO_THUMB = "https://img.youtube.com/vi/VIDEO_ID/hqdefault.jpg";

function initDashboard() {
  verificarLogin();
  gerarDias();
  atualizarProgresso();
}

function verificarLogin() {
  if (!localStorage.getItem("token")) {
    window.location.href = "login.html";
  }
}

function logout() {
  localStorage.clear();
  window.location.href = "login.html";
}

/* ===== PROGRESSO ===== */
function atualizarProgresso() {
  const porcentagem = Math.round((DIA_LIBERADO / TOTAL_DIAS) * 100);
  document.getElementById("barraProgresso").style.width = porcentagem + "%";
  document.getElementById("progressoTexto").innerText =
    `Progresso: ${porcentagem}%`;
}

/* ===== DIAS ===== */
function gerarDias() {
  const carrossel = document.getElementById("diasCarrossel");

  for (let i = 1; i <= TOTAL_DIAS; i++) {
    const card = document.createElement("div");
    card.className = "dia-card";
    card.innerText = `Dia ${i}`;

    if (i > DIA_LIBERADO) {
      card.classList.add("bloqueado");
    } else {
      card.onclick = () => selecionarDia(i);
    }

    carrossel.appendChild(card);
  }
}

function scrollDias(dir) {
  document.getElementById("diasCarrossel").scrollLeft += dir * 300;
}

/* ===== SELEÇÃO ===== */
function selecionarDia(dia) {
  carregarVideos(dia);
  carregarPDF(dia);
}

/* ===== VÍDEOS ===== */
function carregarVideos(dia) {
  const container = document.getElementById("videosContainer");
  container.innerHTML = `
    <div class="video-card">
      <h3>Aula ${dia} – Introdução</h3>
      <img src="${VIDEO_THUMB}" width="100%" style="border-radius:8px">
    </div>
  `;
}

/* ===== PDF ===== */
function carregarPDF(dia) {
  const pdf = document.getElementById("pdfContainer");

  pdf.innerHTML = `
    <button onclick="baixarPDF(${dia})">
      📥 Baixar PDF da Aula ${dia}
    </button>
  `;
}

function baixarPDF(dia) {
  fetch(`http://127.0.0.1:8000/pdf/${dia}`, {
    headers: {
      "Authorization": "Bearer " + localStorage.getItem("token")
    }
  })
  .then(res => res.blob())
  .then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `aula${String(dia).padStart(2,'0')}.pdf`;
    a.click();
  });
}