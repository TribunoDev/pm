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

	//Script para agregar datos de un nuevo carrito
	$('#frmOrden').submit(function(e){
		e.preventDefault();
		$.ajax({
			type: 	'POST',
			url: 	'/agregar-carrito/',
			data: 	{ 
				'Cantidad': $('input[name=Cantidad]').val(),
				'Producto': $('input[name=Producto').val(),
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
			},
			success: function(data){
				$('#mensaje-carrito').slideDown("slow");
				$('.mensaje').html(data);
				datos_carrito();
				item_carrito();
			},
			dataType: 'html'
		});
	});

	//Script para el boton de editar item
	$('.item-cantidad').on('click', '.btnItem-Editar', function(e){
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

	//Script para actualizar la cantidad de cada producto
	$('.item-cantidad').on('click', '.btnItem-Actualizar', function(e){
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
	$('.item-carrito').on('click', '.btnItem-Eliminar', function(e){
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
	$('.item-carrito').on('keyup', 'input[name=Cantidad]', function(){
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

});