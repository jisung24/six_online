document.addEventListener("DOMContentLoaded", function () {

    // 진영 : 선수 검색 
    let searchBtn = document.querySelector('#searchBtn')

    searchBtn.addEventListener('click',searchPlayer)

    function searchPlayer(){
        fetch('/player', { method: "GET", body: formData, }).then((res) => res.json()).then((data) => {
            let row = data['result']
            let searchName = $('#searchBox').val()

            row.forEach((a)=>{
                let img = a['player_img']
                let name = a['player_name']
                let team = a['player_team']
                let back_number = a['player_back_number']
                let position = a['player_position']
                let age = a['player_age']
                let like = a['player_like']

                let temp_html = `<div class="card">
                                    <button type="button" class="like">
                                        <i class="${like} fa-heart likeIcon"></i>
                                    </button>
                                    <div class="imgbox"><img src="${img}" class="player-img"></div>
                                    <p class="name">${name}</p>
                                    <p class="team">${team}</p>
                                    <p class="back-number">${back_number}</p>
                                    <p class="position">${position}</p>
                                    <p class="age">${age}</p>
                                </div>`
                                
                if(searchName == a['player_name']){
                    $('.list-area').append(temp_html)
                } else {
                    alert('검색 결과가 없습니다.')
                }
                
            })
        });
    }

    // 사용자 : 좋아요 토글 버튼
    let likeBtn = document.querySelector('.like');
    let likeBtnIcon = document.querySelector('.likeIcon');

    likeBtn.addEventListener('click', likedToggle);

    function likedToggle(e) {
        console.log(likeBtnIcon)
        if (likeBtnIcon.className.contains == 'far') {
            e.likeBtnIcon.classList.remove('far');
            e.likeBtnIcon.classList.add('fas');
        } else {
            e.likeBtnIcon.classList.remove('fas');
            e.likeBtnIcon.classList.add('far');
        }
    }

    // 관리자 : 이미지 등록 미리보기
    let input = document.querySelector('label');
    let preview = document.querySelector('.imgthumb');

    function updateImageDisplay() {
        while (preview.firstChild) {
            preview.removeChild(preview.firstChild);
        }

        const curFiles = input.files;
        if (curFiles.length === 0) {
            const para = document.createElement('p');
            para.textContent = 'No files currently selected for upload';
            preview.appendChild(para);
        } else {
            const list = document.createElement('ol');
            preview.appendChild(list);

            for (const file of curFiles) {
                const listItem = document.createElement('li');
                const para = document.createElement('p');
                if (validFileType(file)) {
                    para.textContent = `File name ${file.name}, file size ${returnFileSize(file.size)}.`;
                    const image = document.createElement('img');
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

    input.addEventListener('change', updateImageDisplay);

});