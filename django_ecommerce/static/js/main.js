/* Code for button text toggle in JQuery in Portfolio.html */

$(function(){
	// body...
	$("#collapseExample1").click(function(){
		/* Act on the event */
		$('#Example1').collapse({
			toggle: true
		})
	});
});

