let add_field = document.querySelector('#add-field')

add_field.onkeyup = function(){
	if (add_field.value === ''){
		document.querySelector('#add-button').disabled = true;
	} else {
		document.querySelector('#add-button').disabled = false;
	}
}

let rem_field = document.querySelector('#rem-field')
rem_field.onchange = function(){
	if (rem_field.value === ''){
		document.querySelector('#rem-button').disabled = true;
	} else {
		document.querySelector('#rem-button').disabled = false;
	}
}
