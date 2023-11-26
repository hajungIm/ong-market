// HTML 요소를 가져옵니다.
var element = document.querySelector('.keyword_num');

// 텍스트 내에서 숫자만 추출합니다.
var text = element.textContent.trim();
var number = parseInt(text.match(/\d+/)[0], 10);

// 결과를 출력합니다.
console.log(number);
