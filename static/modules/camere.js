function camere () {

    //DICHIARO VARIABILI GLOBALI

    var tabelle = {};
    var eliminaId = 0;
    var csrftoken = $('meta[name=csrf-token]').attr('content')

    //SETTO I MIEI EVENTI 

    $(document).ready(function() {
        $.ajax({
            type: "POST",
            url: 'getTipologia', //CHIAMATA PER AVERE GLI ID DELLA TIPOLOGIA
            success: function (d) {
                if (d.data.status == 'success')
                {
                    var tipologiaCamere = d.data.data.id; //ASSEGNO A UNA VARIABILE LA LISTA DEGLI ID
                    for (var i = 1; i <= tipologiaCamere.length ; i++) //FACCIIO CICLARE IN BASE AL NUMERO DEGLI ID
                    {
                        var id = 'table' + tipologiaCamere[i-1]; //CREO STRINGA ID PER POI ASSEGNARLE
                        var tabella = new BSTable(id, { //ASSEGNO ID ALLE MIE TABELLE / CRO OGGETTO DI CLASSE BSTable
                            editableColumns: "0", //SETTO L'INDEX DELLE COLONNE EDITABILI
                            onEdit: function ($row) {modificaCamera ($row);}, //SETTO LA FUNZIONE DA FARE DOPO IL SEND DELL'EDIT
                            onBeforeDelete: function ($row) {eliminaCamera ($row);}, //SETTO LA FUNZIONE DA FARE DOPO IL SEND DEL DELETE
                            });
                        tabella.init(); //INIZIALIZZO L'OGGETTO
                        tabelle [tipologiaCamere[i-1]] = tabella; //INSERISCO NEL MIO DIC UNA COPPIA CHIAVE VALORE ID/BSTable
                    }
                }
                else
                {
                    alert (JSON.stringify(d.data.message)) //MESSAGGIO IN CASO DI ERRORE
                }                    
            },
            async: false //SETTO LA CHIAMATA ASYNC PER RIEMPIRE IL DICT
        });

        $('#eliminaTipologiaForm').submit(function (c) {
            
            var url = "eliminaTipologia"; // send the form data here.
            $.ajax({
                type: "POST",
                url: url, //CHIAMATA PER ELIMINARE UNA TIPOLOGIA
                data:{'id' : eliminaId},
                success: function (d) {
                    location.reload(); //AGGIORNO LA PAGINA             
                }
            });
            c.preventDefault();
        });
    
        $('#formCamera').submit(function (e) {
            var url = "/apiTipologia/"; // send the form data here.
            $.ajax({
                type: "POST",
                url: url, //CHIAMATA PER AGGIUNGERE UNA CAMERA
                data:{
                    'csrf_token': csrftoken ,
                    'numero_camera' : $('#numero_camera').val(),
                    'dataTipologia' : $( "#numero_camera" ).attr( "data-tipologia" )
                }, // serializes the 's elements. 
                success: function (d) {
                    if (d.data.status == 'success')
                    {
                        $("#cameraFisica").modal('hide');
                        tabelle[Number($( "#numero_camera" ).attr( "data-tipologia" ))].aggiungiCamera([$( "#numero_camera" ).val(), d.data.numeroPosti, d.data.data_camera])
                        tabelle[Number($( "#numero_camera" ).attr( "data-tipologia" ))].refresh();
                    }
                    else
                    {
                        alert (JSON.stringify(d.data.message))
                    }                    
                }
            });
            e.preventDefault();// block the traditional submission of the form.
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

    function modificaCamera ($row){ //FUNZIONE CHE VIENE RICHIAMATA QUANDO NELLA TABELLA VIENE CONFERMATA LA NOTIFICA
        var url = "apiModificaCamera"; // CHIAMATA PER MODIFICARE IL NUMERO DELLA CAMERA
            $.ajax({
                type: "POST", //
                url: url,
                data: {dataTipologia : $row.attr('data-camera'),nuovoNumero  : $row.find('td')[0].outerText}, // serializes the form's elements. 
                success: function (d) {
                    if (d.data.status != 'success')
                    {
                        alert (d.data.message)
                    }                  
                }
            });
    }
    
    function eliminaCamera ($row){ //FUNZIONE CHE VIENE RICHIAMATA QUANDO NELLA TABELLA VIENE CONFERMATA L'ELIMINAZIONE
        var url = "apiEliminaCamera"; // CHIAMATA PER ELIMINARE LA CAMERA
            $.ajax({
                type: "POST",
                url: url,
                data: {dataTipologia : $row.attr('data-camera')},
                success: function (d) {
                    if (d.data.status != 'success')
                    {
                        alert (d.data.message)
                    }                  
                }
            });
    }
    
    $( ".openModalAddCamera" ).click(function() {
        $('#numero_camera').attr('data-tipologia', $(this).attr('id'))
    });
    
    $( ".openModalEliminaTipologia" ).click(function() {
        eliminaId = $(this).attr('data-tipologia');
    });
    
    $( ".openModalModificaTipologia" ).click(function() {
        $('#id_tipologia').attr('data-tipologia', $(this).attr('data-tipologia'));
        $('#id_tipologia').attr('value', $(this).attr('data-tipologia'));
        $('#formModificaNumeroPersone').attr('value', $(this).parent().parent().parent().find('td')[0].outerText);
        $('#formModificaTipologia').attr('value', $(this).parent().parent().parent().find('td')[1].outerText);
        $('#formModificaTipo').attr('value', $(this).parent().parent().parent().find('td')[2].outerText);
    });
    
    
}

export {camere}

