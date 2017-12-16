//Timer

var match_length = 135000;
var start_button_time = match_length;
var change_time;
showTime(start_button_time);

$('#start').on('click', function() {
	NetworkTables.putValue("/SmartDashboard/controls_enabled", true);
	var startTime = Date.now();
	change_time = setInterval(function() {
			showTime(start_button_time);
			if(start_button_time <= 0) {
				NetworkTables.putValue("/SmartDashboard/controls_enabled", false);
				clearInterval(change_time);
			}
			start_button_time -= 100;
		}, 100);
});

$('#stop').on('click', function() {
	NetworkTables.putValue("/SmartDashboard/controls_enabled", false);
	clearInterval(change_time);
});

$('#reset').on('click', function() {
	start_button_time = match_length;
	showTime(start_button_time);
});

function showTime(timeLeft) {	
		console.log(timeLeft)
		var seconds = parseInt((timeLeft / 1000) % 60);
		var minutes = parseInt((timeLeft / 1000) / 60);
		
		// set text for elements
		$('.minutes').text(minutes);
		
		if (seconds < 10) 
			$('.seconds').text("0" + seconds);
		else 
			$('.seconds').text(seconds);
			
}

//Score
var score = 0;

$('.hoop button').on('click', function() {
	var button = $(this);
	var targetClass = button.data('target');
	var targetElement = button.parent().find("." + targetClass);
	var buttonValue = button.data("value");
	var currentTargetValue = parseInt(targetElement.text());
	var nextTargetValue = currentTargetValue + (buttonValue > 0 ? 1 : -1);
	if (currentTargetValue > 0 || buttonValue > 0){
		targetElement.text(nextTargetValue);
		score = (score+button.data("value"));
		$(".score").text(score);
	}
});

$('.penalty button').on('click', function() {
	var button = $(this);
	var targetElement = button.parent().find("span");
	var buttonValue = button.data("value");
	var currentTargetValue = parseInt(targetElement.text());
	var nextTargetValue = currentTargetValue + (buttonValue < 0 ? 1 : -1);
	if (currentTargetValue > 0 || buttonValue < 0){
		targetElement.text(nextTargetValue);
		score = (score+button.data("value"));
		$(".score").text(score);
	}
});
