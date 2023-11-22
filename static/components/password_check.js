const newPassword = document.getElementById("newPassword");
const newPasswordCheck = document.getElementById("newPasswordCheck");

const errorMessage = document.getElementById("password_check__error");
const submitBtn = document.getElementById("confirm_btn_id");

submitBtn.disabled = true; //초기 수정하기 버튼 비활성화

//input에 값이 입력될 때마다 함수 호출되도록 이벤트 리스너에 연결
newPassword.addEventListener("keyup", submitBtnActivate);
newPasswordCheck.addEventListener("keyup", submitBtnActivate);

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
