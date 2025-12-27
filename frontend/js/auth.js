function login(event) {
  event.preventDefault();

  const email = document.getElementById("email").value;
  const senha = document.getElementById("senha").value;
  const erro = document.getElementById("erroMsg");

  erro.innerText = "";

  fetch("http://127.0.0.1:8000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, senha })
  })
  .then(res => {
    if (!res.ok) throw new Error("Credenciais inválidas");
    return res.json();
  })
  .then(data => {
    localStorage.setItem("token", data.access_token);
    window.location.href = "dashboard.html";
  })
  .catch(() => {
    erro.innerText = "E-mail ou senha incorretos";
  });
}

function criarConta(event) {
  event.preventDefault();

  const nome = document.getElementById("nome").value;
  const email = document.getElementById("email").value;
  const senha = document.getElementById("senha").value;
  const confirmar = document.getElementById("confirmarSenha").value;
  const erro = document.getElementById("erroMsg");

  erro.innerText = "";

  if (senha !== confirmar) {
    erro.innerText = "As senhas não coincidem";
    return;
  }

  fetch("http://127.0.0.1:8000/cadastro", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nome, email, senha })
  })
  .then(res => {
    if (!res.ok) throw new Error("Erro ao criar conta");
    return res.json();
  })
  .then(() => {
    alert("Conta criada com sucesso!");
    window.location.href = "login.html";
  })
  .catch(() => {
    erro.innerText = "Erro ao criar conta. Tente outro e-mail.";
  });
}

