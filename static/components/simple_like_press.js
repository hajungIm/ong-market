// 클래스 이름으로 모든 요소를 가져옴
const likeElements = document.querySelectorAll(".item_box1_like");

// 모든 요소에 대해 클릭 이벤트 리스너를 추가
likeElements.forEach(function (likeElement) {
  const bookmarkIcon = likeElement.querySelector(".fa-bookmark");
  const bookmarkBox = likeElement.querySelector(".like_icon_box");

  bookmarkBox.addEventListener("click", function () {
    // 현재 클래스를 확인하고 클래스를 변경
    if (bookmarkIcon.classList.contains("fa-regular")) {
      bookmarkIcon.classList.remove("fa-regular");
      bookmarkIcon.classList.add("fa-solid");
      bookmarkIcon.style.color = "#242424";
    } else {
      bookmarkIcon.classList.remove("fa-solid");
      bookmarkIcon.classList.add("fa-regular");
      bookmarkIcon.style.color = "#606060";
    }
  });
});
