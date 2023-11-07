// 현재 페이지의 title 요소를 가져오기
const homeIcon = document.getElementById("nav_list");
const likeIcon = document.getElementById("nav_like");
const dmIcon = document.getElementById("nav_dm_list");
const mypageIcon = document.getElementById("nav_mypage");
var pageTitle = document.title;

// 현재 페이지의 title이 목표 타이틀과 일치하는지 확인
switch (pageTitle) {
  case "상품 전체 조회":
    homeIcon.firstChild.style.color = "#242424";
    break;

  case "찜한 상품":
    likeIcon.firstChild.style.color = "#242424";
    break;
  case "채팅 목록":
    dmIcon.firstChild.style.color = "#242424";
    break;
  case "마이페이지":
  case "판매중 상품":
  case "거래완료":
    mypageIcon.firstChild.style.color = "#242424";
}
