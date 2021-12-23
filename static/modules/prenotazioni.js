function prenotazioni (extraJson, newDictCamera, idExtra)
{
    var json = JSON.parse(extraJson);
    var jsonExtraInseriti = JSON.parse (idExtra)
    var csrftoken = $('meta[name=csrf-token]').attr('content');
    var newCard = $($("#templateCard").html());
    var pricePrice = $($("#pricePrice").html());
    var prezzo = 0;
    var totale = 0;
    var totaleExtra = 0;
    var camereInserite = [];
    var camerePrenotate = [];
    var extra = {};

    if (!$.isEmptyObject(newDictCamera))
    {
        newDictCamera ['extra'] = {}
        newDictCamera ['prezzoExtra'] = 0
        camerePrenotate.push(newDictCamera);
        totaleExtra = 0;
        extra = {};
        $.each (jsonExtraInseriti, function (key, data) {
            $('#mostraExtra').find('[data-idExtra='+key+']').val(data)
            totaleExtra += json [key]['prezzoExtra'] * parseInt(data)
            camerePrenotate [0] ['extra'] [key] = data.toString();
        })
        $(".totaleamera").html(parseInt(newDictCamera['prezzo']) + totaleExtra + '€');
        totale = parseInt(newDictCamera['prezzo'])
        camerePrenotate [0] ['prezzoExtra'] = totaleExtra;
    }
    
    $('#card_').on('click', '#supplemento' ,function(){
        $('#extraSave').attr('data-index', $(this).attr('data-index'));
    })

    $('#extraSave').on('click', function(){
        var indice = $(this).attr('data-index')
        camerePrenotate [indice] ['prezzoExtra'] = 0;
        camerePrenotate [indice] ['extra'] = {};
        var extraExtra = $($("#extraExtra").html());
        var prezzoExtraCamera = 0
        $('.postoExtra').empty()
        var inputExtra = $('#mostraExtra').find('input');
        totaleExtra = 0;
        $.each ($(inputExtra), function (index, value) {
            extraExtra = $($("#extraExtra").html());
            if ($(value).val() != 0)
            {
                camerePrenotate [indice] ['extra'] [$(value).attr('data-idExtra')]= $(value).val();
                prezzoExtraCamera += parseInt(json[$(value).attr('data-idExtra')]['prezzoExtra']) * $(value).val()
                totaleExtra +=  parseInt(json[$(value).attr('data-idExtra')]['prezzoExtra']) * $(value).val()
                camerePrenotate [indice] ['prezzoExtra'] = prezzoExtraCamera;
            }
            console.log (camerePrenotate)
        })

        $(extraExtra).find('.extraNome').empty();
        $(extraExtra).find('.extraPrezzo').empty();
        
        for (var j = 0; j < camerePrenotate.length; j++)
        {
            var associazione = camerePrenotate [j] ['tipo'] + ' ' + camerePrenotate [j] ['numeroStanza']
            $.each(camerePrenotate [j] ['extra'], function(key,value){
                extraExtra = $($("#extraExtra").html());
                $(extraExtra).find('.extraNome').append(value + 'x ' + json[key]['nomeExtra'] + ' ' + '(' + associazione + ')');
                $(extraExtra).find('.extraPrezzo').append(parseInt(json[key]['prezzoExtra']) * value +'€'); 
                extraExtra.appendTo ('.postoExtra');
            });
        }
        
        $('#mostraExtra').modal('hide');
        $(".totaleCamera").html(totale + totaleExtra + '€');
    });


    $('#mostraPreventivi').on('click','#inserisci_', function (){
        newCard = $($("#templateCard").html());
        pricePrice = $($("#pricePrice").html());
        
        var data_dict_room = $(this).parent().parent().attr('data-dict_room');

        $(newCard).find('.tipologiaCard').html(camereInserite[data_dict_room].tipologia); //dateCard
        $(newCard).find('.numeroCameraCard').html(camereInserite[data_dict_room].numeroStanza);
        $(newCard).find('#deleteCard').attr('data-index', camerePrenotate.length)
        $(newCard).find('#supplemento').attr('data-index', camerePrenotate.length)
        $(newCard).find('.dateCard').html($('#formPreventivo').find( "#checkIn" ).val()+' -> '+$('#formPreventivo').find( "#checkOut" ).val());
        $(newCard).find('.tipoCard').html(camereInserite[data_dict_room].tipo);
        $(newCard).find('.trattamentoCard').html($('#formPreventivo').find( "#trattamento" ).val());
        $(newCard).find('.prezzoCard').html(camereInserite[data_dict_room].prezzo+'€');
        newCard.appendTo("#card_");

        if ($('#price_').children().length == 0)
        {
            $($("#templatePrice").html()).appendTo ("#price_");
            $($("#templatePrenota").html()).appendTo ('#prenota_');
        }
          
        $(pricePrice).attr('data-index', camerePrenotate.length)
        $(pricePrice).find('.priceCamera').html ('CAMERA '+camereInserite[data_dict_room].numeroStanza);
        $(pricePrice).find('.pricePrezzo').html (camereInserite[data_dict_room].prezzo + '€');
        pricePrice.appendTo ('.postoPrezzi');
        camerePrenotate.push(camereInserite[data_dict_room]);
        totale += camereInserite[data_dict_room].prezzo;
        $(".totaleCamera").html(totale + totaleExtra + '€');
        $('#mostraPreventivi').modal('hide');
        $('#formPreventivo').find('.clean').val('')
        
    });

    $('#card_').on('click', '#deleteCard', function (){
        $(this).parent().parent().parent().remove();
        if ($('#card_').children().length == 0)
        {
            $("#price_").children().remove();
            $('#prenota_').children().remove();
        }
        totale -= camerePrenotate[$(this).attr('data-index')].prezzo;
        camerePrenotate [$(this).attr('data-index')] ['numeroStanza'] = '000000';
        $(".totaleCamera").html(totale+' €');
        $('.priceIndex[data-index="' + $(this).attr('data-index') + '"]').remove();
    });

    $('#prenota_').on('click', '#prenotaButton',function (){
        var url = "/inserisciPrenotazione"; // send the form data here.
            $.ajax({
                contentType: 'application/json; charset=utf-8',
                type: "POST",
                url: url, //CHIAMATA PER AGGIUNGERE UNA CAMERA
                data: JSON.stringify({'camere' : camerePrenotate}),
                dataType : 'json',
                success: function (d) 
                {
                    window.location.replace("/aggiungiPrenotazione");
                }
            });
        });

    $(document).ready(function() {
        $('#formPreventivo').submit(function (e) {
            var url = "/calcolaPreventivo"; // send the form data here.
            $.ajax({
                type: "POST",
                url: url, //CHIAMATA PER AGGIUNGERE UNA CAMERA
                data:{
                    'csrf_token': csrftoken ,
                    'cognome': $('#formPreventivo').find( "#cognome" ).val(),
                    'checkIn': $('#formPreventivo').find( "#checkIn" ).val(),
                    'checkOut': $('#formPreventivo').find( "#checkOut" ).val(),  
                    'adulti': $('#formPreventivo').find( "#adulti" ).val(),   
                    'ridotti': $('#formPreventivo').find( "#ridotti" ).val(), 
                    'infant': $('#formPreventivo').find( "#infant" ).val(),  
                    'telefono': $('#formPreventivo').find( "#telefono" ).val(),   
                    'email': $('#formPreventivo').find( "#email" ).val(), 
                    'trattamento': $('#formPreventivo').find( "#trattamento" ).val(), 
                }, // serializes the 's elements. 
                success: function (d) {
                    if (d.data.status == 'success')
                    {   
                        $('#tabellaPreventivi').find('tbody').empty();
                        var newColumnHTML = '';
                        var tipologia = '';
                        var index = 0;
                        camereInserite = []
                        $.each(d.data.final,function(key,value){ 
                            newColumnHTML = ''
                            tipologia = key;
                            prezzo = 0;
                            $.each(value,function(key, value){
                                var dictCamera = {};
                                $.each(value, function(key, value){
                                    switch ($('#formPreventivo').find( "#trattamento" ).val())
                                {
                                    case 'Bed&Breakfast' :
                                        prezzo = value.bb;
                                        break

                                    case 'Mezza pensione' :
                                        prezzo = value.mp;
                                        break
                                        
                                    case 'Pensione completa' :
                                        prezzo = value.pc;
                                        break
                                }
                                    newColumnHTML += '<tr data-dict_room="'+index+'"><td class="numeroCameraInfo"><span style="font-size: 100%;" class="badge badge-primary">' + key + '</span></td><td class="tipologiaInfo">'+tipologia+'</td><td class="prezzoInfo" data-prezzo="'+prezzo+'">'+prezzo+'€</td><td><button id="inserisci_" data-idCamera="'+1+'" data-preventivo="'+1+'" class="btn btn-primary px-3 radius-30">-</button></td></tr>';
                                    index +=1;
                                    dictCamera['numeroStanza'] = key;
                                    dictCamera['prezzo'] = prezzo;
                                    dictCamera['tipo'] = value.tipo;
                                    dictCamera['trattamento']= $('#formPreventivo').find( "#trattamento" ).val();
                                    dictCamera['tipologia'] = tipologia;
                                    dictCamera['idPreventivo'] = value.idPreventivo;
                                    dictCamera['idCamera'] = value.idCamera;
                                    dictCamera['extra'] = {};
                                    dictCamera['prezzoExtra'] = '0';
                                    camereInserite.push(dictCamera);
                                });
                            });
                            $('#tabellaPreventivi').find('tbody').append(newColumnHTML);
                        });
                        $("#mostraPreventivi").modal("show");
                        $("#mostraPreventivi").addClass("modal-dialog-scrollable");
                    }                 
                }
            });
            e.preventDefault();
        });
    });
}

export {prenotazioni}
    