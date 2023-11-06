//거래방식 라디오 버튼 요소 가져오기
const f2fRadio = document.getElementById("f2f_label");
const noF2fRadio = document.getElementById("no-f2f_label");
// 거래장소 select 요소 가져오기
const locationSelect = document.getElementById("location");

document.addEventListener("DOMContentLoaded", function () {
  // 대면 라디오 버튼을 클릭할 때 거래장소 select를 활성화
  f2fRadio.addEventListener("click", function () {
    locationSelect.disabled = false;
    f2fRadio.childNodes[1].style.display = "block";
    noF2fRadio.childNodes[1].style.display = "none";
  });

  // 비대면 라디오 버튼을 클릭할 때 거래장소 select를 비활성화
  noF2fRadio.addEventListener("click", function () {
    locationSelect.disabled = true;
    noF2fRadio.childNodes[1].style.display = "block";
    f2fRadio.childNodes[1].style.display = "none";
  });
});
