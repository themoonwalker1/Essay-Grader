window.setInterval(checkPassword, 600);
function checkPassword() {
    console.log("Checking Password");
    var password1 = document.getElementById("id_password_1").value;
    var password2 = document.getElementById("id_password_2").value;
    $.ajax({
        url: "/ajax/User/password",
        data: {
            'password1': password1,
            'password2': password2
        },
        success: function (data) {
            if (data.length){
                document.getElementById("b").src = document.getElementById("imgs").getAttribute("check");
            } else {
                document.getElementById("b").src = document.getElementById("imgs").getAttribute("x");
            }
            if (data.special){
                document.getElementById("c").src = document.getElementById("imgs").getAttribute("check");
            } else {
                document.getElementById("c").src = document.getElementById("imgs").getAttribute("x");
            }
            if (data.number){
                document.getElementById("d").src = document.getElementById("imgs").getAttribute("check");
            } else {
                document.getElementById("d").src = document.getElementById("imgs").getAttribute("x");
            }
            if (data.upandlow){
                document.getElementById("e").src = document.getElementById("imgs").getAttribute("check");
            } else {
                document.getElementById("e").src = document.getElementById("imgs").getAttribute("x");
            }
            if (data.match){
                document.getElementById("f").src = document.getElementById("imgs").getAttribute("check");
            } else {
                document.getElementById("f").src = document.getElementById("imgs").getAttribute("x");
            }
        }
    });
}