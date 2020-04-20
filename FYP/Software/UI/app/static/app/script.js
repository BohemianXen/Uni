"use strict";

function connectButtonClicked(status){
  document.getElementById("actionLabel").innerHTML = "Hello World";
}

var connectButton = document.getElementById("connectButton");
connectButton.addEventListener("click", connectButtonClicked);
