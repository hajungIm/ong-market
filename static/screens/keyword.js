// HTML 요소를 가져옵니다.
var element = document.querySelector('.keyword_num');

// 텍스트 내에서 숫자만 추출합니다.
var text = element.textContent.trim();
var number = parseInt(text.match(/\d+/)[0], 10);

// 결과를 출력합니다.
console.log(number);

var reviewItems = [
    document.getElementById("time"),
    document.getElementById("detail"),
    document.getElementById("resonable"),
    document.getElementById("kind"),
    document.getElementById("condition"),
    document.getElementById("response"),
    document.getElementById("give"),
    document.getElementById("come")
  ];

var reviewClass = [
    document.getElementById("green green_1"),
    document.getElementById("green green_2"),
    document.getElementById("green green_3"),
    document.getElementById("green green_4"),
    document.getElementById("green green_5"),
    document.getElementById("green green_6"),
    document.getElementById("green green_7"),
    document.getElementById("green green_8")
];

function setOpacity(elementId, opacityValue, elementclass) {
    var element = document.getElementById(elementId);
    var opacityValue = element / 10;
    if (element) {
      elementclass.style.opacity = opacityValue;
    }
  }

  for(var i = 0; i < 8; i++){
    setOpacity(reviewItems[i], reviewItems[i]/number, reviewClass[i]);
    reviewClass[i].style.width = reviewItems[i]/number;
  }
