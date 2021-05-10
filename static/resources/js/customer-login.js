const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});


// my code 

document.getElementById('sign-up-btn-id').addEventListener('click', register);

function register() {
	var email = document.getElementById('reg-email').value;
    var username = document.getElementById('reg-username').value;
    var password = document.getElementById('reg-password').value;

    let csrfToken = $("input[name=csrfmiddlewaretoken").val();
    
    $.ajax({
        type: 'POST',
        url: '/customer/create-new-customer/',
        data: {
            'username': username,
            'password': password,
            'email': email,
            csrfmiddlewaretoken: csrfToken
        },
        dataType: 'json', 
        
        success: function (res) {
            var login_status = false;
            login_status = res['login'];
            if(login_status == true) {
                var url = '/customer/dashboard';
                document.location.href = url;
            } else {
                if (res['email'] == undefined) {
                    document.getElementById('error-msg').innerHTML = res['username'];
                } else if (res['username'] == undefined){ 
                    document.getElementById('error-msg').innerHTML = res['email'];
                } else {
                    var err_msg_id = document.getElementById('error-msg');
                    err_msg = res['username'] + "<br>" + res['email'];
                    err_msg_id.innerHTML = err_msg;
                }
            }
        }
    });
    
}



function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    let csrfToken = $("input[name=csrfmiddlewaretoken").val();

    if(fields_are_not_null() == false) {
        return false;
    }

    $.ajax({
        type: 'POST',
        url: '/account/user-login/',
        data: {
            'username': username,
            'password': password,
            csrfmiddlewaretoken: csrfToken
        },
        dataType: 'json', 
        
        success: function (res, status) {
            if(res.is_authenticated==true){
                var url = '/profile';
                document.location.href = url;
            } else {
                // cleanForm();
                document.getElementById('username').classList.add('is-invalid');
                document.getElementById('password').classList.add('is-invalid');
                document.getElementById('error-msg').innerHTML = 'Invalid login credentials.';
                setTimeout(function() {
                    document.getElementById('error-msg').innerHTML = '';    
                }, 3000);
            }
        }
    });
    
}
