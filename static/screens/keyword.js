document.addEventListener("DOMContentLoaded", function() {
  var reviewItems = [
      document.getElementById("time"),
      document.getElementById("detail"),
      document.getElementById("resonable"),
      document.getElementById("kind"),
      document.getElementById("condition"),
      document.getElementById("response"),
      document.getElementById("give"),
      document.getElementById("come")
  ];

  var reviewClass = [
      document.querySelector(".green_0"),
      document.querySelector(".green_1"),
      document.querySelector(".green_2"),
      document.querySelector(".green_3"),
      document.querySelector(".green_4"),
      document.querySelector(".green_5"),
      document.querySelector(".green_6"),
      document.querySelector(".green_7")
  ];

  // 'keyword_num'에서 숫자 값을 가져옵니다.
  var keywordNumElement = document.querySelector('.total_review_number');
  console.log('keywordNumElement:', keywordNumElement); // 추가된 부분
  var keywordNumText = keywordNumElement.textContent.trim();
  var totalNumber = parseInt(keywordNumText.match(/\d+/)[0], 10);

  // Loop through each review item
  for (var i = 0; i < reviewItems.length; i++) {
    // Check if the reviewClass element exists
    if (reviewClass[i]) {
      // Get the numeric value from the review item
      var reviewValue = parseInt(reviewItems[i].textContent, 10);

      // Check if the reviewValue is a valid number
      if (isNaN(reviewValue)) {
        console.error("Invalid numeric value for review item", i, ":", reviewItems[i].textContent.trim());
        continue; // Skip to the next iteration if the value is not a number
      }

      // Calculate the opacity ratio
      var opacityRatio = reviewValue / totalNumber;

      // Log the values for debugging
      console.log('Review Item', i, ':', reviewItems[i].textContent.trim(), 'Review Value:', reviewValue, 'Total Number:', totalNumber, 'Opacity Ratio:', opacityRatio);

      // Set the background-color opacity of the corresponding reviewClass
      reviewClass[i].style.backgroundColor = `rgba(76, 217, 100, ${opacityRatio})`;
      reviewClass[i].style.width = opacityRatio * 100 + '%';
    }
  }
});