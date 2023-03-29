"use strict";

// 삭제 버튼 누르면 선수 삭제되는 기능!
const card = document.querySelector(".playerCard"); // card가져옴
const delete_button = card.querySelector(".delete_button"); // card안에 있는 삭제버튼!
const playerID = card.getAttribute("data-id");

// DELETE : /players/:id
let callDeleteAPI = async () => {
  let callDeleteFetch = await fetch(`/players/${playerID}`, {});
};
