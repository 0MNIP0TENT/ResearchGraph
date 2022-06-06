function getEntityValue(check){
  // Selecting the input element and get its value 
  var inputVal = document.getElementById("myInput").value;
    
    upperCase = inputVal.toUpperCase() 

    if (check.includes(upperCase)) {
      window.location.replace("/Entitys/"+upperCase);
    }

    else {
      alert('You Entered an invalid input.');
    }

}

function getRelationValue(check){
  // Selecting the input element and get its value 
  var inputVal = document.getElementById("myInput").value;
  upperCase = inputVal.toUpperCase() 
    if (check.includes(upperCase)) {
      window.location.replace("/Relations/"+upperCase);
    }

    else {
      alert('You Entered an invalid input.');
    }

}

function getTypeValue(check){
  // Selecting the input element and get its value 
  var inputVal = document.getElementById("myInput").value;
  upperCase = inputVal.toUpperCase() 
    if (check.includes(upperCase)) {
      window.location.replace("/Types/"+upperCase);
    }

    else {
      alert('You Entered an invalid input.');
    }

}
