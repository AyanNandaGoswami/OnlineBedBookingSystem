window.onload = initAll();

function initAll() {
    set_user_details();
    get_patients('Alive');
}


function set_user_details() {
    $.ajax({
        type: 'GET',
        url: '/userapp/get-user-details',
        dataType: 'json',
        
        success: function (res) {

            if (res['first_name'] == null) {
                document.getElementById('profile_name').innerText = res['username'];
                document.getElementById('page_title').innerText = res['username'] + ' - Dashboard';
                document.getElementById('profile_name_footer').innerHTML = "<div class=\"small\">Logged in as:</div>"+res['username']; 
            } else {
                document.getElementById('profile_name').innerText = res['first_name'] + ' ' + res['last_name'] + ' - Dashboard';
                document.getElementById('page_title').innerText = res['first_name'] + ' ' + res['last_name'] + '- Dashboard';
                document.getElementById('profile_name_footer').innerHTML = "<div class=\"small\">Logged in as:</div>" + res['first_name'] + " " + res['last_name'];
            }
            
            // if (res['profile_image_link'] == null) {
            //     document.getElementById('profile_image').src = 'https://i.postimg.cc/BbKp2Y9K/user.png';
            // } else {
            //     document.getElementById('profile_image').src = res['profile_image_link'];
            // }
        }
    });
}

function get_patients(slug) {
    $ ( document ).ready(function() {
        $.ajax({
            type: 'GET',
            url: '/hospital/get-patients/'+slug,
            dataType: 'json',
            
            success: function(res) {

                document.getElementById('databse_name').innerHTML = "<i class=\"fas fa-table mr-1\"></i>" + res['status'] + " Patients";      // change database table name

                var data = res['patients'];
                var table = $('#dataTable').DataTable();

                table.clear().draw();   // clear all rows

                for(i=0; i<data.length; i++) {
                    table.row.add( {
                        [0]:    "<a href=\"" + data[i]['slug'] + "\">" + data[i]['name'] + "</a>",
                        [1]:    data[i]['adahr'],
                        [2]:    data[i]['status'],
                        [3]:    new Date(data[i]['created_at'])
                    } ).draw().node();
                }
            }
        });
    });
}

