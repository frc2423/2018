
$('#start').on('click', function() {
	NetworkTables.putValue("/SmartDashboard/controls_enabled", true);
});

$('#stop').on('click', function() {
	NetworkTables.putValue("/SmartDashboard/controls_enabled", false);
});