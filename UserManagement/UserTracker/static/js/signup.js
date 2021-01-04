    var left_height=$("#left").css("height")
    $("#right").css("height",left_height)
    document.querySelector("#id_password").type="password"
    function auth_confirm() {
        if ($("#id_password").value() === $("#pass_confirm").value()){
            $("#form").submit()
        }
        else{
            alert("Passwords do not match")
        }
    }