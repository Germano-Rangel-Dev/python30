import { auth, db } from "./firebase.js";
import { signInWithEmailAndPassword } from
  "https://www.gstatic.com/firebasejs/10.12.0/firebase-auth.js";

import { doc, getDoc } from
  "https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js";

window.login = async function () {
  const email = document.getElementById("email").value.trim();
  const senha = document.getElementById("senha").value;

  if (!email || !senha) {
    alert("Preencha email e senha");
    return;
  }

  try {
    // Login Firebase
    const cred = await signInWithEmailAndPassword(auth, email, senha);
    const user = cred.user;

    // Busca perfil no Firestore
    const ref = doc(db, "usuarios", user.uid);
    const snap = await getDoc(ref);

    if (!snap.exists()) {
      alert("Usuário sem perfil no sistema.");
      return;
    }

    const dados = snap.data();

    // Redirecionamento por role
    if (dados.role === "admin") {
      window.location.href = "admin.html";
    } else {
      window.location.href = "index.html";
    }

  } catch (err) {
    alert("Erro no login: " + err.message);
  }
};
