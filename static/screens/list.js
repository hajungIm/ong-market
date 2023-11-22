const selectPlace = document.getElementById("select_place");
const f2fBtn = document.getElementById("item_option_btn");
const icon = f2fBtn.querySelector("i");
const text = f2fBtn.querySelector("p");

//버튼에 클릭 이벤트 추가, toggleButtonText 함수 실행
f2fBtn.addEventListener("click", toggleButtonText);

//숫자 , 처리를 위한 코드
//문서를 로드할 때 각 상품에 대해 모두 , 처리가 되도록 반복문을 사용한다.
document.addEventListener("DOMContentLoaded", function () {
  //문서가 로드될 때 실행되는 함수
  const priceElements = document.querySelectorAll(".item_box1__price"); //'item_box1__price' 클래스를 가진 모든 요소 선택
  //선택된 각 요소에 대한 반복문 실행
  priceElements.forEach(function (priceElement) {
    // 가격 값 가져오기
    const price = priceElement.textContent || priceElement.innerHTML;
    //가격에 쉼표 추기
    const formattedPrice = addCommasToNumber(price);
    priceElement.textContent = formattedPrice;
    priceElement.innerHTML = formattedPrice;
  });
});

//대면, 비대면 선택에 따라 select 활성화, 비활성화하는 함수
function toggleButtonText() {
  if (text.textContent == "대면") {
    text.textContent = "비대면";
    icon.style.display = "none";
    selectPlace.setAttribute("disabled", "disabled");
  } else {
    text.textContent = "대면";
    icon.style.display = "inline";
    selectPlace.removeAttribute("disabled");
  }
}

//,를 추가하는 함수
function addCommasToNumber(number) {
  return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
