const itemName = document.getElementById("itemName");
const itemPrice = document.getElementById("price");
const itemStatus = document.getElementsByName("status");
const itemDescription = document.getElementById("description");
const itemTrans = document.getElementsByName("transaction");
const itemLocation = document.getElementById("location");
const imgInput = document.getElementById("imgInput");
const form = document.getElementById("itemForm");

form.addEventListener("submit", function (event) {
  if (
    nameCheck() &&
    priceCheck() &&
    statusCheck() &&
    descriptionCheck() &&
    transactionCheck() &&
    itemImgCheck()
  ) {
    // 모든 검사가 통과되면 폼을 제출
  } else {
    // 검사에서 실패하면 폼 제출을 막음
    event.preventDefault();
  }
});

function nameCheck() {
  if (itemName.value.length > 0) {
    return true;
  } else {
    alert("상품 이름을 입력해주세요.");
    return false;
  }
}

function priceCheck() {
  if (itemPrice.value.length > 0) {
    return true;
  } else {
    alert("상품 가격을 입력해주세요.");
    return false;
  }
}

function statusCheck() {
  for (let i = 0; i < itemStatus.length; i++) {
    if (itemStatus[i].checked) {
      return true;
    }
  }
  alert("상품 상태를 선택해주세요.");
  return false;
}

function descriptionCheck() {
  if (itemDescription.value.length >= 10) {
    return true;
  } else {
    alert("상품 설명은 10자 이상이어야 합니다.");
    return false;
  }
}

function transactionCheck() {
  if (itemTrans[0].checked) {
    if (itemLocation.value === "") {
      alert("거래 희망 장소를 선택해주세요.");
      return false;
    }
    return true;
  } else if (itemTrans[1].checked) {
    return true;
  }
  alert("거래 방식을 선택해주세요.");
  return false;
}

function itemImgCheck() {
  if (imgInput.files.length === 0) {
    alert("제품 사진을 선택해주세요.");
    return false;
  } else {
    return true;
  }
}
