$(document).ready(function() {
  $('#recover-form').on('submit', function(event) {
    event.preventDefault();
    console.log('form submitted');

    username = $('#username').val()
    email = $('#email').val()

    data_dict = {
      'email': email,
      'username': username,
    }


    console.log("Email " + email)
    console.log("Username " + username)

    /*csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
      url: "/recover_password/",
      type: "POST",
      data: data_dict,

      success: function(json) {
        console.log('success');
        console.log(json);

        $('#recover-message').text(json['recover_message']);
        if(json['response'] == 'redirect_index') {
          location.href = '/index/';
        } else if(json['response'] == 'redirect_login') {
          location.href = '/login/';
        }
      },

      error: function(xhr, errmsg, err) {
        console.log('error')
      }
    })
  })*/
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
