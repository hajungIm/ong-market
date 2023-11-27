const photoBtn = document.getElementsByClassName("photo_btn")[0];
const photoChangePanel = document.getElementById("photo_change");
const cancleBtn = document.getElementsByClassName("cancel_btn")[0];
const fileSubmitBtn = document.getElementById("photo_submit_btn");
const fileInput = document.getElementById("profileImgInput");
const img = document.getElementById("current_profile_image"); //현재 프로필 이미지 요소를 가져온다.
const origin_img = img.src; //원래 이미지 src
//초기화
// fileSubmitBtn.disabled = true;
fileSubmitBtn.style.backgroundColor = "#949494";
photoChangePanel.style.visibility = "hidden";

photoBtn.addEventListener("click", function () {
  hasFileInput();
  photoChangePanel.style.visibility = "visible";
});

cancleBtn.addEventListener("click", function () {
  //프로필 이미지 원래대로 돌려놓기
  img.src = origin_img;
  // 업로드 파일 비어있게 저장
  fileInput.value = "";
  photoChangePanel.style.visibility = "hidden";
});

fileInput.addEventListener("change", hasFileInput);

//file input이 있으면 버튼 활성화 / 없으면 비활성화
function hasFileInput() {
  if (fileInput.files.length == 0) {
    // fileSubmitBtn.disabled = true;
    fileSubmitBtn.style.backgroundColor = "#949494";
    return false;
  } else {
    //선택한 파일이 있는 경우
    //파일 리더 생성 및 onload 이벤트 핸들링
    const reader = new FileReader();
    reader.onload = (e) => {
      if (!e.target.result.startsWith("data:image/")) {
        alert("이미지 파일을 선택하세요.");
        return;
      } else {
        //파일 읽을 때 실행할 함수 등록
        img.src = e.target.result; //이미지 요소의 src url을 변경한다.
        console.log("파일 선택 완료. 이미지 반영 완료");
        //e.target.result는 파일이 성공적으로 읽혀온 결과물을 나타낸다.
        //Data URL 형식으로, 이미지 파일의 내용을 문자열로 포함하고 있습니다.

        fileSubmitBtn.style.backgroundColor = "var(--blue)";
        // fileSubmitBtn.disabled = false;
      }
    };
    reader.readAsDataURL(fileInput.files[0]); // 파일 읽기 시작
    return true;
  }
}
