//거래방식 라디오 버튼 요소 가져오기
const f2fRadio = document.getElementById("f2f");
const noF2fRadio = document.getElementById("no-f2f");

// 거래장소 select 요소 가져오기
const locationSelect = document.getElementById("location");

document.addEventListener("DOMContentLoaded", function () {
  // 대면 라디오 버튼을 클릭할 때 거래장소 select를 활성화
  f2fRadio.addEventListener("click", function () {
    locationSelect.disabled = false;
  });

  // 비대면 라디오 버튼을 클릭할 때 거래장소 select를 비활성화
  noF2fRadio.addEventListener("click", function () {
    locationSelect.disabled = true;
  });
});
