"use strict";
let logout = document.querySelector(".logout");
logout.addEventListener("click", () => {
  $.removeCookie("mytoken", { path: "/" });
  window.location.href = "/";
});
