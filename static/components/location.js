const transLocation = document.getElementById("transaction_location");
const locationValue = transLocation.innerHTML;

let value = "";
switch (locationValue.trim()) {
  case "ecc":
    value = "ECC";
    break;
  case "asan":
    value = "아산공학관";
    break;
  case "newEng":
    value = "신공학관";
    break;
  case "edu":
    value = "교육관";
    break;
  case "eHouse":
    value = "기숙사(E-house, 한우리)";
    break;
  case "iHouse":
    value = "기숙사(I-house)";
    break;
  case "mainGate":
    value = "정문";
    break;
  case "science":
    value = "종합과학관";
    break;
  case "library":
    value = "중앙도서관";
    break;
  case "art":
    value = "조형예술관";
    break;
  case "posco":
    value = "포스코관";
    break;
  case "student":
    value = "학관";
    break;
  default:
    value = locationValue;
}
transLocation.innerHTML = value;
