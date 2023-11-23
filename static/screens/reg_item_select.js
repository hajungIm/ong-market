//-----------------폼 등록 시간--------------//
//현재 날짜 및 시간 설정
const regDate = document.getElementById("reg_date");
const currentDate = new Date();

// 원하는 형식으로 변환
const formattedDate = `${currentDate.getFullYear()}-${(
  currentDate.getMonth() + 1
)
  .toString()
  .padStart(2, "0")}-${currentDate
  .getDate()
  .toString()
  .padStart(2, "0")}T${currentDate
  .getHours()
  .toString()
  .padStart(2, "0")}:${currentDate.getMinutes().toString().padStart(2, "0")}`;

// 폼 요소에 설정
regDate.value = formattedDate;
console.log("formattedDate = ", formattedDate);
console.log("regDate.value = ", regDate.value);

//---------거래장소 select----------//
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
