function getEntityValue(check){
  // Selecting the input element and get its value 
  var inputVal = document.getElementById("myInput").value;
    
    upperCase = inputVal.toUpperCase(); 

    if (check.includes(upperCase)) {
      window.location.replace("/Entities/UnVerified/"+upperCase);
    }
    else {
      alert('You Entered an invalid input.');
    }
}

function getRelationValue(check){
  // Selecting the input element and get its value 
  var inputVal = document.getElementById("myInput").value;
  upperCase = inputVal.toUpperCase(); 
    if (check.includes(upperCase)) {
      window.location.replace("/Relations/UnVerified/"+upperCase);
    }
    else {
      alert('You Entered an invalid input.');
    }
}

function getTypeValue(translations){
  // Selecting the input element and get its value 
  var inputVal = document.getElementById("myInput").value;
  lowerCase = inputVal.toLowerCase(); 
  if(lowerCase in translations) {
    window.location.replace("/Types/UnVerified/"+translations[lowerCase]);
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
