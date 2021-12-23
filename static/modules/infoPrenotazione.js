function infoPrenotazione () {

    $('').on('click', function(){
        var bottoni = $('#statoSoggiornoGroup').find('button')
        switch ($(this).attr('id'))
        {
            case 1 :
                bottoni[0].removeClass('btn-warning')
                break;
            
            case 2 :
                break;

            case 3 :
                break;
        }
    })
}