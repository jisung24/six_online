document.addEventListener("DOMContentLoaded", function () {
  // 사용자 : 좋아요 토글 버튼
  let likeBtn = document.querySelector(".like");
  let likeBtnIcon = document.querySelector(".likeIcon");

  likeBtn.addEventListener("click", likedToggle);

  function likedToggle(e) {
    console.log(likeBtnIcon);
    if (likeBtnIcon.className.contains == "far") {
      e.likeBtnIcon.classList.remove("far");
      e.likeBtnIcon.classList.add("fas");
    } else {
      e.likeBtnIcon.classList.remove("fas");
      e.likeBtnIcon.classList.add("far");
    }
  }

  // 관리자 : 이미지 등록 미리보기
  let input = document.querySelector("label");
  let preview = document.querySelector(".imgthumb");

  function updateImageDisplay() {
    while (preview.firstChild) {
      preview.removeChild(preview.firstChild);
    }

    const curFiles = input.files;
    if (curFiles.length === 0) {
      const para = document.createElement("p");
      para.textContent = "No files currently selected for upload";
      preview.appendChild(para);
    } else {
      const list = document.createElement("ol");
      preview.appendChild(list);

      for (const file of curFiles) {
        const listItem = document.createElement("li");
        const para = document.createElement("p");
        if (validFileType(file)) {
          para.textContent = `File name ${
            file.name
          }, file size ${returnFileSize(file.size)}.`;
          const image = document.createElement("img");
          image.src = URL.createObjectURL(file);

          listItem.appendChild(image);
          listItem.appendChild(para);
        } else {
          para.textContent = `File name ${file.name}: Not a valid file type. Update your selection.`;
          listItem.appendChild(para);
        }

        list.appendChild(listItem);
      }
    }
  }

  input.addEventListener("change", updateImageDisplay);
});
