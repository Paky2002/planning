function preventivi (extraJson) 
{
    var jsonExtra = JSON.parse (extraJson)
    var csrftoken = $('meta[name=csrf-token]').attr('content');
    var newColumnHTML = '';
    var camereInserite = [];
    var sovraPrezzo = 0;

    var idArr = [];

    $('#openModalExtra').on('click', function(){
        $("#mostraPreventivi").modal("hide");
        $('#mostraExtra').modal('show');
    });

    $('#extraSave').on('click', function(){
        var extraDatas = $('#extra').find('.extraData');
        sovraPrezzo = 0;
        var prezzoMaggiore = 0;
        idArr = [];
        $.each(extraDatas, function(index, value){
            if ($(value).find('input').val() > 0)
            {
                for (var i  = 0; i < $(value).find('input').val(); i++)
                {
                    idArr.push($(value).children('div').attr('data-idExtra'));
                }
                console.log (idArr);
            }
            
            sovraPrezzo += parseInt($(value).children('div').children('input').val()) * parseInt(jsonExtra[$(value).children('div').attr('data-idExtra')]['prezzoExtra']);
        });

        var prezziRiga = $('#tabellaPreventivi').find('tbody').find('tr');
        $.each(prezziRiga, function (index, value){
            $.each($(value).find('.prezzi'), function(index, value){
                console.log ($(value).attr('data_prezzo_'))
                prezzoMaggiore = parseInt($(value).attr('data-prezzo_')) + parseInt(sovraPrezzo);
                $(value).html(prezzoMaggiore+'€');
            });
        });
        $("#mostraPreventivi").modal("show");
        $('#mostraExtra').modal('hide');
    });

    $('#extraClose').on('click', function(){
        var extraDatas = $('#extra').find('.extraData');
        $.each(extraDatas, function(index, value){
            $(value).children('div').children('input').val(0);
        });
        $("#mostraPreventivi").modal("show");
        $('#mostraExtra').modal('hide');
    });

    $('#mostraPreventivi').on('click', '#inserisci',function(){
        $('#trattamentoSave').attr('data-index', $(this).attr('data-index'));
        $('#mostraTrattamento').modal('show'); 
    });

    $('#trattamentoSave').on('click', function(){
        var urlRedirect = '/createPrenotazione?trattamento='+$('#trattamentoInserisci').val()+'&idCamera='+camereInserite [$(this).attr('data-Index')]['idCamera']+'&prezzo='+camereInserite[$(this).attr('data-index')][$('#trattamentoInserisci').val()]+'&idPreventivo='+camereInserite [$(this).attr('data-Index')]['idPreventivo']+'&prezzoSupplementi='+sovraPrezzo;
        for (var i= 0; i < idArr.length; i++)
        {
            urlRedirect += '&idExtra=' + idArr [i];
        }
        $('#formPreventivo').attr('action', urlRedirect)
        $('#formPreventivo').submit()
    });

    $('#trattamentoClose').on('click', function(){
        $('#mostraTrattamento').modal('hide'); 
    });

    $(document).ready(function() {
        $('#bottoneMostraPreventivo').on('click', function () {
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
                }, // serializes the 's elements. 
                success: function (d) {
                    if (d.data.status == 'success')
                    {   
                        $('#tabellaPreventivi').find('tbody').empty();
                        var tipologia = '';
                        var index = 0;
                        $.each(d.data.final,function(key,value){ 
                            var dictCamera = {};
                            newColumnHTML = ''
                            tipologia = key;
                            $.each(value,function(key, value){
                                $.each(value, function(key, value){
                                    newColumnHTML += '<tr><td><span style="font-size: 100%;" class="badge badge-primary">' + key + '</span></td><td>'+tipologia+'</td><td data-prezzo_="'+value.bb+'" class="prezzi">'+value.bb+'€</td><td data-prezzo_="'+value.mp+'" class="prezzi">'+value.mp+'€</td><td data-prezzo_="'+value.pc+'" class="prezzi">'+value.pc+'€</td><td class="d-flex justify-content-center"><button id="inserisci" data-index = "'+index+'" style="width:100%;border:none;width:20px;height:20px" type="submit" class="btn btn-primary px-3 radius-30 d-flex justify-content-center align-items-center"><i style="font-size:10px"class="bi bi-app-indicator"></i></button></td></tr>';
                                    dictCamera['bb'] = value.bb;
                                    dictCamera['mp'] = value.mp;
                                    dictCamera['pc'] = value.pc;
                                    dictCamera['idCamera'] = value.idCamera;
                                    dictCamera['idPreventivo'] = value.idPreventivo;
                                    camereInserite.push(dictCamera);
                                    index += 1;
                                });
                                
                            });
                            $('#tabellaPreventivi').find('tbody').append(newColumnHTML);
                        });
                        $("#mostraPreventivi").modal("show");
                        $("#mostraPreventivi").addClass("modal-dialog-scrollable");
                    }                 
                }
            });
        });
    });
}

export {preventivi}