async function reformuler() {
    const texte = document.getElementById("texte").value;

    const response = await fetch("/reformuler", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ texte })
    });

    const data = await response.json();
    document.getElementById("resultat").innerHTML = data.reformulation;
}
