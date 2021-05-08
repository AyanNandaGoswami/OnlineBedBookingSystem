document.getElementById('reg-btn').addEventListener('click', register);

function register() {
    var hospital_name = document.getElementById('hospital_name').value;
    var hospital_id = document.getElementById('hospital_id').value;
    var state = document.getElementById('state').value;
    var hospital_type = document.getElementById('hospital_type').value;
    var email = document.getElementById('email').value;
    var help_line = document.getElementById('help_line').value;
    var username = document.getElementById('user_name').value;
    var password = document.getElementById('password').value;

    let csrfToken = $("input[name=csrfmiddlewaretoken").val();

    $.ajax({
        type: 'POST',
        url: '/hospital/register-new-hospital/',
        data: {
            'name': hospital_name,
            'hospital_id': hospital_id,
            'state': state,
            'hospital_type': hospital_type,
            'email': email,
            'help_line': help_line,
            'username': username,
            'password': password,
            csrfmiddlewaretoken: csrfToken
        },
        dataType: 'json',
        
        success: function (res) {
            var login_status = false;
            login_status = res['login'];
            if(login_status == true) {
                // var url = '/profile';
                // document.location.href = url;
                console.log('ok');
            } else {
                document.getElementById('error-msg').innerHTML = res['username'];
            }
        }
    }); 
}


