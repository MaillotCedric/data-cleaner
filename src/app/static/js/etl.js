btn_import = document.getElementById("btn_import_csv");
btn_import_bdd = document.getElementById("btn_import_bdd");
div_loading = document.getElementById("loading_message");
file_input = document.getElementById("id_fichier");
loading_modal = document.getElementById("loading_modal");

function est_present(element_html) {
    return element_html != null;
};

function est_visible(btn) {
    return !btn.classList.value.split(" ").includes("d-none");
};

function enlever_classe(nom_classe, element_html) {
    element_html.classList.remove(nom_classe);
};

btn_import.addEventListener("click", () => {
    enlever_classe("d-none", loading_modal);
    div_loading.innerHTML = "Nettoyage en cours ...";
});

if (est_present(btn_import_bdd)) {
    btn_import_bdd.addEventListener("click", () => {
        enlever_classe("d-none", loading_modal);
        div_loading.innerHTML = "Importation en base de données ...";
    });
};

file_input.addEventListener("input", () => {
    if (!est_visible(btn_import)) {
        enlever_classe("d-none", btn_import);
    }
});
