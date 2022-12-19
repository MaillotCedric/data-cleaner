btn_import = document.getElementById("btn_import_csv");
btn_import_bdd = document.getElementById("btn_import_bdd");
div_loading = document.getElementById("loading_message");

function est_present(element_html) {
    return element_html != null;
};

btn_import.addEventListener("click", () => {
    div_loading.innerHTML = "Nettoyage en cours ..."
});

if (est_present(btn_import_bdd)) {
    btn_import_bdd.addEventListener("click", () => {
        div_loading.innerHTML = "Importation en bdd ..."
    });
};
