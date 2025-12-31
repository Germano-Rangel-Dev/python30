function protegerPagina() {
  if (!localStorage.getItem("token")) {
    window.location.replace("login.html");
  }
}

function carregarDashboard() {
  const token = localStorage.getItem("token");
  const el = document.getElementById("token");
  if (el && token) {
    el.innerText = token;
  }
}

function logout() {
  localStorage.removeItem("token");
  window.location.href = "login.html";
}

function login() {
  const email = document.getElementById("email").value;
  const senha = document.getElementById("senha").value;

  fetch("http://127.0.0.1:8000/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-cache"
    },
    body: JSON.stringify({
      email: email,
      senha: senha
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.token) {
      localStorage.setItem("token", data.token);
      window.location.href = "index.html";
    } else {
      alert("Login inválido");
    }
  })
  .catch(err => {
    alert("Erro de conexão");
    console.error(err);
  });
}
