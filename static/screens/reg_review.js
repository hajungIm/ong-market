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

// 초기 색상 설정
updateStarColors();
updateKeywordColors();

// '선택할 키워드가 없어요.' 라벨과 다른 라벨들을 가져옵니다.
const noKeywordLabel = document.getElementById('no_keyword');
const otherKeywordLabels = document.querySelectorAll('.keyword_list:not(#no_keyword)');
const checkboxKeywords = document.querySelectorAll('.checkbox_keyword:not(#no_keyword)');

// '선택할 키워드가 없어요.' 라벨 클릭 이벤트 처리
let clickCount = 0;

noKeywordLabel.addEventListener('change', function () {
  clickCount++;
  const isChecked = clickCount % 2 === 0;

  otherKeywordLabels.forEach(function (label) {
    label.style.color = isChecked ? "#d9d9d9" : "#242424";
    label.style.backgroundColor = isChecked ? "#F5F5F5" : "#242424";
  });

  checkboxKeywords.forEach(function (checkbox) {
    checkbox.disabled = isChecked;
    checkbox.checked = false;
  });

  // 만약 '선택할 키워드가 없어요'가 선택되었고, 다른 키워드 중 하나 이상이 선택되어 있으면
  // 다른 키워드들을 초기화하고 '선택할 키워드가 없어요'를 선택한 횟수 초기화
  if (isChecked) {
    otherKeywordLabels.forEach(function (label) {
      if (clickCount) {
        label.style.backgroundColor = "#F5F5F5";
        label.style.color = "#242424";
      }
    });
    clickCount = 0;
  }
});



// 다른 체크박스를 눌렀을 때 clickCount를 초기화하는 부분 추가
});