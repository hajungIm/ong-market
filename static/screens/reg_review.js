// 라디오 버튼 요소들과 해당 아이콘 요소들을 가져옵니다.
const starInputs = document.querySelectorAll(".checkbox_rate");
const starIcons = document.querySelectorAll(".star i");
const keywordInputs = document.querySelectorAll(".checkbox_keyword");
const keyworLabels = document.querySelectorAll(".keyword_list");
// 라디오 버튼 상태가 변경될 때 호출되는 함수
starInputs[0].disabled = false;
for (let i = 0; i < starInputs.length; i++) {
  starInputs[i].disabled = false;
}

function updateStarColors() {
  starInputs.forEach((input, index) => {
    const icon = starIcons[index];
    if (input.checked) {
      console.log("별 색상 바뀌기");
      // 라디오 버튼이 체크되었을 때 아이콘 색상을 빨간색으로 변경
      icon.style.color = "#BF190E";
      if (index < starInputs.length - 1) {
        starInputs[index + 1].disabled = false;
      }
    } else {
      // 라디오 버튼이 해제됐을 때 아이콘 색상을 초기 색깔로 변경 (여기서는 #d9d9d9)
      icon.style.color = "#d9d9d9";
      for (let i = index + 1; i < starInputs.length; i++) {
        starInputs[i].disabled = true;
        starInputs[i].checked = false;
      }
    }
  });
}

// 키워드 선택 필수 + 선택할 키워드 없음 선택시 모두 비활성화 처리 기능 구현해야 함.
function updateKeywordColors() {
  keywordInputs.forEach((input, index) => {
    const box = keyworLabels[index];
    if (input.checked) {
      // 체크되었을 때 아이콘 색상을 빨간색으로 변경
      box.style.color = "#FFFFFF";
      box.style.backgroundColor = "#242424";
    } else {
      // 해제됐을 때 아이콘 색상을 초기 색깔로 변경 (여기서는 #d9d9d9)
      box.style.backgroundColor = "#F5F5F5";
      box.style.color = "#242424";
    }
  });
}

// 상태 변경 이벤트에 이벤트 리스너를 추가합니다.
starInputs.forEach((input) => {
  input.addEventListener("change", updateStarColors);
});

keywordInputs.forEach((input) => {
  input.addEventListener("change", updateKeywordColors);
});

// 뒤로가기
document.addEventListener("DOMContentLoaded", function () {
  // 뒤로가기 버튼에 이벤트 리스너 추가
  const backButton = document.querySelector(".base_header__icon");
  backButton.addEventListener("click", function () {
    history.back();
  });
});
// 초기 색상 설정
updateStarColors();
updateKeywordColors();
const noKeywordLabel = document.getElementById('no_keyword');
const otherKeywordLabels = document.querySelectorAll('.checkbox_keyword:not(#no_keyword)');
const checkboxKeywords = document.querySelectorAll('.checkbox_keyword:not(#no_keyword)');
const keywordInputs2 = document.querySelectorAll(".checkbox_keyword:not(#no_keyword)");

// '선택할 키워드가 없어요.' 체크박스 클릭 이벤트 처리
let clickCount = 1;

noKeywordLabel.addEventListener('change', function () {
  const isChecked = clickCount % 2;
  if (isChecked == 1) {
    console.log("isChecked is true");
    otherKeywordLabels.forEach(function (label) {
      label.style.color = isChecked ? "#d9d9d9" : "#242424";
      label.style.backgroundColor = isChecked ? "#F5F5F5" : "#242424";
    });

    checkboxKeywords.forEach(function (checkbox) {
      checkbox.disabled = true;
      checkbox.checked = false;
      // 추가된 부분: 선택할 수 없는 버튼은 시각적으로 다르게 스타일 적용
    });

    keywordInputs2.forEach(function (input, index) {
        keyworLabels[index].style.backgroundColor = "#F5F5F5";
        keyworLabels[index].style.color = "#242424";
        keyworLabels[index].style.cursor = 'not-allowed';
        keyworLabels[index].style.opacity = 0.5;
    });
    clickCount++;

  } else {
    console.log("isChecked is false");
    otherKeywordLabels.forEach(function (label) {
      label.style.color = "#242424";
      label.style.backgroundColor = "#F5F5F5";
    });

    checkboxKeywords.forEach(function (checkbox) {
      checkbox.disabled = false;
      checkbox.checked = false;
      // 추가된 부분: 선택할 수 있는 버튼은 스타일 초기화
    });
    keywordInputs2.forEach(function (input, index) {
      keyworLabels[index].style.cursor = 'pointer';
      keyworLabels[index].style.opacity = 1;
  });

    clickCount = 1;
  }
});