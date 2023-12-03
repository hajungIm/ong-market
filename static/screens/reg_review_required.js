const reviewTitle = document.getElementById("review_title");
const imgInput = document.getElementById("review_imgInput");
const form = document.getElementById("reviewForm");

//별점
const stars = document.getElementsByName("rating");

form.addEventListener("submit", function (event) {
  if (starCheck() && keywordCheck() && titleCheck() && reviewImgCheck()) {
    // 모든 검사가 통과되면 폼을 제출
  } else {
    // 검사에서 실패하면 폼 제출을 막음
    event.preventDefault();
  }
});

function starCheck() {
  for (let i = 0; i < stars.length; i++) {
    if (stars[i].checked) {
      return true;
    }
  }
  alert("별점을 선택해주세요.");
  return false;
}

function titleCheck() {
  if (reviewTitle.value.length > 0) {
    return true;
  } else {
    alert("리뷰 제목을 입력해주세요.");
    return false;
  }
}

function reviewImgCheck() {
  if (imgInput.files.length === 0) {
    alert("리뷰 사진을 선택해주세요.");
    return false;
  } else {
    return true;
  }
}

function keywordCheck() {
  // Check if at least one checkbox is selected in the "어떤 점이 좋았나요?" section
  const checkboxes = document.querySelectorAll(
    ".checkbox_keyword:not(#no_keyword):checked"
  );
  const noKeywordCheckbox = document.querySelector(
    'input[name="keywordNo"]:checked'
  );

  if (checkboxes.length === 0 && !noKeywordCheckbox) {
    alert(
      "키워드를 최소 하나 이상 선택해주세요.\n선택할 키워드가 없다면 '키워드 없음'을 눌러 주세요."
    );
    return false;
  }

  // Continue with form submission or other actions if needed
  else {
    return true;
  }
}
