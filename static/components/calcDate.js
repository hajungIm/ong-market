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
    const secondsDiff = Math.floor(timeDiff / 1000);
    const minutesDiff = Math.floor(secondsDiff / 60);
    const hoursDiff = Math.floor(minutesDiff / 60);
    const daysDiff = Math.floor(hoursDiff / 24);
    const weeksDiff = Math.floor(daysDiff / 7);
    const monthsDiff = Math.floor(daysDiff / 30);
    const yearsDiff = Math.floor(daysDiff / 365);

    // 결과를 HTML 요소에 적용
    let displayText = "";
    if (secondsDiff < 60) {
      displayText = `${secondsDiff}초 전`;
    } else if (minutesDiff < 60) {
      displayText = `${minutesDiff}분 전`;
    } else if (hoursDiff < 24) {
      displayText = `${hoursDiff}시간 전`;
    } else if (daysDiff < 7) {
      displayText = `${daysDiff}일 전`;
    } else if (weeksDiff < 4) {
      displayText = `${weeksDiff}주 전`;
    } else if (monthsDiff < 12) {
      displayText = `${monthsDiff}달 전`;
    } else {
      displayText = `${yearsDiff}년 전 이상`;
    }

    // 결과를 HTML 요소에 적용
    dateElement.textContent = displayText;
  });
});
