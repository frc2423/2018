$("input[name='position']").change( function() {
	NetworkTables.putValue("/autonomous/DriveNDrop/robot_position", $("input[name='position']:checked").val())
});

$("input[name='left_switch']").change( function() {
	NetworkTables.putValue("/autonomous/DriveNDrop/action_if_left_switch", $("input[name='left_switch']:checked").val())
});

$("input[name='right_switch']").change( function() {
	NetworkTables.putValue("/autonomous/DriveNDrop/action_if right_switch", $("input[name='right_switch']:checked").val())
});

// create a wrapper around native canvas element (with id="c")
var canvas = new fabric.Canvas('c');

// create a rectangle object
var rect = new fabric.Rect({
left: 100,
top: 100,
fill: 'red',
width: 20,
height: 20
});

// "add" rectangle onto canvas
canvas.add(rect);