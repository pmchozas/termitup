$('.menu__title a').on('click', myFunction);

function myFunction(e) {
	e.preventDefault();

	if($(this).next().hasClass('responsive') ) {
		$('.menu__list').removeClass('responsive');
	}else{
		$('.menu__list').removeClass('responsive');
		$(this).next().addClass('responsive');
	}
	
}


