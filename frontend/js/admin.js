const tabela = document.getElementById("tabelaAlunos");

// token admin simples (depois vira login)
const ADMIN_TOKEN = "admin123";

fetch("http://127.0.0.1:8000/admin/alunos?token=" + ADMIN_TOKEN)
  .then(res => res.json())
  .then(alunos => {
    alunos.forEach(aluno => {
      const tr = document.createElement("tr");

      tr.innerHTML = `
        <td>${aluno.nome}</td>
        <td>${aluno.dias_liberados}</td>
        <td>
          <button onclick="liberar(${aluno.id})">Liberar +1 dia</button>
        </td>
      `;

      tabela.appendChild(tr);
    });
  });

function liberar(id) {
  fetch(`http://127.0.0.1:8000/admin/liberar-dia?usuario_id=${id}&dias=30&token=${ADMIN_TOKEN}`, {
    method: "POST"
  })
  .then(res => res.json())
  .then(() => {
    alert("Dias liberados!");
    location.reload();
  });
}
