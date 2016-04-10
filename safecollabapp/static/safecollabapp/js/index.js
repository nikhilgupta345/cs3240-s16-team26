$(document).ready(function() {

  $('#form-addmanager').on('submit', function(event) {
    event.preventDefault();

    username = $('#username').val()

    data_dict = {
      'username': username
    }

    csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
      url: "/add_manager/",
      type: "POST",
      data: data_dict,

      success: function(json) {
        $('#addmanager-response').text(json['response']);
        $('#manager-list').append('<li>' + username + '</li>');
      },

      error: function(xhr, errmsg, err) {
        console.log('error');
      }
    })
  })
})


function getCookie(name) {
  var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
