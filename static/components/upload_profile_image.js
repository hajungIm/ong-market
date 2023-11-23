//수정 예정

document
  .getElementById("profileImgInput")
  .addEventListener("change", handleFileSelect);
document
  .querySelector(".photo_btn")
  .addEventListener("click", triggerFileInput);

function triggerFileInput() {
  document.getElementById("profileImgInput").click();
}

function handleFileSelect(event) {
  const fileInput = event.target;
  const file = fileInput.files[0];

  if (file) {
    const formData = new FormData();
    formData.append("profileImage", file);

    fetch("/upload_profile_image", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("File upload success:", data);
      })
      .catch((error) => {
        console.error("File upload error:", error);
      });
  }
}
