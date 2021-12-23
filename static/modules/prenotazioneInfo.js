function prenotazioneInfo (idPrenotazione) {
    
        new PerfectScrollbar('.dashboard-dettagli-prenotazioni'); 
		new PerfectScrollbar('.listExtra');
		new PerfectScrollbar('.scrollContatti'); 
		new PerfectScrollbar('.pagamentiList'); 

		var contattoModificato = 0
		var idPrenotazione = idPrenotazione;
		var csrftoken = $('meta[name=csrf-token]').attr('content');

		//ATTIVITA SUGLI EXTRA

		$('#formAggiungiExtraPrenotazione').submit(function (e) {
				var url = "/aggiungiExtraPrenotazione"; // send the form data here.
				$.ajax({
					type: "POST",
					url: url, //CHIAMATA PER AGGIUNGERE UNA CAMERA
					data:{
						'csrf_token': csrftoken ,
						'nome': $('#formAggiungiExtraPrenotazione').find( "#nome" ).val(),
						'quantita': $('#formAggiungiExtraPrenotazione').find( "#quantita" ).val(),
						'prezzo': $('#formAggiungiExtraPrenotazione').find( "#prezzo" ).val(),
						'idPrenotazione' : idPrenotazione
					},
					success: function (d) {
						if (d.data.status == 'success')
						{
							var extraTemplate = $($("#extraTemplate").html());
							$(extraTemplate).find('#quantitaNomeExtraTemplate').html('x'+d.data.newDictExtra['quantita']+d.data.newDictExtra['nome'])
							$(extraTemplate).find('#prezzoExtraTemplate').text(d.data.newDictExtra['prezzo']+'€')
							$(extraTemplate).find('.deleteExtra').attr('data-idextra', d.data.newDictExtra['id'])
							extraTemplate.appendTo('.listExtra')
							aggiornaDati (d.data.dictAggiornato)
							notifica_success(d.data.msg);
						}

						if (d.data.status == 'error')
						{
							notifica_errore(d.data.msg);
						}
						
					}
				})
				e.preventDefault();
			})

		$('#mostraExtra').on('click', '.deleteExtra', function (e) {
				var url = "/eliminaExtraPrenotazione"; // send the form data here.
				$.ajax({
					type: "POST",
					url: url, //CHIAMATA PER AGGIUNGERE UNA CAMERA
					data:{
						'csrf_token': csrftoken ,
						'idExtra': $(this).attr("data-idextra"),
						'idPrenotazione' : idPrenotazione
					},
					success: function (d) {
						if (d.data.status == 'success')
						{
							$('div [data-idextra = '+d.data.id+']').parent().parent().parent().parent().remove();
							aggiornaDati (d.data.dictAggiornato)
							notifica_success(d.data.msg);
						}

						if (d.data.status == 'error')
						{
							notifica_errore(d.data.msg);
						}
						
					}
				})
			})

		//FINE ATTIVITA SUGLI EXTRA

		//ATTIVITA SUI SUPPLEMENTI

		$('#salvaSupplementi').on('click', function (){
			var inputSupplementi = $('#mostraSupplementi').find('input');
			var dictSupplementi = {}

			$.each (inputSupplementi, function(index, value){
				if ($(value).val != 0)
				{
					dictSupplementi [$(value).attr('data-idSupplemento')] = $(value).val();
				}
			})
			var url = '/modificaSupplementiPrenotazione';
			$.ajax ({
				contentType: 'application/json; charset=utf-8',
				type : 'POST', 
				url : '/modificaSupplementiPrenotazione',
				data : JSON.stringify({'idPrenotazione' : idPrenotazione, 'dictSupplementi': dictSupplementi}),
				dataType : 'json',
				success: function (d) {
					if (d.data.status == 'success')
					{	
						$.each (inputSupplementi, function(index, value){
						{
							$(value).attr('data-lastModify', $(value).val());
						}})

						aggiornaDati (d.data.dictAggiornato)
						notifica_success(d.data.msg);
					}
					
					if (d.data.status == "error")
					{
						notifica_errore(d.data.msg);
					}
				}
			})
		});

		$('#supplementiClose').on('click', function (){
			var inputSupplementi = $('#mostraSupplementi').find('input');
			$.each (inputSupplementi, function(index, value){
				$(value).val($(value).attr('data-lastModify'));
			})
		})


		//FINE ATTIVITA SUI SUSPPLEMENTI

		//ATTIVITA SUI PAGAMENTI

		$('#formAggiungiPagamentoPrenotazione').submit(function (e) {
				var url = "/aggiungiPagamentoPrenotazione"; // send the form data here.
				$.ajax({
					type: "POST",
					url: url, //CHIAMATA PER AGGIUNGERE UNA CAMERA
					data:{
						'csrf_token': csrftoken ,
						'pagamento': $('#formAggiungiPagamentoPrenotazione').find( "#pagamento" ).val(),
						'idPrenotazione' : idPrenotazione
					},
					success: function (d) {
						if (d.data.status == 'success')
						{
							var pagamentoTemplate = $($("#pagamentoTemplate").html());
							$(pagamentoTemplate).find('.dataPagamento').html(d.data.newDictPagamento['data'])
							$(pagamentoTemplate).find('.prezzoPagamento').text(d.data.newDictPagamento['pagamento']+'€')
							$(pagamentoTemplate).find('.deletePagamento').attr('data-idPagamento', d.data.newDictPagamento['id'])
							pagamentoTemplate.appendTo('.pagamentiList')
							aggiornaDati (d.data.dictAggiornato)
							notifica_success(d.data.msg);
						}

						if (d.data.status == 'error')
						{
							notifica_errore(d.data.msg);
						}
						
					}
				})
				e.preventDefault();
			})

			$('#mostraPagamenti').on('click','.deletePagamento',function (e) {
				var url = "/eliminaPagamentoPrenotazione"; // send the form data here.
				$.ajax({
					type: "POST",
					url: url, //CHIAMATA PER AGGIUNGERE UNA CAMERA
					data:{
						'csrf_token': csrftoken ,
						'idPagamento': $(this).attr("data-idPagamento"),
						'idPrenotazione' : idPrenotazione
					},
					success: function (d) {
						if (d.data.status == 'success')
						{
							$('div [data-idPagamento = '+d.data.id+']').parent().parent().parent().parent().remove();
							aggiornaDati (d.data.dictAggiornato)
							notifica_success(d.data.msg);
						}

						if (d.data.status == 'error')
						{
							notifica_errore(d.data.msg);
						}
						
					}
				})
				e.preventDefault();
			})

		//FINE ATTIVITA SUI PAGAMENTI

		//ATTIVITA SU CLIENTI

		$('#formRegistrazioneCliente').submit(function(){
			$(this).find('#csrf_token').val(csrftoken)
			if (contattoModificato == 0)
			{
				$(this).attr('action', '/registraCliente/'+idPrenotazione);
			}
			else
			{
				$(this).attr('action', '/registraCliente/'+idPrenotazione+'/'+contattoModificato);
			}
			
		})	

		$('#buttonCloseContatti').on('click', function(){
			contattoModificato = 0
		})

		$('#deleteContatto').on('click', function(){
			var url = '/eliminaContatto';
			$.ajax({
				type : 'POST',
				url : url,
				data : {'idPrenotazione' : idPrenotazione, 'idContatto' : contattoModificato},
				success : function (d) {
					if (d.data.status == 'success')
					{
						$('div [data-idContatto='+contattoModificato+']').parent().remove();
						contattoModificato = 0;
						$('#mostraRegistraCliente').modal('hide')
						notifica_success(d.data.msg)
						aggiornaDati (d.data.dictAggiornato)
					}
					
					if (d.data.status == 'error')
					{
						notifica_errore(d.data.msg)
					}
				}
		})
	})

		$('#buttonRegistraCliente').on('click', function (){
			$('#deleteContatto').hide()
			$('#formRegistrazioneCliente').find('input').val('')
		})

		$('.openModalRegistraCliente').on('click', function(){
			var url = '/getContatto';
			$.ajax({
				type : 'POST',
				url : url,
				data : {'idPrenotazione' : idPrenotazione, 'idContatto' : $(this).attr('data-idContatto')},
				success : function (d) {
					if (d.data.status == 'success')
					{
						$('#mostraRegistraCliente').find('#nome').val(d.data.conctat ['nome'])
						$('#mostraRegistraCliente').find('#cognome').val(d.data.conctat ['cognome'])
						$('#mostraRegistraCliente').find('#cittadinanza').val(d.data.conctat ['cittadinanza'])
						$('#mostraRegistraCliente').find('#sesso').val(d.data.conctat ['sesso'])
						$('#mostraRegistraCliente').find('#telefono').val(d.data.conctat ['telefono'])
						$('#mostraRegistraCliente').find('#email').val(d.data.conctat ['email'])
						$('#mostraRegistraCliente').find('#dataDiNascita').val(new Date(d.data.conctat ['dataDiNascita']).toISOString().split('T')[0])
						$('#mostraRegistraCliente').find('#paeseNascita').val(d.data.conctat ['paeseNascita'])
						$('#mostraRegistraCliente').find('#comuneNascita').val(d.data.conctat ['comuneNascita'])
						$('#mostraRegistraCliente').find('#paeseResidenza').val(d.data.conctat ['paeseResidenza'])
						$('#mostraRegistraCliente').find('#comuneResidenza').val(d.data.conctat ['comuneResidenza'])
						$('#mostraRegistraCliente').find('#cap').val(d.data.conctat ['cap'])
						$('#mostraRegistraCliente').find('#indirizzo').val(d.data.conctat ['indirizzo'])
						$('#mostraRegistraCliente').find('#documento').val(d.data.conctat ['documento'])
						$('#mostraRegistraCliente').find('#paeseImmissione').val(d.data.conctat ['paeseImmissione'])
						$('#mostraRegistraCliente').find('#numeroDocumento').val(d.data.conctat ['numeroDocumento'])
						$('#mostraRegistraCliente').find('#emessoDa').val(d.data.conctat ['emessoDa'])
						$('#mostraRegistraCliente').find('#dataEmissione').val(new Date(d.data.conctat ['dataEmissione']).toISOString().split('T')[0])
						$('#mostraRegistraCliente').find('#dataScadenza').val(new Date(d.data.conctat ['dataScadenza']).toISOString().split('T')[0])
						contattoModificato = d.data.conctat ['id']
						$('#deleteContatto').show()
						$('#mostraRegistraCliente').modal('show')
					}
					if (d.data.stuts == 'error')
					{
						notifica_errore(d.data.msg);
					}
				} 
			})
		})

		//FINE ATTIVITA SU CLIENTI
		
		$('.custom-switch').on('change', function (){
			$.ajax ({
				type : 'post',
				url : '/activeTassaSoggiorno',
				data : {'idPrenotazione' : idPrenotazione, 'stato' : Number($('#customSwitch1').is(':checked'))},
				success : function (d) {
					if (d.data.status == 'success')
					{	
						notifica_success(d.data.msg);
						aggiornaDati (d.data.dictAggiornato)
					}
					
					if (d.data.status == "error")
					{
						notifica_errore(d.data.msg);
					} 
				}
			})
		});

		$('.statoSoggiorno').on('click', function(){
			var bottoni = $('#statoSoggiornoGroup').find('button');
			var idStato = $(this).attr('id');
			var url = '/cambiaStatoSoggiorno';
			$.ajax({
                type: "POST",
                url: url, //CHIAMATA PER ELIMINARE UNA TIPOLOGIA
                data:{'nuovoStato' : idStato, 'idPrenotazione' : idPrenotazione},
                success: function (d) {
                    if (d.data.status == 'success')
					{
						zeroStatus(bottoni)
						switch (idStato)
						{
							case '1' :
								$(bottoni[0]).removeClass("btn-outline-warning")
								$(bottoni[0]).addClass ("btn-warning")
								break;
							
							case '2' :
								$(bottoni[1]).removeClass("btn-outline-success")
								$(bottoni[1]).addClass ("btn-success")
								break;

							case '3' :
								$(bottoni[2]).removeClass("btn-outline-danger")
								$(bottoni[2]).addClass ("btn-danger")
								break;
						}
						notifica_success(d.data.msg)
					}

					if (d.data.status == 'error')
					{
						notifica_errore(d.data.msg)
					}
                }
            });
		});

		$('.statopagamento').on('click', function(){
			var bottoni = $('#statoPagamentoGroup').find('button')
			var idStato = $(this).attr('id');
			var url = '/cambiaStatoPagamento';
			$.ajax({
                type: "POST",
                url: url, //CHIAMATA PER ELIMINARE UNA TIPOLOGIA
                data:{'nuovoStato' : idStato, 'idPrenotazione' : idPrenotazione},
                success: function (d) {
					if (d.data.status == 'success')
					{
						zeroStatusPagamento(bottoni)
						switch (idStato)
						{
							case '1' :
								$(bottoni[0]).removeClass("btn-outline-warning")
								$(bottoni[0]).addClass ("btn-warning")
								break;
							
							case '2' :
								$(bottoni[1]).removeClass("btn-outline-primary")
								$(bottoni[1]).addClass ("btn-primary")
								break;

							case '3' :
								$(bottoni[2]).removeClass("btn-outline-success")
								$(bottoni[2]).addClass ("btn-success")
								break;
						}
						notifica_success(d.data.msg)
						aggiornaDati (d.data.dictAggiornato)
					}

					if (d.data.status == 'error')
					{
						notifica_errore(d.data.msg)
					}
				}
			})
		});

	function zeroStatus (bottoni) {
		
		$(bottoni[0]).removeClass("btn-warning")
		$(bottoni[1]).removeClass("btn-success")
		$(bottoni[2]).removeClass("btn-danger")
		$(bottoni[0]).addClass ("btn-outline-warning")
		$(bottoni[1]).addClass ("btn-outline-success")
		$(bottoni[2]).addClass ("btn-outline-danger")
	
	}

	function zeroStatusPagamento (bottoni) {
		
		$(bottoni[0]).removeClass("btn-warning")
		$(bottoni[1]).removeClass("btn-primary")
		$(bottoni[2]).removeClass("btn-success")
		$(bottoni[0]).addClass ("btn-outline-warning")
		$(bottoni[1]).addClass ("btn-outline-primary")
		$(bottoni[2]).addClass ("btn-outline-success")
	
	}

	function aggiornaDati (newDict) 
	{
		$('#totale').html('TOTALE : ' + newDict ['totale'] +'€')
		$('#daPagare').html('DA PAGARE ' + (parseInt(newDict ['totale']) - parseInt(newDict ['pagato'])) +'€')
		$('#labelTassa').html(newDict ['tassaSoggiorno'] +'€')
		$('#prezzoExtra').html(newDict ['prezzoExtra'] +'€')
		$('#prezzoSupplementi').html(newDict ['prezzoSupplementi'] +'€')
		
	}
}

export {prenotazioneInfo}