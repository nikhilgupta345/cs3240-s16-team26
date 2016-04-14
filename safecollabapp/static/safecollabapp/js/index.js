$(document).ready(function() {

  /* Add a new group */
  $('#create_group_button').click(function(event) {
    event.preventDefault();
    name = $('#group_name').val()

    data_dict = {
      'group_name': name
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
      url: "/create_group/",
      type: "POST",
      data: data_dict,

      success: function(json) {
        if(json['response'] != '') {
          $('#create_group_response').text(json['response']);
        } else {
          $('#create_group_cancel').click()
          new_row = '<tr> <td>' + name + '</td>';
          new_row += '<td>1</td>';
          new_row += '<td>';
          new_row += '<select class="select_userbox" style="width:100%">';
          
          usernames = json['usernames'];

          for(var i = 0; i < usernames.length ; i++) {
            new_row += '<option value="' + usernames[i] + '">' + usernames[i] + '</option>'
          }

          console.log(json['usernames'])

          new_row += '</select>';
          new_row += '</td></tr>'
          $('#groups_table').append(new_row)

          $('.select_userbox').select2({
            placeholder: "Select a User",
            allowClear: false
          });

          $('#group_name').val('');

        }
      },

      error: function(xhr, errmsg, err) {
        console.log('error');
      }
    })
  })

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
        if(json['response'] != 'Could not find a user with that username') {
            $('#manager-list ul').append('<li>' + username + '</li>');
        }
        
        $('#addmanager-response').text(json['response']);

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
