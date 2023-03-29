"use strict";

// 삭제 버튼 누르면 선수 삭제되는 기능!
const cards = document.querySelectorAll(".playerCard"); // card가져옴
const delete_button = document.querySelectorAll(".delete_button"); // card안에 있는 삭제버튼 전체로 가져온다..!

delete_button.forEach((value, index) => {
  // cards[index]를 맞춰준다..!
  value.addEventListener("click", () => {
    let playerID = cards[index].getAttribute("data-id");
    // alert(playerID);

    fetch(`/players/${playerID}`, {
      method: "POST",
      body: {
        id: playerID, // id라는 변수에 넣어서 서버로 가져감!
      },
    }).then((res) => (window.location.href = "/"));
  });
});
// const idArr = [];
// card.forEach((value) => {
//   // 클릭한 버튼의 id를 가져와야 해...!
// });
// console.log(idArr);
// // DELETE : /players/:id
