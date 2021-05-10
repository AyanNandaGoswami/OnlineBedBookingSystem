window.onload = initAll();

function initAll() {
    set_user_details();
}


function set_user_details() {
    $.ajax({
        type: 'GET',
        url: '/userapp/get-user-details',
        dataType: 'json',
        
        success: function (res) {

            if (res['first_name'] == null) {
                document.getElementById('profile_name').innerText = res['username'];
                document.getElementById('page_title').innerText = res['username'] + '- Dashboard';
                document.getElementById('profile_hrader_name').innerText = res['username']; 
            } else {
                document.getElementById('profile_name').innerText = res['first_name'] + ' ' + res['last_name'];
                document.getElementById('page_title').innerText = res['first_name'] + ' ' + res['last_name'] + '- Dashboard';
                document.getElementById('profile_hrader_name').innerText = res['first_name'] + ' ' + res['last_name'];
            }
            
            if (res['profile_image_link'] == null) {
                document.getElementById('profile_image').src = 'https://i.postimg.cc/BbKp2Y9K/user.png';
            } else {
                document.getElementById('profile_image').src = res['profile_image_link'];
            }
        }
    });
}

