let background_colors = ["#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00", "#A65628", "#F781BF"];

function draw_chart_produits(produits) {
    let ctx = document.getElementById("chart_top_produits");
    let nb_produits = produits.length;

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
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "produits",
                        font: {
                            size: 14,
                            weight: "bold"
                        }
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "nombre de ventes",
                        font: {
                            size: 14,
                            weight: "bold"
                        }
                    }
                }
            },
            parsing: {
                xAxisKey: "stock_code",
                yAxisKey: "nb_ventes"
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: "Top "+ nb_produits +" des produits les plus vendus",
                    position: "top",
                    font: {
                        size: 16,
                        weight: "bold"
                    },
                    color: "black"
                }
            }
        }
    });
};

function draw_chart_pays_produits(produits) {
    let ctx_pays_produits = document.getElementById("chart_top_pays_produits");
    let pays_selectionne = produits[0].country;

    new Chart(ctx_pays_produits, {
        type: 'bar',
        data: {
            datasets: [{
                data: produits,
                backgroundColor: background_colors
            }]
        },
        options: {
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "produits",
                        font: {
                            size: 14,
                            weight: "bold"
                        }
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "nombre de ventes",
                        font: {
                            size: 14,
                            weight: "bold"
                        }
                    }
                }
            },
            parsing: {
                xAxisKey: "stock_code",
                yAxisKey: "nb_ventes"
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: "Top 10 des produits les plus vendus pour " + pays_selectionne,
                    position: "top",
                    font: {
                        size: 16,
                        weight: "bold"
                    },
                    color: "black"
                }
            }
        }
    });
};

function click_on_bar(pointer) {
    return pointer.length !== 0;
};

function draw_chart_pays(pays) {
    let ctx_pays = document.getElementById("chart_top_pays");

    let my_chart = new Chart(ctx_pays, {
        type: 'bar',
        data: {
            datasets: [{
                data: pays,
                backgroundColor: background_colors
            }]
        },
        options: {
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "pays",
                        font: {
                            size: 14,
                            weight: "bold"
                        }
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "nombre de ventes",
                        font: {
                            size: 14,
                            weight: "bold"
                        }
                    },
                    type: "logarithmic"
                }
            },
            parsing: {
                xAxisKey: "country",
                yAxisKey: "nb_ventes"
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: "Top 10 des pays de livraison",
                    position: "top",
                    font: {
                        size: 16,
                        weight: "bold"
                    },
                    color: "black"
                }
            },
            onClick(event) {
                let intersection = {
                    intersect: true
                };
                let pointer = my_chart.getElementsAtEventForMode(event, 'nearest', intersection, false);
            
                if (click_on_bar(pointer)) {
                    let index = pointer[0].index;
                    let pays_selectionne = pays[index].country; 

                    ajax_call("GET", "../api/sales_of?pays="+ pays_selectionne +"&top=10&format=json", donnees={}, success_callback=update_chart_pays_produits, error_callback=afficher_error);
                };
            }
        }
    });
};

function aucune_donnee(json) {
    return json.length === 0;
};

function update_chart_container(container, html) {
    container.innerHTML = `
        <div>
        `+ html +`
        </div>
    `;
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

function update_chart_pays(json) {
    let chart_container = document.getElementById("chart_container_top_pays");

    if (aucune_donnee(json)) {
        update_chart_container(chart_container, "Aucun pays")
    } else {
        update_chart_container(chart_container, "<canvas id='chart_top_pays'></canvas>")

        draw_chart_pays(json)
    }
};

function update_chart_pays_produits(json) {
    let chart_container = document.getElementById("chart_container_top_pays_produits");

    update_chart_container(chart_container, "<canvas id='chart_top_pays_produits'></canvas>");
    draw_chart_pays_produits(json);
};

// afficher le top 10 des produits vendus (graph. affiché par défaut)
ajax_call("GET", "../api/sales_by_products?top=10&format=json", donnees={}, success_callback=update_chart_produits, error_callback=afficher_error);

// afficher le top 10 des pays de livraison
// ajax_call("GET", "../api/sales_by_countries?top=10&format=json", donnees={}, success_callback=update_chart_pays, error_callback=afficher_error);

// Populate select with years
$.ajax({
    type: "GET",
    url: "../api/years?format=json",
    success: function(json) {
        let select = document.getElementById("select_years");

        json.forEach(element => {
            let year = element.year;

            select.innerHTML = select.innerHTML + `<option value="`+ year +`">`+ year +`</option>`;
        });
    },
    error: function(erreur) {
        afficher_error(erreur)
    }
});

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

function get_values_select() {
    let values = [];
    let selects = document.getElementsByClassName("form-select");
    
    for (let index = 0; index < selects.length; index++) {
        let select = selects[index];
        let name = select.name;
        let value = select.options[select.selectedIndex].value;

        values.push({
            "name": name,
            "value": value
        });
    };

    return values;
};

function get_params(values_selects) {
    params = "?";

    values_selects.forEach(value_select => {
        let name = value_select.name;
        let value = value_select.value;

        if (value !== "") {
            params += name + "=" + value + "&";
        };
    });
    params === "?" ? params += "&format=json" : params += "format=json";

    return params;
};

function get_requete_produits(values_selects) {
    let params = get_params(values_selects);
    let requete_produits = "../api/sales_by_products" + params;

    return requete_produits;
};

function enlever_classe(nom_classe, element_html) {
    element_html.classList.remove(nom_classe);
};

function ajouter_classe(nom_classe, element_html) {
    element_html.classList.add(nom_classe);
};

function apply_filters_produits(json) {
    ajouter_classe("d-none", loading_modal);
    update_chart_produits(json);
};

$(document).on('click', "#btn_filtrer", function(event){
    let values_selects = get_values_select();
    let requete_produits = get_requete_produits(values_selects);
    let div_loading = document.getElementById("loading_message");

    enlever_classe("d-none", loading_modal);
    div_loading.innerHTML = "Veuillez patienter ...";
    ajax_call("GET", requete_produits, donnees={}, success_callback=apply_filters_produits, error_callback=afficher_error);
});
