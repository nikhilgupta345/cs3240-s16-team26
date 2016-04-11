$(document).ready(function() {

  /* Add a Site Manager */
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

  /* Suspend a User Account */
  $('a.link-suspend').click(function() {
    console.log($(this).attr('id'))

    data_dict = {
      'username': $(this).attr('id')
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
      url: "/suspend_user/",
      type: "POST",
      data: data_dict,

      success: function(json) {
        $('#manageusers-response').text(json['response']); // Username
      },

      error: function(xhr, errmsg, err) {
        console.log('error');
      }
    })
    return false;
  })

  /* Restore a User Account */
  $('a.link-restore').click(function() {
    data_dict = {
      'username': $(this).attr('id') // Get the username
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
      url: "/restore_user/",
      type: "POST",
      data: data_dict,

      success: function(json) {
        $('#manageusers-response').text(json['response']);
      },

      error: function(xhr, errmsg, err) {
        console.log('error');
      }
    })
    return false;
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
