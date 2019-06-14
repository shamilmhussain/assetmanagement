$(document).ready(function () {

                function checkPasswordMatch() {
                    var password = $("#password").val();
                    var confirmPassword = $("#password2").val();




                    if (password == "" && confirmPassword == ""){
                        $("#message").removeClass()
                        $("#message2").html("")}
                    else if (password == confirmPassword){
                        $("#message").addClass("fas fa-smile").removeClass("fa-angry").css("color","white")
                        $("#message2").html("Passwords match!").css("color","white")}
                    else if(password != confirmPassword){
                        $("#message").addClass("fas fa-angry").removeClass("fa-smile").css("color","red")
                        $("#message2").html("Passwords do not match!").css("color","red")}




                }


                $("#password2").keyup(checkPasswordMatch);

                $("#password2").focusout(function(){
                    var password = $("#password").val();
                    var confirmPassword = $("#password2").val();

                    if (confirmPassword==""){
                        $("#message").removeClass()
                        $("#message2").html("")}

                });

                $("#password").keyup(function(){
                    var password = $("#password").val();
                    var confirmPassword = $("#password2").val();


                    if (password == confirmPassword && confirmPassword != ""){
                        $("#message").addClass("fas fa-smile").removeClass("fa-angry").css("color","white")
                        $("#message2").html("Passwords match!").css("color","white")}


                    else if(password != confirmPassword && confirmPassword != ""){
                        $("#message").addClass("fas fa-angry").removeClass("fa-smile").css("color","red")
                        $("#message2").html("Passwords do not match!").css("color","red")}


                });



                function checkUser(data,usr,msg){
                  var check=false;

                  for (i=0; i<data.length; i++){
                    if( data[i].username == usr){
                        check=true;
                        break;
                    }
                  }

                  if(usr==""){
                    msg.html("")
                  }
                  else if(check==true){
                    msg.html("Username already exist").css("color","red");
                    $("#username")[0].setCustomValidity("Username already exist")
                  }
                  else{
                    msg.html("Username Available").css("color","white");
                    $("#username")[0].setCustomValidity("")
                  }
                }


                $("#username").on("keyup change",function(){
                      var us = $("#username").val()

                      var ourRequest = new XMLHttpRequest();
                      var ms = $("#msg")
                      ourRequest.open('GET','/usernames/')
                      ourRequest.onload = function(){
                        var ourData = JSON.parse(ourRequest.responseText);
                        checkUser(ourData,us,ms);
                      };
                      ourRequest.send();

                });

                $("#sub-btn").click(function(){
                    var password = $("#password").val();
                    var confirmPassword = $("#password2").val();
//                    var phone = $("#phone").val();
//                    var len = phone.length
//                      var u = $("#username")
//                      var v=document.getElementById("message4");
//                      var x = document.getElementById("username");


                    if (password != confirmPassword){
                        $("#password2")[0].setCustomValidity("Password donot match.");
                    }

                    else if(password == confirmPassword && confirmPassword != ""){
                        $("#password2")[0].setCustomValidity("");
                    }
//                  if(check==true){
//                    v.html("true")
//
//
//                  }
//                  else{
//                    v.html("false")
//                    x.setCustomValidity("")
//
//                  }
//                    if(typeof phone != "number")
//                    {
//                        phone.val(typeof phone)
//                    }

//                    if(len != 10 ){
//                        phone.setCustomValidity("Please Enter Phone Numbe of Length 10");
//                    }
//                    else if(len == 10){
//                        phone.setCustomValidity("");
//                    }


                });

//                    function pageRedirect() {
//
//                        window.location.replace("http://127.0.0.1:8080/login/");
//
//                    }
//                var key = $("key-btn").val()
//
//                if (key=="account-created"){
//                    setTimeout("pageRedirect()", 10000);
//                    }




        });