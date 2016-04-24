$(document).ready(function() {

  /* Add user to a group */
  $('tbody').on('click', '.add_user_to_group_button', function(event) {
    event.preventDefault();
    id = event.target.id;

    // ID is of form add_button_{{ group.name }}, so we need to get group name
    group_name = id.substring(11);
    username = $('#select_' + group_name).val();
    console.log(username);
    console.log(group_name);

    data_dict = {
      'group_name': group_name,
      'username':username
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
      url: "/add_user_to_group/",
      type: "POST",
      data: data_dict,

      success: function(json) {
        if(json['response'] != '') { // User unsuccessfully added to groupo
          $.notify(json['response'], "error");
        } else {
          $.notify('User successfully added!', "success");
          var td_num_users = $('#td_num_users_' + group_name)[0];
          var cur_users = parseInt(td_num_users.innerHTML);
          td_num_users.innerHTML = cur_users + 1 // Change num_users in the table by 1
        }
      },

      error: function(xhr, errmsg, err) {
        $.notify('Error adding this user.', "error");
        console.log('error');
      }
    })
  })

   /* Add a new group */
  $('#sitemanager_create_group_button').click(function(event) {
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
      url: "/sitemanager_create_group/",
      type: "POST",
      data: data_dict,

      success: function(json) {
        if(json['response'] != '') {
          $('#sitemanager_create_group_response').text(json['response']);
        } else {
          $('#sitemanager_create_group_cancel').click()
          new_row = '<tr> <td>' + name + '</td>';
          new_row += '<td class="td_num_users" id="td_num_users_' + name + '">1</td>';
          new_row += '<td>';
          new_row += '<select class="select_userbox" style="width:100%" id="select_' + name + '">';
          
          console.log(json);
          usernames = json['usernames'];

          new_row += '<option />';
          for(var i = 0; i < usernames.length ; i++) {
            new_row += '<option value="' + usernames[i] + '">' + usernames[i] + '</option>'
          }

          console.log(json['usernames'])

          new_row += '</select>';
          new_row += '</td><td><button type="submit" class="btn btn-primary add_user_to_group_button" id="add_button_' + name + '">' + 'Add User</button></td>'
          new_row += '</tr>'
          $('#groups_table').append(new_row)

          $('.select_userbox').select2({
            placeholder: "Select a User",
            allowClear: false
          });

          $('#group_name').val('');
          $('#sitemanager_create_group_response').text('');
        }
      },

      error: function(xhr, errmsg, err) {
        console.log('error');
      }
    })
  })

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
          new_row += '<td class="td_num_users" id="td_num_users_' + name + '">1</td>';
          new_row += '<td>';
          new_row += '<select class="select_userbox" style="width:100%" id="select_' + name + '">';
          
          console.log(json);
          usernames = json['usernames'];

          new_row += '<option />';
          for(var i = 0; i < usernames.length ; i++) {
            new_row += '<option value="' + usernames[i] + '">' + usernames[i] + '</option>'
          }

          console.log(json['usernames'])

          new_row += '</select>';
          new_row += '</td><td><button type="submit" class="btn btn-primary add_user_to_group_button" id="add_button_' + name + '">' + 'Add User</button></td>'
          new_row += '</tr>'
          $('#groups_table').append(new_row)

          $('.select_userbox').select2({
            placeholder: "Select a User",
            allowClear: false
          });

          $('#group_name').val('');
          $('#create_group_response').text('');
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

  /* view a report */
  $('form.view-report-form').on('submit', function(event) {
    event.preventDefault();

    var form = $(event.target);
    reportName = form.find('#report_name').val();

    data_dict = {
      'short_desc' : reportName,
    };

    csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({
      url: "/view_report/",
      type: "POST",
      data: data_dict,

      success: function(json) {
        $('#viewreport-response').html(
            '<h3>' + json['short_desc'] + '</h3>' +
            '<h4>' + json['time'] + '</h4>' +
            '<p>' + json['long_desc'] + '</p>' +
            '<p>' + json['file_name'] + '</p>'
            );
      },

      error: function(xhr, errmsg, err) {
        console.log('error');
      }
    })
  });

  /* view a report */
  $('form.sitemanager-view-report-form').on('submit', function(event) {
    event.preventDefault();

    var form = $(event.target);
    reportName = form.find('#report_name').val();

    data_dict = {
      'short_desc' : reportName,
    };

    csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({
      url: "/view_report/",
      type: "POST",
      data: data_dict,

      success: function(json) {
        $('#sitemanager-viewreport-response').html(
            '<h3>' + json['short_desc'] + '</h3>' +
            '<h4>' + json['time'] + '</h4>' +
            '<p>' + json['long_desc'] + '</p>'
            );
      },

      error: function(xhr, errmsg, err) {
        console.log('error');
      }
    })
  });

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

  $("#group_name").keyup(function(event){
    if(event.keyCode == 13){
      $("#create_group_button").click();
    }
  });
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
