function afficher_success(reponse) {
    afficher("success : ");
    afficher(reponse);
};

function afficher_error(error) {
    afficher("erreur : ");
    afficher(error);
};

function ajax_call(methode, ajax_url, donnees, success_callback, error_callback) {
    let csrftoken = majuscule(methode) === "POST" ? document.querySelector('[name=csrfmiddlewaretoken]').value : "";

    $.ajax({
        type: methode,
        url: ajax_url,
        headers:{'X-CSRFToken': csrftoken},
        data: donnees,
        success: function(json) {
            success_callback(json);
        },
        error: function(erreur) {
            error_callback(erreur);
        }
    });
};

function ajouter_ajax_call(element_id, methode, ajax_url, donnees={}, success_callback=afficher_success, error_callback=afficher_error) {
    $(document).on('submit', element_id, function(event){
        event.preventDefault();
    
        ajax_call(methode, ajax_url, donnees, success_callback, error_callback);
    });
};
