/* ===============================
   AUTENTICAÇÃO / PROTEÇÃO
================================ */

function protegerPagina() {
  const token = localStorage.getItem("token");
  if (!token) {
    window.location.replace("login.html");
  }
}

function logout() {
  localStorage.removeItem("token");
  window.location.href = "login.html";
}

/* ===============================
   LOGIN
================================ */

async function login() {
  const email = document.getElementById("email").value;
  const senha = document.getElementById("senha").value;

  try {
    const response = await fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
      },
      cache: "no-store",   // 🔴 ISSO RESOLVE O 304
      body: JSON.stringify({ email, senha })
    });

    if (!response.ok) {
      alert("Login inválido");
      return;
    }

    const data = await response.json();

    localStorage.setItem("token", data.token);

    window.location.href = "index.html";

  } catch (error) {
    console.error(error);
    alert("Erro de conexão com o servidor");
  }
}

/* ===============================
   DASHBOARD
================================ */

function carregarDashboard() {
  const token = localStorage.getItem("token");
  const el = document.getElementById("token");
  if (el && token) {
    el.innerText = token;
  }
}

/* ===============================
   SIDEBAR (MOBILE)
================================ */

function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  const isMobile = window.innerWidth < 1024;

  // no mobile o botão controla
  if (isMobile) {
    sidebar.classList.toggle("ativa");
    sidebar.classList.toggle("fechada");
  }
}

/* ===============================
   CARROSSEL DE AULAS
================================ */

function scrollAulas(direcao) {
  const carousel = document.getElementById("carouselAulas");
  if (!carousel) return;

  const aula = carousel.querySelector(".aula");
  if (!aula) return;

  const gap = 16;
  const scrollAmount = aula.offsetWidth + gap;

  carousel.scrollLeft += direcao * scrollAmount;
}

/* ===============================
   AULAS / PROGRESSO
================================ */

const TOTAL_AULAS = 30;

function carregarProgresso() {
  let aulaAtual = parseInt(localStorage.getItem("aulaAtual")) || 1;

  const aulas = document.querySelectorAll(".aula");

  aulas.forEach(aula => {
    const numero = parseInt(aula.dataset.aula);

    if (numero > aulaAtual) {
      aula.classList.add("bloqueada");
      aula.onclick = null;
    } else {
      aula.classList.remove("bloqueada");
      aula.onclick = () => abrirAula(numero);
    }
  });

  atualizarProgresso(aulaAtual);
}

function abrirAula(numero) {
  // aqui futuramente entra a página real da aula
  alert(`Abrindo Aula ${numero}`);

  // simulação de conclusão automática
  concluirAula(numero);
}

function concluirAula(numero) {
  let aulaAtual = parseInt(localStorage.getItem("aulaAtual")) || 1;

  if (numero === aulaAtual && aulaAtual < TOTAL_AULAS) {
    aulaAtual++;
    localStorage.setItem("aulaAtual", aulaAtual);
  }

  carregarProgresso();
}

function atualizarProgresso(aulaAtual) {
  const porcentagem = Math.round(((aulaAtual - 1) / TOTAL_AULAS) * 100);

  const barra = document.getElementById("barraProgresso");
  const texto = document.getElementById("textoProgresso");

  if (barra) barra.style.width = porcentagem + "%";
  if (texto) texto.innerText = `${porcentagem}% concluído`;
}

/* ===============================
   INICIALIZAÇÃO SEGURA
================================ */

document.addEventListener("DOMContentLoaded", () => {
  carregarDashboard();
  carregarProgresso();
});
