const maxMessageLength = 37; // 예시로 길이 20으로 설정
const messageTexts = document.querySelectorAll(".maxLength");

document.addEventListener("DOMContentLoaded", function () {
  messageTexts.forEach((messageText) => {
    console.log(messageText.textContent.length);
    messageText.textContent = messageText.textContent.trim();
    if (messageText.textContent.length > maxMessageLength) {
      messageText.textContent =
        messageText.textContent.substring(0, maxMessageLength) + "...";
    }
  });
});
