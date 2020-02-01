function validateForm() {
    const x = document.forms["myform"]["semail"].value;
    const y = document.forms["myform"]["seligibility"].value;
    if ((x == "" && y == "")||(x && y)) {
      alert("Provide only one feild");
      return false;
    }
  } 