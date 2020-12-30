let add_student = document.querySelector('#add-field');

add_student.onkeyup = function() {
  if (add_student.value === '') {
    document.querySelector('#add-button').disabled = true;
  } else {
    document.querySelector('#add-button').disabled = false;
  }
}


document.querySelector('#search-student').onchange = function (){
  if (document.querySelector('#search-student').value === ''){
    document.querySelector('#upd-button').disabled = true;
    document.querySelector('#rem-button').disabled = true; 
  } else {
    document.querySelector('#upd-button').disabled = false;
    document.querySelector('#rem-button').disabled = false;
  }
}

