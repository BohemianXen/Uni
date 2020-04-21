
//from: https://stackoverflow.com/questions/6506897/csrf-token-missing-or-incorrect-while-post-parameter-via-ajax-in-django
function getCookie(c_name) {
  if (document.cookie.length > 0) {
      c_start = document.cookie.indexOf(c_name + "=");
      if (c_start != -1) {
          c_start = c_start + c_name.length + 1;
          c_end = document.cookie.indexOf(";", c_start);
          if (c_end == -1) c_end = document.cookie.length;
          return unescape(document.cookie.substring(c_start,c_end));
      }
  }
  return "";
}


$("#connectButton").click(function () {
  var currentStatus = $("#statusLabel").html();
  var connect = (currentStatus.includes('Disconnected'))? 'true':'false';

  var csrftoken = (getCookie("csrftoken"));
  $.ajax({
    type: 'POST',
    data: {'connect': connect},
    dataType: 'json',
    headers: {"X-CSRFToken": csrftoken},
    success: function (data) {
      $("#statusLabel").text(data.status);
      $("#actionLabel").text(data.action);
    }
  });
});

(function update() {
  console.log("Update")
  $.ajax({
      type: 'GET',
      data: {doUpdate: 'true'},
      dataType: 'json',
      success: function(data) {
        $("#statusLabel").text(data.status);
        $("#actionLabel").text(data.action);
      }
  }).then(function() {
     setTimeout(update, 1000);
  });
})();


/*$(document).ready(function () {
  var label = status; // $("#statusLabel").html();
  console.log("I Don't Know What I'm Doing")
  console.log(label)
  $.ajax({
     data: {'status': label},
     dataType: 'json',
     success: function (data) { console.log(label)}
   });
});*/
