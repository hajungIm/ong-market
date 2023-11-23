document.addEventListener("DOMContentLoaded", function () {
  var dateElements = document.querySelectorAll(".item_reg_date");
  dateElements.forEach(function (dateElement) {
    // HTML 요소에서 날짜 문자열 읽기
    const dateString = dateElement.textContent || dateElement.innerHTML;

    // 날짜 문자열 파싱
    const [datePart, timePart] = dateString.split("T");
    const [year, month, day] = datePart.split("-");
    const [hour, minute] = timePart.split(":");

    // 상품 등록 날짜와 시간으로 Date 객체 생성
    const userDate = new Date(year, month - 1, day, hour, minute);

    // 현재 시간으로 Date 객체 생성
    const currentDate = new Date();

    // 두 날짜의 차이 계산
    const timeDiff = currentDate - userDate;
    const daysDiff = Math.floor(timeDiff / (1000 * 60 * 60 * 24));

    // '며칠 전'을 표시
    let displayText = "";
    if (daysDiff === 0) {
      displayText = "오늘";
    } else if (daysDiff === 1) {
      displayText = "1일 전";
    } else {
      displayText = `${daysDiff}일 전`;
    }

    // 결과를 HTML 요소에 적용
    dateElement.textContent = displayText;
  });
});
