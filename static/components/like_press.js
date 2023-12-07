// 클래스 이름으로 모든 요소를 가져옴
const likeElements = document.querySelectorAll(".item_box1_like");

// 모든 요소에 대해 클릭 이벤트 리스너를 추가
likeElements.forEach(function (likeElement) {
  const bookmarkIcon = likeElement.querySelector(".fa-bookmark");

  const likeCounter = likeElement.querySelector(".item_like_num");
  const bookmarkBox = likeElement.querySelector(".like_icon_box");

  //찜하기 버튼 눌렀을 때 상품 상세 화면으로 이동하지 않도록 막기
  likeElement.addEventListener("click", function (event) {
    event.preventDefault(); // 기본 동작 막기
    // 여기에 필요한 로직 추가
  });

  //찜하기 버튼 눌렀을 때 색상 변하도록
  bookmarkBox.addEventListener("click", function () {
    if (userId === "no session") {
      console.log("로그인 안한 사람이 찜 클릭 -> alert 띄우기");
      alert("로그인 한 사용자만 이용가능합니다!");
      return;
    }

    // 현재 클래스를 확인하고 클래스를 변경
    var itemId = this.closest(".item_box1").id.replace("item-", "");
    let flag; // 좋아요를 증가시키려면 1, 감소시키려면 -1로 설정

    if (bookmarkIcon.classList.contains("fa-regular")) {
      console.log("찜한 안한 상태에서 클릭");
      flag = 1;
      console.log("현재 flag ", flag);
      bookmarkIcon.classList.remove("fa-regular");
      bookmarkIcon.classList.add("fa-solid");
      bookmarkIcon.style.color = "#242424";
      likeCounter.textContent = parseInt(likeCounter.textContent) + 1; // 값 증가
    } else {
      console.log("찜한상태에서 클릭");
      flag = -1;
      console.log("현재 flag ", flag);
      bookmarkIcon.classList.remove("fa-solid");
      bookmarkIcon.classList.add("fa-regular");
      bookmarkIcon.style.color = "#606060";
      likeCounter.textContent = parseInt(likeCounter.textContent) - 1; // 값 감소
    }
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/like/" + itemId, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function () {
      if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        console.log("찜하기 업데이트 성공: " + response.message);
      } else {
        alert("오류가 발생했습니다: " + xhr.status);
      }
    };
    xhr.send(JSON.stringify({ itemId: itemId, flag: flag }));
  });
});

//페이지 로드 시 찜한 상품이면 찜 표시되도록 업데이트
document.addEventListener("DOMContentLoaded", function () {
  likeItemIds.forEach((itemId) => {
    const bookmarkIcon = document.querySelector(
      `#item-${itemId} .item_box1_like .fa-bookmark`
    );
    if (bookmarkIcon === null) {
      return;
    }

    bookmarkIcon.classList.remove("fa-regular");
    bookmarkIcon.classList.add("fa-solid");
    bookmarkIcon.style.color = "#242424";
  });
});
