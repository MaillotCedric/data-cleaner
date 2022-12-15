btn_import = document.getElementById("btn_import_csv");
div_loading = document.getElementById("loading_message");

btn_import.addEventListener("click", () => {
    div_loading.innerHTML = "Nettoyage en cours ..."
});
