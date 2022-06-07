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
var input = document.getElementById("myInput");
// Execute a function when the user presses a key on the keyboard
input.addEventListener("keypress", function(event) {
  // If the user presses the "Enter" key on the keyboard
  if (event.key === "Enter") {
    // Cancel the default action, if needed
    event.preventDefault();
   //  Trigger the button element with a click
    document.getElementById("myBtn").click();
  }
});
