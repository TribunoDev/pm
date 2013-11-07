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





	
});