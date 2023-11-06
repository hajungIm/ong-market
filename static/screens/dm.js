const button = document.getElementById("dm__plus_btn");
const functionMenu = document.getElementById("dm_function__menu");

function rotateButton() {
  // 현재 클래스를 확인하고 클래스를 추가 또는 제거
  if (button.classList.contains("rotate-45")) {
    button.classList.remove("rotate-45");
    functionMenu.style.visibility = "hidden";
    functionMenu.style.height = "0px";
  } else {
    button.classList.add("rotate-45");
    functionMenu.style.visibility = "visible";
    functionMenu.style.height = "250px";
  }
}

button.addEventListener("click", rotateButton);

//   // 현재 회전 각도를 가져온 후 90도씩 회전
//   const currentRotation = button.style.transform || "rotate(0deg)";
//   const currentDegree = parseInt(currentRotation.match(/\d+/));
//   const newDegree = (currentDegree + 90) % 360;

//   // 회전 각도를 적용
//   button.style.transform = `rotate(${newDegree}deg)`;
