var socket = io();

socket.on('connect', function() {
	
});
socket.on('disconnect', function() {
	
});
socket.on('data', function(data) {
	socket_data_cb(data);
});

function toggleSection(sectionId, trigger) {
	var section = document.getElementById(sectionId);
	var arrow = trigger.querySelector('span');
	if (section.classList.contains('hide')) {
		section.classList.remove('hide');
		arrow.classList.remove('arrow-down');
		arrow.classList.add('arrow-up');
	} else {
		section.classList.add('hide');
		arrow.classList.remove('arrow-up');
		arrow.classList.add('arrow-down');
	}
}

function socket_data_cb(data) {
   switch(data.type) {
		case 'latestviolation': {
			update_latest_violation(data.payload);
			break;
		}
		case 'addnewviolation': {
			break;	
		}
		default: {
			break;
		}
	}
}

function load_new_vp() {
	socket.emit('requestdata', {data : {'type': 'latestviolation'}});
}

function themvipham() {
	var payload = {
		"lop" : document.getElementById("lop"),
		"ten_hs" : document.getElementById("ten_hs"),
		"ma_nq" : document.getElementById("ma_nq")
	}
	socket.emit('requestdata', {data : {'type' : 'addnewviolation', 'payload' : payload}});
}

$( document ).ready(function() {
    console.log( "ready!" );
});
