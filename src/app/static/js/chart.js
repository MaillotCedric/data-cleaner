// Populate select with countries names
$.ajax({
    type: "GET",
    url: "../api/countries?format=json",
    success: function(json) {
        let select = document.getElementById("select_pays");

        json.forEach(element => {
            let pays = element.country;

            select.innerHTML = select.innerHTML + `<option value="`+ pays +`">`+ pays +`</option>`;
        });
    },
    error: function(erreur) {
        afficher_error(erreur)
    }
});

ajouter_ajax_call("#btn_ventes_produits", "GET", "../api/sales_by_products?top=3&format=json");
ajouter_ajax_call("#btn_ventes_pays", "GET", "../api/sales_by_countries?top=3&format=json");

// add ajax call on form ventes_pays_produits
$(document).on('submit', "#btn_ventes_pays_produits", function(event){
    let select = document.getElementById("select_pays");
    let pays = select.value;

    event.preventDefault();
    ajax_call("GET", "../api/sales_of?pays="+ pays +"&top=3&format=json", donnees={}, success_callback=afficher_success, error_callback=afficher_error);
});
