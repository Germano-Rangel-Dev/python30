import { auth, db } from "./firebase.js";
import { createUserWithEmailAndPassword } from
  "https://www.gstatic.com/firebasejs/10.12.0/firebase-auth.js";

import { doc, setDoc } from
  "https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js";

window.cadastrar = async function () {
  const email = document.getElementById("email").value.trim();
  const senha = document.getElementById("senha").value;

  if (!email || !senha) {
    alert("Preencha email e senha");
    return;
  }

  try {
    // 1️⃣ Cria usuário no Auth
    const cred = await createUserWithEmailAndPassword(auth, email, senha);
    const user = cred.user;

    // 2️⃣ Cria perfil no Firestore
    await setDoc(doc(db, "usuarios", user.uid), {
      email: email,
      role: "aluno",        // 👈 automático
      ultimaAula: 0,
      criadoEm: new Date()
    });

    alert("Conta criada com sucesso!");
    window.location.href = "login.html";

  } catch (err) {
    alert("Erro no cadastro: " + err.message);
  }
};
