$(document).on("ready", function(){

	Ofertas();
	LlenarCatalogo();

	if (screen.width < 641) {
		$("#etiquetas ul").removeClass("nav-tabs");
		$("#etiquetas ul").addClass("nav-pills");
		$("#etiquetas").css("border-top", "1px solid #bdc3c7");
		$("#etiquetas").css("border-bottom", "1px solid #bdc3c7");
		$("#contenido-producto li").css("margin-left", "120px");
	};

	$("#menu a").on("click", function(){
		$("#menu li").each(function(){
			$("#menu li").removeClass("active");
		});

		$(this).closest("li").addClass("active");
	});

	$("#myTab a").on("click", function(e){
		e.preventDefault();
		$("#myTab li").each(function(){
			$("#myTab li").removeClass("active");
		});

		$(this).closest("li").addClass("active");
	});

	//Script para la opción "Destacados" en el menu intermedio de la página de Inicio
	$("#destacados").on("click", function(){
		Destacados();
	});

	//Script para la opción "Oferta" en el menu intermedio de la página de Inicio
	$("#ofertas").on("click", function(){
		Ofertas();
	});

	$("#novedades").on("click", function(){
		Novedades();
	});

	function Destacados(){
		$.get("/productos-destacados/", function(data){
			$("#resultado-productos").html(data);
		}, "html");
		
	};

	function Ofertas(){
		$.get("/productos-en-oferta/", function(data){
			$("#resultado-productos").html(data);
		}, "html")
	};

	function Novedades(){
		$.get("/productos-en-novedades/", function(data){
			$("#resultado-productos").html(data);
		}, "html")
	};

	//Script para llenar la catalogo "Producto" en el menu principal.
	function LlenarCatalogo(){
		$.get("/catalogo-productos/", function(data){
			$('#categorias-productos').html(data);
		}, "html");
	};

	//Script que genera contenido en ventana modal
	$('#resultado-productos, #todas-marcas').on('click', '.btn-detalle', function(){
		$.ajax({
			type:'POST',
			url:'/detalle-producto/',
			data: {
				'parametro':$(this).attr('data'),
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
			},
			success: function(data){
				$('#modal-ventana').html(data);
			},
			dataType: 'html',
		});
	});

	//Script para evaluar si las contraseñas coinsiden
	$('#btnRegistrar').on('click', function(e){
		password1 = $('#id_password').val();
		password2 = $('#repetir_password').val();

		if (password1 != password2) {
			e.preventDefault();
			$('#repetir_password').addClass('alert-danger');
		};
	});

	$('#repetir_password').on('focus', function(){
		$('#repetir_password').removeClass('alert-danger');
	});
	
	//Script para los datos del carrito
	function datos_carrito () {
		$.ajax({
			type: 	'GET',
			url: 	'/datos-carrito/',
			data: 	{},
			success: function(data){
				$('.total-item-carrito').html(data);
			},
			dataType: 	'html'
		});
	};

	datos_carrito();

	//Script que retorna los item del carrito a la pestaña del menu
	function item_carrito () {
		$.ajax({
			type: 	'GET',
			url: 	'/item-carrito/',
			data: 	{},
			success: function(data){
				$('.nav #total-item').html(data.cantidad);
			},
			dataType: 'JsON'
		});
	};

	item_carrito();

	//Script para el boton de editar item
	$('.items-carrito').on('click', '.btnItem-Editar', function(e){
		var idDetalle = $(this).attr('data-id');
		var frmCantidad = $(this).closest('.item-cantidad').attr('data-id');
		e.preventDefault();
		$.ajax({
			type: 	'POST',
			url: 	'/form-editar-cantidad/',
			data: 	{
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
				'idDetalle':idDetalle
			},
			success: function(data){
				$('div[data-id='+ frmCantidad + '] div').html(data);
			},
			dataType: 'html'
		});

	});

	//Script para obtener datos de un carrito
	$.ajax({
		type: 	'GET',
		url: 	'/obtener-datos-carrito/',
		data: 	{},
		success: function(data){
			$('.items-en-carrito').html(data);
		},
		dataType: 'html'
	});

	//Script para actualizar la cantidad de cada producto
	$('.items-carrito, #item-carrito').on('click', '.btnItem-Actualizar', function(e){
		e.preventDefault();
		var form = $(this).closest('form').attr('id');
		var frmCantidad = $(this).closest('.item-cantidad').attr('data-id');

		$.ajax({
			type: 	'POST',
			url: 	'/actualizar-cantidad/',
			data: 	{
				'Cantidad': $('form[id=' + form + '] input[name=Cantidad]').val(),
				'Producto': $('form[id=' + form + '] input[name=Producto]').val(),
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
			},
			success: function(data){
				$('div[data-id='+ frmCantidad + '] div').html(data);
				datos_carrito();
				item_carrito();
			},
			dataType: 'html'

		});
	});

	//Script para el boton de eliminar item
	$('.items-carrito').on('click', '.btnItem-Eliminar', function(e){
		e.preventDefault();
		var idDetalle = $(this).attr('data-id');
		$(this).closest('.item-carrito').slideUp('slow');

		$.ajax({
			type: 	'POST',
			url: 	'/eliminar-item/',
			data: 	{
				'idDetalle':idDetalle, 
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
			},
			success: function(data){
				datos_carrito();
				item_carrito();
			},
			dataType: 'json'
		});

	});

	//Script para evaluar si el valor del input es cero
	$('.items-carrito').on('keyup', 'input[name=Cantidad]', function(){
		input_val = $(this).val();
		form = $(this).closest('form').attr('id');

		if (input_val == 0) {
			$('.item-carrito form[id=' + form + '] a').text('Eliminar');
			$('.item-carrito form[id=' + form + '] a').removeClass('btnItem-Actualizar');
			$('.item-carrito form[id=' + form + '] a').addClass('btnItem-Eliminar');
		} else{
			$('.item-carrito form[id=' + form + '] a').text('Actualizar');
			$('.item-carrito form[id=' + form + '] a').addClass('btnItem-Actualizar');
			$('.item-carrito form[id=' + form + '] a').removeClass('btnItem-Eliminar');
		};
	});

	//Script para obtener la informacion del usuario
	$.ajax({
		type: 	'GET',
		url: 	'/obtener-info-usuario/',
		data: 	{},
		success: function(data){
			$('.info-usuario .panel').html(data);
		},
		dataType: 'html'
	});

	//Script para agregar elementos css a controles de inicio de sesión
	$('#frmRegUsuario label, #formularioEmail label').addClass('control-label');
	$('#id_username').addClass('form-control input-lg');
	$('#id_password').addClass('form-control input-lg');
	$('#id_amigo, #id_correo, #id_mensaje, #id_email').addClass('form-control');

	$('#panel-direccion input, #panel-direccion select, #panel-direccion textarea').addClass('form-control');

	//Active para imagenes miniatura en detalle
	$('#no-template-pager img').on('click', function(){
		$('#no-template-pager img').removeClass('active_img');
		$(this).addClass('active_img');
	});

	$('.s2').cycle({
		fx: 'fade'
	});


	//Script para capturar el url de la pagina actual
	var home = 'http://127.0.0.1:8000/';
	var href = $(location).attr('href');
	if (home == href) {
		$('#myCarousel').css('display', 'block');
	};

	var marcas = home + 'marcas/';
	var ingresar = home + 'ingresar/';
	var registrar = home + 'registro/';
	var rec_contrasena = home + 'recuperar-contrasena/';
	if (href == marcas || href == ingresar || href == registrar || href == rec_contrasena) {
		$('#list_carousel').css('display', 'none');
	};

	$('#carouMarcas').carouFredSel({
		items: {
			width: 200,
		//	height: '30%',	//	optionally resize item-height
			visible: {
				min: 2,
				max: 6
			}
		},
		prev: '#prev2',
		next: '#next2',

		mousewheel: true,
		responsive: true,
		scroll: 2,
		swipe: {
			onMouse: true,
			onTouch: true
		},
		width: '100%',
	});

	//Script para el boton imprimir
	$('#frmDireccion input, #frmDireccion select, #frmDireccion textarea').attr('required', 'True');

	//Script para validar el usuario a registrar
	$('#username').on('blur', function(){
		username=$('#username').val();
		$.ajax({
			type: 	'POST',
			url: 	'/verificar-usuario/',
			data: 	{
				'usuario':username,
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
			},
			success: function(data){
				if (data.tUser==1) {
					$('#verificaUser').text("El nombre de usuario '" +username+ "' ya existe");
					$('#username').val("");
				}else{
					$('#verificaUser').text("");
				};
			},
			dataType: 'json'
		});
	});

	//Script para verificar email a registrar
	$('#email').on('blur', function(){
		email=$('#email').val();
		$.ajax({
			type: 	'POST',
			url: 	'/verificar-email/',
			data: 	{
				'email':email,
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
			},
			success: function(data){
				if (data.tUser==1) {
					$('#verificarEmail').text("El e-mail '" +email+ "' ya está registrado");
					$('#email').val("");
				}else{
					$('#verificarEmail').text("");
				};
			},
			dataType: 'json'
		});
	});

	//Script para verificar email al reponer contrasena
	$('#recEmail').on('blur', function(){
		email=$('#recEmail').val();
		$.ajax({
			type: 	'POST',
			url: 	'/verificar-email/',
			data: 	{
				'email':email,
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
			},
			success: function(data){
				if (data.tUser==0) {
					$('#verificarEmail').text("El e-mail '" +email+ "' ya está registrado");
					$('#email').val("");
				}else{
					$('#verificarEmail').text("");
				};
			},
			dataType: 'json'
		});
	});

	//Script para verificar RNP ya registrado
	$('#RNP').on('blur', function(){
		RNP=$('#RNP').val();
		$.ajax({
			type: 	'POST',
			url: 	'/verificar-rnp/',
			data: 	{
				'rnp':RNP,
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
			},
			success: function(data){
				if (data.tUser==1) {
					$('#verificaRNP').text("El RNP '" +RNP+ "' ya está registrado");
					$('#RNP').val("");
				}else{
					$('#verificaRNP').text("");
				};
			},
			dataType: 'json'
		});
	});


	//Script para cargar la url para compartir por email
	$('#id_url').val(href);
	$('#id_amigo').attr('required', 'required');
	$('#id_correo').attr('required', 'required');
	$('#id_mensaje').attr('required', 'required')

	$('#myModalRecomendacion #id_url').val("www.pm.hn");


	//Script para cargar combo Región desde el combo País
	$('#id_Region').attr('disabled', 'disabled');
	$('#id_Ciudad').attr('disabled', 'disabled');
	$('#id_Pais').on('click', function(){
		if ($(this).val()=="") {
			$('#id_Region, #id_Ciudad').val("");
			$('#id_Region').attr('disabled', 'disabled');
			$('#id_Ciudad').attr('disabled', 'disabled');
		}else{
			$('#id_Region').removeAttr('disabled');
		};
	});

	$('#id_Pais').change(function(){
		$.ajax({
			type: 	'POST',
			url: 	'/cargar-region/',
			data: 	{
				'pais':$(this).val(),
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
			},
			success: function(data){
				$('#id_Region').html(data);
			},
			dataType: 'html'
		});
	});

	//Script para cargar el combo Ciudad
	$('#id_Region').on('click', function(){
		if ($(this).val()=="") {
			$('#id_Ciudad').val("");
			$('#id_Ciudad').attr('disabled', 'disabled');
		}else{
			$('#id_Ciudad').removeAttr('disabled');
		};
	});
	$('#id_Region').change(function(){
		$.ajax({
			type: 	'POST',
			url: 	'/cargar-ciudad/',
			data: 	{
				'region':$(this).val(),
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
			},
			success: function(data){
				$('#id_Ciudad').html(data);
			},
			dataType: 'html'
		});
	});


	//Script para cargar imagenes a un producto
	/*$('#agregar_campo').on('click', function(){
		var contar_campos = $('input[type="file"]').length;
		var siguiente_campo = contar_campos + 1;
		$('#carga_archivo').prepend('<div class="form-group"><label for="exampleInputFile">Imágen</label><input type="file" id="image" name="imagen_'+ siguiente_campo +'" /></div>');

	});*/
	
	

});
