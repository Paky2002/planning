function tariffe () 
{
    var eliminaId = 0;
    var modificaId = 0;
    var tabelle = {};
    var csrftoken = $('meta[name=csrf-token]').attr('content')

    $(document).ready(function() {
        $.ajax({
            type: "POST",
            url: 'getPeriodi', //CHIAMATA PER AVERE GLI ID DELLA TIPOLOGIA
            success: function (d) {
                if (d.data.status == 'success')
                {
                    var periodi = d.data.data.id; //ASSEGNO A UNA VARIABILE LA LISTA DEGLI ID
                    for (var i = 1; i <= periodi.length ; i++) //FACCIIO CICLARE IN BASE AL NUMERO DEGLI ID
                    {
                        var id = 'table' + periodi[i-1]; //CREO STRINGA ID PER POI ASSEGNARLE
                        var tabella = new BSTable(id, { //ASSEGNO ID ALLE MIE TABELLE / CRO OGGETTO DI CLASSE BSTable
                            reset : true,
                            editableColumns: "2,3", //SETTO L'INDEX DELLE COLONNE EDITABILI
                            onEdit: function ($row) {modificaTariffe($row);}, //SETTO LA FUNZIONE DA FARE DOPO IL SEND DELL'EDIT
                            onReset: function ($row) {resetTariffe ($row);}, //SETTO LA FUNZIONE DA FARE DOPO IL SEND DEL DELETE
                            });
                        tabella.init(); //INIZIALIZZO L'OGGETTO
                        tabelle [periodi[i-1]] = tabella; //INSERISCO NEL MIO DIC UNA COPPIA CHIAVE VALORE ID/BSTable
                    }
                }
                else
                {
                    alert (JSON.stringify(d.data.message)) //MESSAGGIO IN CASO DI ERRORE
                }                    
            },
            async: false //SETTO LA CHIAMATA ASYNC PER RIEMPIRE IL DICT
        });

        $('#eliminaPeriodoForm').submit(function (c) {
            var url = "eliminaPeriodo"; // send the form data here.
            $.ajax({
                type: "POST",
                url: url, //CHIAMATA PER ELIMINARE UNA TIPOLOGIA
                data:{'id' : eliminaId},
                success: function (d) {location.reload();} //AGGIORNO LA PAGINA
            });
            c.preventDefault();
        });

        $('#modificaPeriodoForm').submit(function (c) {
            var url = "cambiaPeriodo"; // send the form data here.
            $.ajax({
                type: "POST",
                url: url, //CHIAMATA PER ELIMINARE UNA TIPOLOGIA
                data:{
                    'csrf_token': csrftoken ,
                    'dataInizio' : $('#modificaPeriodoForm').find('#dataInizio').val(),
                    'dataFine' : $('#modificaPeriodoForm').find('#dataFine').val(),
                    'id' : modificaId
                },
                success: function (d) {
                    location.reload(); //AGGIORNO LA PAGINA             
                }
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

    $( ".openModalEliminaPeriodo" ).click(function() {
        eliminaId = $(this).attr('data-periodo');
    });

    $( ".openModalModificaPeriodo" ).click(function() {
        modificaId = $(this).attr('data-periodo');
    });

    function modificaTariffe ($row){ //FUNZIONE CHE VIENE RICHIAMATA QUANDO NELLA TABELLA VIENE CONFERMATA LA NOTIFICA
        console.log ($row)
        var url = "modificaTariffe"; // CHIAMATA PER MODIFICARE IL NUMERO DELLA CAMERA
            $.ajax({
                type: "POST", //
                url: url,
                data:{'dataTariffa' : $row.attr('data-tariffa'),'tipologia' : $row.attr('data-tipo'),'prezzoNotte'  : $row.find('td')[2].outerText,'prezzoSettimana'  : $row.find('td')[3].outerText}, // serializes the form's elements. 
                success: function (d) {
                    if (d.data.status != 'success')
                    {
                        alert (d.data.message)
                    }                  
                }
            });
    }

    function resetTariffe ($row){ //FUNZIONE CHE VIENE RICHIAMATA QUANDO NELLA TABELLA VIENE CONFERMATA LA NOTIFICA
        console.log ($row)
        var url = "resetTariffe"; // CHIAMATA PER MODIFICARE IL NUMERO DELLA CAMERA
            $.ajax({
                type: "POST", //
                url: url,
                data:{'dataTariffa' : $row.attr('data-tariffa'),'tipologia' : $row.attr('data-tipo')}, // serializes the form's elements. 
                success: function (d) {
                    if (d.data.status != 'success')
                    {
                        alert (d.data.message)
                    }                  
                }
            });
    }
}

export {tariffe}