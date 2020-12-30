let add_student = document.querySelector('#add-field')

add_student.onkeyup = function() {
  if (add_student.value === '') {
    document.querySelector('#add-button').disabled = true;
  } else {
    document.querySelector('#add-button').disabled = false;
  }
}

