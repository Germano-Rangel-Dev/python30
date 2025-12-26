function login() {
  localStorage.setItem("logado", "sim");
  location.href = "dashboard.html";
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
