
$('#start').on('click', function() {
	NetworkTables.putValue("/SmartDashboard/controls_enabled", true);
});

$('#stop').on('click', function() {
	NetworkTables.putValue("/SmartDashboard/controls_enabled", false);
});

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