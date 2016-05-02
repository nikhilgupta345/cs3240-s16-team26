$(document).ready(function() {

  $('#search-form').on('submit', function(event) {
      event.preventDefault();

      csrftoken = getCookie('csrftoken');
      $.ajaxSetup({
          beforeSend: function (xhr, settings) {
              if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                  xhr.setRequestHeader("X-CSRFToken", csrftoken);
              }
          }
      });

      $.ajax({
          url: "/search_reports/",
          type: "POST",
          data: {},

          success: function (json) {

              results = json['search_results'];
              table_rows = '';
              for( var i = 0; i < results.size(); i++) {
                  table_rows += '<tr>';
                  table_rows += '<td>' + results[i][0] + '</td>';
                  table_rows += '<td>' + results[i][1] + '</td>';
                  table_rows += '<td>' + results[i][2] + '</td>';
                  table_rows += '</tr>';
              }

              $('#view-search-results').html(
                  table_rows
              );
          },

          error: function (xhr, errmsg, err) {
              console.log('Error displaying search results');
          }

      });
  });

  /* Remove user from a group using SM */
  $('tbody').on('click', '.sm_remove_user_from_group_button', function(event) {
    event.preventDefault();
    id = event.target.id;

    // ID is of form add_button_{{ group.name }}, so we need to get group name
    group_name = id.substring(17);
    username = $('#sm_select_' + group_name).val();
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
      url: "/remove_user_from_group/",
      type: "POST",
      data: data_dict,

      success: function(json) {
        if(json['response'] != '') { // User unsuccessfully added to groupo
          $.notify(json['response'], "error");
        } else {
          $.notify('User successfully removed!', "success");
          var sm_td_num_users = $('#sm_td_num_users_' + group_name)[0];
          var cur_users = parseInt(sm_td_num_users.innerHTML);
          sm_td_num_users.innerHTML = cur_users - 1 // Change num_users in the table by 1
        }
      },

      error: function(xhr, errmsg, err) {
        $.notify('Error removing this user.', "error");
        console.log('error');
      }
    })
  })

  /* Add user to a group using SM */
  $('tbody').on('click', '.sm_add_user_to_group_button', function(event) {
    event.preventDefault();
    id = event.target.id;

    // ID is of form add_button_{{ group.name }}, so we need to get group name
    group_name = id.substring(14);
    username = $('#sm_select_' + group_name).val();
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
          var sm_td_num_users = $('#sm_td_num_users_' + group_name)[0];
          var cur_users = parseInt(sm_td_num_users.innerHTML);
          sm_td_num_users.innerHTML = cur_users + 1 // Change num_users in the table by 1
        }
      },

      error: function(xhr, errmsg, err) {
        $.notify('Error adding this user.', "error");
        console.log('error');
      }
    })
  })

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
  $('#sm_create_group_button').click(function(event) {
    event.preventDefault();
    name = $('#sm_group_name').val()

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
      url: "/sm_create_group/",
      type: "POST",
      data: data_dict,

      success: function(json) {
        if(json['response'] != '') {
          $('#sm_create_group_response').text(json['response']);
        } else {
          $('#sm_create_group_cancel').click()
          new_row = '<tr> <td>' + name + '</td>';
          new_row += '<td class="td_num_users" id="sm_td_num_users_' + name + '">0</td>';
          new_row += '<td>';
          new_row += '<select class="select_userbox" style="width:100%" id="sm_select_' + name + '">';
          
          console.log(json);
          usernames = json['usernames'];

          new_row += '<option />';
          for(var i = 0; i < usernames.length ; i++) {
            new_row += '<option value="' + usernames[i] + '">' + usernames[i] + '</option>'
          }

          console.log(json['usernames'])

          new_row += '</select>';
          new_row += '</td><td><button type="submit" class="btn btn-primary sm_add_user_to_group_button" id="sm_add_button_' + name + '">' + 'Add </button><'
          new_row += '<button type="submit" class="btn btn-danger sm_remove_user_from_group_button" id="sm_remove_button_' + name + '">' + 'Remove</button></td>'
          new_row += '</tr>'
          $('#sm_groups_table').append(new_row)

          $('.select_userbox').select2({
            placeholder: "Select a User",
            allowClear: false
          });

          $('#sm_group_name').val('');
          $('#sm_create_group_response').text('');
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

          // Add the new group to the option for creating a report
          $('#group').append('<option value="' + name + '">' + name + '</option>');
        }
      },

      error: function(xhr, errmsg, err) {
        console.log('error');
      }
    })
  })

  var getMessages = function(recipient) {
    var data_dict = {
      'recipient': recipient
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
      url: "/get_messages/",
      type: "POST",
      data: data_dict,

      success: function(json) {
        var messages = json['messages']
        if(messages.length == 0) {
          $('#message-viewport').html('<p><em>No messages found.</em></p>');
        } else {
          $('#message-viewport').html('<div class="list-group">');
          for(var i in messages) {
            var message = messages[i];
            $('#message-viewport').append(
                '<li class="list-group-item"><h4 class="list-group-item-heading">From ' + message['sender'] + ' at ' + message['time'] + ':</h4>' +
                '<p class="list-group-item-text">' + message['text'] + '</p></li>'
                );
          }
          $('#message-viewport').append('</div>');
        }
      },

      error: function(xhr, errmsg, err) {
        console.log('error');
      }
    })
  };

  $('#message-recipient').change(function() {
    var recipient = $('#message-recipient').val();

    $('#send-message-form-container').html(
       '<form id="send-message-form" action="/send_message/" method="post" role="form">' +
       '<div class="form-group">' +
       '<div class="row"><input type="hidden" id="recipient" name="recipient" value="' + recipient + '"/>' +
       '<div class="col-sm-12"><textarea rows="8" id="message" name="message" style="resize:none;" class="form-control"></textarea></div></div>' +
       '<div class="row"><div class="col-sm-12"><input type="submit" value="Send" class="form-control btn btn-primary" />' +
       '</div></div></div></form>'
        );

    $('#send-message-form').on('submit', function(event) {
      event.preventDefault();
      var form = $(event.target);
      var recipient = form.find('#recipient').val();
      var messageText = form.find('#message').val();
      var data_dict = {
        'recipient' : recipient,
        'message' : messageText,
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
        url: "/send_message/",
        type: "POST",
        data: data_dict,

        success: function(json) {
          getMessages(recipient);
        },

        error: function(xhr, errmsg, err) {
          console.log('error');
        }
      })
    });

    getMessages(recipient);
  });

  /* Add a Site Manager */
  $('#form-addmanager').on('submit', function(event) {
    event.preventDefault();

    username = $('#add_manager_username').val()

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
        if(json['response'].indexOf('Successful') > -1) {
            $('#manager-list ul').append('<li>' + username + '</li>');
        }
        
        $('#addmanager-response').text(json['response']);
        $('#add_manager-username').text('');

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

  $('form.create-folder-form').on('submit', function(event) {
    event.preventDefault();

    csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({
      url: "/create_folder/",
      type: "POST",
      data: {},

      success: function(json) {
        $('#viewreport-response').html(
            '<h4>Create a Folder</h4>' +
            '<form action="" class="submit-folder-form" method="POST">' +
            '<div class="form-group">' +
            '<p><input type="text" name="folder_name" maxlength="128" id="folder_name" class="form-control" /></p>' +
            '<p><input type="submit" class="btn btn-primary" value="Create Folder" /></p>' +
            '</div></form>'
            );

        $('form.submit-folder-form').on('submit', function(event) {
          event.preventDefault();
          var form = $(event.target);
          var folder_name = form.find('#folder_name').val();

          csrftoken = getCookie('csrftoken');
          $.ajaxSetup({
              beforeSend: function(xhr, settings) {
                  if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                      xhr.setRequestHeader("X-CSRFToken", csrftoken);
                  }
              }
          });

          var folder_dict = {
            'folder_name' : folder_name,
          };

          $.ajax({
            url: "/submit_folder/",
            type: "POST",
            data: folder_dict,

            success: function(json) {
              window.location.href="/index/";
            },

            error: function(xhr, errmsg, err) {
              console.log('error');
            }
          });
          
        });
      },

      error: function(xhr, errmsg, err) {
        console.log('error');
      }
    });
  });

  var closeFolder = function() {
    $('form.close-folder-form').on('submit', function(event) {
      event.preventDefault();

      var form = $(event.target);
      var folder_name = form.find('#folder_name').val();

      var data_dict = {
        'folder_name' : folder_name,
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
        url: "/close_folder/",
        type: "POST",
        data: data_dict,

        success: function(json) {
          var folder_div = form.parent();

          folder_div.html(
              '<form action="/open_folder/" class="open-folder-form" method="POST">' +
              '<button type="submit" class="list-group-item" name="folder_name" id="folder_name" value="' + folder_name + '">' +
              '<span id="folder-glyph" class="glyphicon glyphicon-folder-close"></span> ' + folder_name +
              '</button></form>'
              );

          openFolder();
        },

        error: function(xhr, errmsg, err) {
          console.log('error');
        },
      });
    });
  };
  closeFolder();

  var openFolder = function() {
    $('form.open-folder-form').on('submit', function(event) {
      event.preventDefault();

      var form = $(event.target);
      var folder_name = form.find('#folder_name').val();

      var data_dict = {
        'folder_name' : folder_name,
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
        url: "/open_folder/",
        type: "POST",
        data: data_dict,

        success: function(json) {
          var folder_div = form.parent();

          folder_div.html(
              '<form action="/close_folder/" class="close-folder-form" method="POST">' +
              '<button type="submit" class="list-group-item" name="folder_name" id="folder_name" value="' + folder_name + '">' +
              '<span id="folder-glyph" class="glyphicon glyphicon-folder-open"></span> ' + folder_name +
              '</button></form>'
              );

          $('#viewreport-response').html(
              '<h3>' + folder_name + '</h3>' +
              '<p><form action="" class="begin-edit-folder-form" method="POST">' +
              '<input type="hidden" name="folder_name" value="' + folder_name + '" />' +
              '<input type="submit" value="Edit folder" class="btn btn-primary" /></form></p>' +
              '<p><form action="/delete_folder/" class="delete-folder-form" method="POST">' +
              '<input type="hidden" name="folder_name" value="' + folder_name + '" />' +
              '<input type="submit" value="Delete folder" class="btn btn-danger" /></form></p>'
              );

          $('form.delete-folder-form').on('submit', function(event) {
            event.preventDefault();
            csrftoken = getCookie('csrftoken');
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            var delete_dict = {
              'folder_name' : folder_name,
            };

            $.ajax({
              url: "/delete_folder/",
              type: "POST",
              data: delete_dict,

              success: function(json) {
                window.location.href="/index/";
              },

              error: function(xhr, errmsg, err) {
                console.log('error');
              }
            });
            
          });

          $('form.begin-edit-folder-form').on('submit', function(event) {
              event.preventDefault();
              $('#viewreport-response').html(
                '<div class="form-group">' +
                '<form action="/edit_folder/" class="edit-folder-form" method="POST">' +
                '<input type="text" id="folder_name" name="folder_name" class="form-control" value="' + folder_name + '" />' +
                '<input type="submit" value="Save Changes" class="form-control btn btn-primary" />' +
                '</form></div>'
                  );

              $('form.edit-folder-form').on('submit', function(event) {
                event.preventDefault();
                var form = $(event.target);
                new_name = form.find('#folder_name').val();

                var edit_dict = {
                  'original_name' : folder_name, // we get this for free via closure
                  'new_name' : new_name,
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
                  url: "/edit_folder/",
                  type: "POST",
                  data: edit_dict,

                  success: function(json) {
                    window.location.href="/index/";
                  },

                  error: function(xhr, errmsg, err) {
                    console.log('error');
                  }
                });
                
              });
          });
          closeFolder();

          // For each report returned in the json object, append a new form object
          var reports = json['reports'];
          for(var i = 0; i < reports.length; ++i) {
            report = reports[i];
            folder_div.append(
                '<form action="/view_report/" class="view-report-form" method="POST">' +
                  '<button type="submit" class="list-group-item" name="report_name" id="report_name" value="' + report.short_desc + '">' + report.short_desc +
                  (report.private ? '<span class="label label-default label-pill pull-sm-right">Private</span>' : '') +
                  '</button></form>'
                );
          }

          updateForms();
        },

        error: function(xhr, errmsg, err) {
          console.log('error');
        },
      });
    });
  };
  openFolder();


  /* view a report */
  // Yes, this is wonky. But it allows these actions to be reapplied
  // to the forms dynamically generated when opening folders.
  var updateForms = function() {
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
              '<p><em>File:</em> ' + json['file_name'] + '</p>' +
              (json['is_owner'] ? 
              '<p><form action="" class="begin-edit-report-form" method="POST">' +
              '<input type="hidden" name="report_name" value="' + json['short_desc'] + '" />' +
              '<input type="submit" value="Edit Report" class="btn btn-primary" /></form></p>' +
              '<p><form action="/delete_report/" class="delete-report-form" method="POST">' +
              '<input type="hidden" name="report_name" value="' + json['short_desc'] + '" />' +
              '<input type="submit" value="Delete Report" class="btn btn-danger" /></form></p>'
              : '')
              );

          $('form.delete-report-form').on('submit', function(event) {
            event.preventDefault();
            csrftoken = getCookie('csrftoken');
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            var delete_dict = {
              'report_name' : reportName,
            };

            $.ajax({
              url: "/delete_report/",
              type: "POST",
              data: delete_dict,

              success: function(json) {
                window.location.href="/index/";
              },

              error: function(xhr, errmsg, err) {
                console.log('error');
              }
            });
            
          });

          $('form.begin-edit-report-form').on('submit', function(event) {
              event.preventDefault();
              $('#viewreport-response').html(
                '<div class="form-group">' +
                '<form action="/edit_report/" class="edit-report-form" method="POST">' +
                '<input type="text" id="short_desc" name="short_desc" class="form-control" value="' + json['short_desc'] + '" />' +
                '<h4>' + json['time'] + '</h4>' +
                '<textarea id="long_desc" name="long_desc" rows="8" id="long_desc" class="form-control">' + json['long_desc'] + '</textarea>' +
                '<p>' + json['file_name'] + '</p>' +
                '<input type="submit" value="Save Changes" class="form-control btn btn-primary" />' +
                '</form></div>'
                  );

              $('form.edit-report-form').on('submit', function(event) {
                event.preventDefault();
                var form = $(event.target);
                short_desc = form.find('#short_desc').val();
                long_desc = form.find('#long_desc').val();

                var edit_dict = {
                  'original_name' : reportName, // we get this for free via closure
                  'short_desc' : short_desc,
                  'long_desc' : long_desc,
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
                  url: "/edit_report/",
                  type: "POST",
                  data: edit_dict,

                  success: function(json) {
                    window.location.href="/index/";
                  },

                  error: function(xhr, errmsg, err) {
                    console.log('error');
                  }
                });
                
              });
          });
        },

        error: function(xhr, errmsg, err) {
          console.log('error');
        }
      });
    });
  };
  updateForms();

  $('form.view-file-form').on('submit', function(event) {
    event.preventDefault();

    var form = $(event.target);
    fileName = form.find('#file_name').val();

    data_dict = {
      'file_name' : fileName,
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
      url: "/view_file/",
      type: "POST",
      data: data_dict,

      success: function(json) {
        $('#viewfile-response').html(
            '<h3>' + json['file_name'] + '</h3>' +
            '<h4><em>Report: </em>' + json['report_name'] + '</h4>' +
            '<p><a href="/download/' + json['file_id'] + '"><button class="btn btn-primary">Download</button></a></p>' +
            '<p><form action="/delete_file/" class="delete-file-form" method="POST">' +
            '<input type="hidden" name="file_name" value="' + json['file_name'] + '" />' +
            '<input type="submit" value="Delete file" class="btn btn-danger" /></form></p>'
            );

        $('form.delete-file-form').on('submit', function(event) {
          event.preventDefault();
          csrftoken = getCookie('csrftoken');
          $.ajaxSetup({
              beforeSend: function(xhr, settings) {
                  if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                      xhr.setRequestHeader("X-CSRFToken", csrftoken);
                  }
              }
          });

          var delete_dict = {
            'file_name' : fileName,
          };

          $.ajax({
            url: "/delete_file/",
            type: "POST",
            data: delete_dict,

            success: function(json) {
              window.location.href="/index/";
            },

            error: function(xhr, errmsg, err) {
              console.log('error');
            }
          });
          
        });

      },

      error: function(xhr, errmsg, err) {
        console.log('error');
      }
    });
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

        $('#sitemanager-viewreport-delete').html(
          '<button type="button" class="btn btn-default" id="sitemanager-viewreport-delete-button">Delete</button>'
        );

        $('#sitemanager-viewreport-delete-button').on('click', function() {
          $.ajax({
            url: "/sm_delete_report/",
            type: "POST",
            data: {
              'short_desc': reportName
            },
            success: function() {
              form.hide();
              $('#sitemanager-viewreport-response').html('');
               $('#sitemanager-viewreport-delete').html('');
            },
            error: function(xhr, errmsg, err) {
              console.log('error deleting report');
            }
          })
        })
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
