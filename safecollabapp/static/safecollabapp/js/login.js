$(document).ready(function() {
  $('#login-form-link').click(function(e) {
    $("#login-form").delay(110).fadeIn(100);
    $("#register-form").fadeOut(100);
    $('#register-form-link').removeClass('active');
    $('#register-message').text('');
    $(this).addClass('active');
    e.preventDefault();
  });

  $('#register-form-link').click(function(e) {
    $("#register-form").delay(110).fadeIn(100);
    $("#login-form").fadeOut(100);
    $('#login-form-link').removeClass('active');
    $('#login-message').text('');
    $(this).addClass('active');
    e.preventDefault();
  });

  $('#register-form').on('submit', function(event) {
    event.preventDefault();
    console.log('form submitted');

    first_name = $('#first-name').val()
    last_name = $('#last-name').val()
    email = $('#email').val()
    username = $('#register-username').val()
    password = $('#register-password').val()
    confirm_password = $('#confirm-password').val()

    data_dict = {
      'first-name': first_name,
      'last-name': last_name,
      'email': email,
      'username': username,
      'password': password,
      'confirm-password': confirm_password
    }

    console.log("First name " + first_name)
    console.log("Last name " + last_name)
    console.log("Email " + email)
    console.log("Username " + username)
    console.log("Password " + password)
    console.log("Confirm " + confirm_password)

    csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
      url: "/register/",
      type: "POST",
      data: data_dict,

      success: function(json) {
        $('#register-message').text(json['register_message']);
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
