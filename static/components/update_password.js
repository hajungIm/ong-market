document.addEventListener("DOMContentLoaded", function () {
  const updatePasswordForm = document.getElementById("updatePasswordForm");

  updatePasswordForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(updatePasswordForm);
    console.log("FormData:", formData);
    const newPassword = formData.get("newPassword");
    console.log("newPassword:", newPassword);
    const newPasswordCheck = formData.get("confirmPassword");

    // 클라이언트 측 유효성 검사
    if (newPassword !== newPasswordCheck) {
      document.getElementById("password_check__error").innerText =
        "비밀번호가 일치하지 않습니다.";
      return;
    } else {
      document.getElementById("password_check__error").innerText = "";
    }

    // 서버로 비밀번호 업데이트 요청
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/update_password", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    xhr.onload = function () {
      if (xhr.status === 200) {
        const response = JSON.parse(xhr.responseText);
        if (response.success) {
          alert("비밀번호가 성공적으로 변경되었습니다!");
          window.location.reload(); // 페이지 새로고침 또는 리디렉션
        } else {
          alert("비밀번호 업데이트에 실패했습니다.");
        }
      }
    };

    // FormData를 문자열로 변환하여 전송
    xhr.send(new URLSearchParams(formData));
  });
});
