let background_colors = ["#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00", "#A65628", "#F781BF"];

function draw_chart_produits(produits) {
    let ctx = document.getElementById("chart_top_produits");

    new Chart(ctx, {
        type: 'bar',
        data: {
            datasets: [{
                data: produits,
                backgroundColor: background_colors
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            parsing: {
                xAxisKey: "stock_code",
                yAxisKey: "nb_ventes"
            }
        }
    });
};

function aucune_donnee(json) {
    return json.length === 0;
};

function update_chart_container(container, html) {
    container.innerHTML = html;
};

function update_chart_produits(json) {
    let chart_container = document.getElementById("chart_container_top_produits");

    if (aucune_donnee(json)) {
        update_chart_container(chart_container, "Aucun produits")
    } else {
        update_chart_container(chart_container, "<canvas id='chart_top_produits'></canvas>")

        draw_chart_produits(json)
    }
};

// afficher le top 10 des produits vendus (graph. affiché par défaut)
ajax_call("GET", "../api/sales_by_products?top=10&format=json", donnees={}, success_callback=update_chart_produits, error_callback=afficher_error);

// Populate select with countries names
// $.ajax({
//     type: "GET",
//     url: "../api/countries?format=json",
//     success: function(json) {
//         let select = document.getElementById("select_pays");

//         json.forEach(element => {
//             let pays = element.country;

//             select.innerHTML = select.innerHTML + `<option value="`+ pays +`">`+ pays +`</option>`;
//         });
//     },
//     error: function(erreur) {
//         afficher_error(erreur)
//     }
// });

// ajouter_ajax_call("#btn_ventes_produits", "GET", "../api/sales_by_products?top=3&format=json");
// ajouter_ajax_call("#btn_ventes_pays", "GET", "../api/sales_by_countries?top=3&format=json");

// add ajax call on form ventes_pays_produits
// $(document).on('submit', "#btn_ventes_pays_produits", function(event){
//     let select = document.getElementById("select_pays");
//     let pays = select.value;

//     event.preventDefault();
//     ajax_call("GET", "../api/sales_of?pays="+ pays +"&top=3&format=json", donnees={}, success_callback=afficher_success, error_callback=afficher_error);
// });
