const goBackIcon = document.getElementsByClassName("base_header__back")[0];

goBackIcon.addEventListener("click", function (event) {
  event.preventDefault(); //기본 링크 동작 중단

  //이전 페이지로 이동
  history.back();
});
