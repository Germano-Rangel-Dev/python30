import { auth, db } from "./firebase.js";
import { doc, getDoc, setDoc } from
  "https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js";

export async function carregarProgresso() {
  const user = auth.currentUser;
  if (!user) return;

  const ref = doc(db, "usuarios", user.uid);
  const snap = await getDoc(ref);

  let ultimaAula = 0;

  if (snap.exists()) {
    ultimaAula = snap.data().ultimaAula || 0;
  }

  aplicarBloqueio(ultimaAula);
  atualizarBarra(ultimaAula);
}

function aplicarBloqueio(ultimaAula) {
  document.querySelectorAll(".aula").forEach(card => {
    const numero = parseInt(card.dataset.aula);

    if (numero > ultimaAula + 1) {
      card.classList.add("bloqueada");
    } else {
      card.classList.remove("bloqueada");
    }
  });
}

function atualizarBarra(ultimaAula) {
  const total = 30;
  const percentual = Math.round((ultimaAula / total) * 100);

  document.getElementById("barraProgresso").style.width = percentual + "%";
  document.getElementById("textoProgresso").innerText = percentual + "%";
}

export async function concluirAula(numeroAula) {
  const user = auth.currentUser;
  if (!user) return;

  await setDoc(doc(db, "usuarios", user.uid), {
    ultimaAula: numeroAula,
    atualizadoEm: new Date()
  }, { merge: true });

  carregarProgresso();
}
