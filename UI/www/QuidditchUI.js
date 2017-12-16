
$('#start').on('click', function() {
	//NetworkTables.putValue("/SmartDashboard/controls_enabled", true);
	var startTime = Date.now();
	setInterval(function() {
		showTime(startTime);
	}, 100);
});

$('#stop').on('click', function() {
	//NetworkTables.putValue("/SmartDashboard/controls_enabled", false);
});

function showTime(time) {
		var timeElapsed = Date.now() - time;
		var timeLeft = 135000 - timeElapsed;
		
		var seconds = parseInt((timeLeft / 1000) % 60);
		var minutes = parseInt((timeLeft / 1000) / 60);
		
		// set text for elements
		$('.minutes').text(minutes);
		
		if (seconds < 10) 
			$('.seconds').text("0" + seconds);
		else 
			$('.seconds').text(seconds);
			
}


