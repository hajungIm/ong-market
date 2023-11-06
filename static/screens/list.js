const selectPlace = document.getElementById("select_place");
const f2fBtn = document.getElementById("item_option_btn");
const icon = f2fBtn.querySelector("i");
const text = f2fBtn.querySelector("p");
const currentPageIcon = document.getElementById("nav_list").firstChild;

currentPageIcon.style.color = "#242424";

function toogleButtonText() {
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

f2fBtn.addEventListener("click", toogleButtonText);
