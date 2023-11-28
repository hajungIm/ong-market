document.addEventListener("DOMContentLoaded", function () {
  var descriptionElements = document.querySelectorAll(".line_break");
  descriptionElements.forEach(function (descriptionElement) {
    // HTML 요소에서 텍스트 읽기
    const text = descriptionElement.textContent || descriptionElement.innerHTML;

    // 개행 문자를 HTML 줄바꿈 태그로 대체
    const formattedText = text.replace(/\n/g, "<br>");

    // HTML 요소에 적용
    descriptionElement.innerHTML = formattedText;
  });
});
