function extra () {
    var csrftoken = $('meta[name=csrf-token]').attr('content')
    var tabella = new BSTable('table', { //ASSEGNO ID ALLE MIE TABELLE / CRO OGGETTO DI CLASSE BSTable
        editableColumns: "0,1,2", //SETTO L'INDEX DELLE COLONNE EDITABILI
        onEdit: function ($row) {modificaExtra ($row)}, //SETTO LA FUNZIONE DA FARE DOPO IL SEND DELL'EDIT
        onBeforeDelete: function ($row) {eliminaExtra ($row)}, //SETTO LA FUNZIONE DA FARE DOPO IL SEND DEL DELETE
        });
    tabella.init(); //INIZIALIZZO L'OGGETTO

    $(document).ready(function() {
        $('#aggiungiExtraForm').submit(function (c) {
            var url = "aggiungiExtra"; // send the form data here.
            $.ajax({
                type: "POST",
                url: url, //CHIAMATA PER ELIMINARE UNA TIPOLOGIA
                data:{
                    'csrf_token': csrftoken ,
                    'nomeExtra' : $('#aggiungiExtraForm').find('#nomeExtra').val(),
                    'prezzoExtra' : $('#aggiungiExtraForm').find('#prezzoExtra').val(),
                    'tipoExtra' : $('#aggiungiExtraForm').find('#tipoExtra').val()
                },
                success: function (d) {
                    $("#aggiungiExtraModal").modal('hide');
                    tabella.aggiungiExtra([d.data.nomeExtra, d.data.prezzoExtra, d.data.tipoExtra])
                    tabella.refresh();
                } //AGGIORNO LA PAGINA
            });
            c.preventDefault();
        });
        // Inject our CSRF token into our AJAX request.
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
            }
        })
    });

    function modificaExtra ($row)
    {
        var url = 'modificaExtra';
        $.ajax({
            type: "POST",
            url: url, 
            data:{'csrf_token': csrftoken ,'nomeExtra' : $row.find('td')[0].outerText,'prezzoExtra' : $row.find('td')[1].outerText,'tipoExtra' : $row.find('td')[2].outerText, 'id' : $row.attr('data-extra')},
        });
    }

    function eliminaExtra ($row)
    {
        var url = 'eliminaExtra';
        $.ajax({
            type: "POST",
            url: url, 
            data:{'csrf_token': csrftoken , 'id' : $row.attr('data-extra')}
        });
    }
}

export {extra}