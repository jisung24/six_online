"use strict";

function login() {
  alert("hello!");
  let userID = document.querySelector("#userID");
  let userPW = document.querySelector("#userPW");

  if (userID.value === "") {
    alert("아이디를 입력하세요!");
    userID.focus();
  }

  if (userPW.value === "") {
    alert("pw입력하세요!");
    userPW.focus();
  }

  $ajax({
    type: "POST",
    url: "/api/login",
    data: {
      userID: userID.value,
      userPW: userPW.value,
    },
    success: (res) => {
      if (res["result"] === "success") {
        $.cookie("mytoken", res["token"], { path: "/" });
        window.location.replace("/");
      } else {
        alert(res["msg"]);
      }
    },
  });
}
