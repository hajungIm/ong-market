document.addEventListener("DOMContentLoaded", function () {
  const timestamps = document.querySelectorAll(".timeformat");
  timestamps.forEach((timestamp) => {
    const dateString = timestamp.textContent || timestamp.innerHTML;
    // 날짜 문자열 파싱
    const [datePart, timePart] = dateString.split(",");
    const [day, month, year] = datePart.trim().split("/");
    const [hour, minute, second] = timePart.trim().split(":");

    //마지막 dm 날짜와 시간으로 Date 객체 생성
    const lastTime = new Date(year, month - 1, day, hour, minute, second);

    // 현재 시간으로 Date 객체 생성
    const currentDate = new Date();

    // 두 날짜의 차이 계산
    const timeDiff = currentDate.getTime() - lastTime.getTime();
    const secondsDiff = Math.round(timeDiff / 1000);
    const minutesDiff = Math.round(secondsDiff / 60);
    const hoursDiff = Math.round(minutesDiff / 60);
    const daysDiff = Math.round(hoursDiff / 24);
    const weeksDiff = Math.round(daysDiff / 7);
    const monthsDiff = Math.round(daysDiff / 30);
    const yearsDiff = Math.round(daysDiff / 365);

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

    timestamp.textContent = displayText;
  });
});
