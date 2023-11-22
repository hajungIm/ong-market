const newPassword = document.getElementById("newPassword");
const newPasswordCheck = document.getElementById("newPasswordCheck");

const errorMessage = document.getElementById("password_check__error");
const submitBtn = document.getElementById("confirm_btn_id");

submitBtn.disabled = true; //초기 수정하기 버튼 비활성화

//input에 값이 입력될 때마다 함수 호출되도록 이벤트 리스너에 연결
newPassword.addEventListener("keyup", submitBtnActivate);
newPasswordCheck.addEventListener("keyup", submitBtnActivate);

//submitBtn 클릭시 -> 서버에 비밀번호 변경 요청 (fetch API 사용)
submitBtn.addEventListener("click", function () {
  //클라이언트가 서버의 엔드포인트로 POST 요청
  fetch("/change_password", {
    // 백엔드의 엔드포인트에 맞게 수정해야 함.
    method: "POST", //요청 메소드 : POST
    headers: {
      //요청 헤더 : 컨텐츠가 JSON임을 명시
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      //비밀번호를 JSON 형식으로 보냄
      newPassword: newPassword.value,
    }),
  })
    .then((response) => {
      //서버로부터 응답을 처리하는 함수 정의
      if (!response.ok) {
        //HTTP 응답이 정상적이지 않으면 에러 발생
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json(); //JSON 형식 응답을 parsing & then 블록으로 전달
    })
    .then((data) => {
      //서버에서 받은 JSON 데이터의 message 속성을 알림창으로 표시
      alert(data.message);
    })
    .catch((error) => {
      //요청이 실패하거나, 서버에서 에러 응답이 오는 경우, 변경 실패 에러 알림창 표시
      alert("비밀번호 변경 에러: " + error.message);
    });
});

//비빌번호 일치 여부에 따라 제출 버튼 활성화, 비활성화 설정
function submitBtnActivate() {
  if (comparePassword()) {
    submitBtn.disabled = false;
  } else {
    submitBtn.disabled = true;
  }
}

//새 비밀번호, 비밀번호 확인이 서로 같은지 확인
function comparePassword() {
  if (newPassword.value.length !== 0 || newPasswordCheck.value.length !== 0) {
    if (newPassword.value !== newPasswordCheck.value) {
      errorMessage.innerHTML = "비밀번호가 일치하지 않습니다.";
      return false;
    } else {
      errorMessage.innerHTML = "";
      return true;
    }
  }
}
