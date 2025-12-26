const API = "http://127.0.0.1:8000";

function login() {
  const email = document.getElementById("email").value;
  const senha = document.getElementById("senha").value;

  fetch(API + "/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, senha })
  })
  .then(r => r.json())
  .then(d => {
    if (d.ok) {
      localStorage.setItem("logado", "sim");
      location.href = "dashboard.html";
    } else {
      document.getElementById("msg").innerText = "Login inválido";
    }
  })
  .catch(() => {
    document.getElementById("msg").innerText = "Erro de conexão com o backend";
  });
}

function proteger() {
  if (localStorage.getItem("logado") !== "sim") {
    location.href = "login.html";
  }
}

function logout() {
  localStorage.removeItem("logado");
  location.href = "index.html";
}

function cadastrar() {
  const email = document.getElementById("email").value;
  const senha = document.getElementById("senha").value;

  fetch(API + "/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, senha })
  })
  .then(r => r.json())
  .then(d => {
    if (d.ok) {
      alert("Cadastro realizado com sucesso!");
      location.href = "login.html";
    } else {
      document.getElementById("msg").innerText = d.erro || "Erro no cadastro";
    }
  })
  .catch(() => {
    document.getElementById("msg").innerText = "Erro de conexão";
  });
}

