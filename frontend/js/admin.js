import { auth, db } from "./firebase.js";
import {
  collection, getDocs
} from "https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js";

async function carregarAlunos() {
  const lista = document.getElementById("listaAlunos");
  lista.innerHTML = "";

  const query = await getDocs(collection(db, "usuarios"));

  query.forEach(doc => {
    const user = doc.data();

    if (user.role === "aluno") {
      lista.innerHTML += `
        <div class="card">
          <p><strong>Email:</strong> ${user.email}</p>
          <p><strong>Última aula:</strong> ${user.ultimaAula || 0}</p>
        </div>
      `;
    }
  });
}

window.addEventListener("load", carregarAlunos);
