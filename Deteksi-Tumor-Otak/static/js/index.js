// const dropArea = document.querySelector(".drop-box"),
//   input = dropArea.querySelector("input"),
//   dragText = dropArea.querySelector("h4");

// let file;

// // Handle click to trigger file input
// dropArea.addEventListener("click", () => {
//   input.click();
// });

// // Handle dragover event
// dropArea.addEventListener("dragover", (e) => {
//   e.preventDefault(); // Prevent default behavior
//   dropArea.classList.add("active");
//   dragText.textContent = "Release to Upload File";
// });

// // Handle dragleave event
// dropArea.addEventListener("dragleave", () => {
//   dropArea.classList.remove("active");
//   dragText.textContent = "Select File here";
// });

// // Handle drop event
// dropArea.addEventListener("drop", (e) => {
//   e.preventDefault(); // Prevent default behavior
//   dropArea.classList.remove("active");
//   dragText.textContent = "Select File here";

//   file = e.dataTransfer.files[0]; // Get the first dropped file
//   handleFile(file);
// });

// // Handle file input (if user clicks the box and selects a file)
// input.addEventListener("change", function () {
//   file = this.files[0]; // Get the selected file
//   handleFile(file);
// });

// // Validate file and show preview
// function handleFile(file) {
//   const validExtensions = ["image/jpeg", "image/jpg", "image/png"];
//   if (file && validExtensions.includes(file.type)) {
//     showFile(file); // Display file preview and handle upload
//   } else {
//     alert("Invalid file type. Please upload an image (JPG, JPEG, PNG).");
//   }
// }

// // Display file and show preview
// function showFile(file) {
//   const fileReader = new FileReader();
//   fileReader.onload = function (e) {
//     const imgElement = document.createElement("img");
//     imgElement.src = e.target.result;
//     imgElement.alt = "Uploaded Preview";
//     imgElement.style.maxWidth = "100%";
//     imgElement.style.height = "auto";

//     // Clear the drop box and display the image
//     dropArea.innerHTML = ""; // Clear existing content
//     dropArea.appendChild(imgElement);
//   };
//   fileReader.readAsDataURL(file);
// }

const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("fileID");
const imageView = document.getElementById("img-view");

inputFile.addEventListener("change", uploadImage);

function uploadImage() {
  if (inputFile.files && inputFile.files[0]) {
    let imgLink = URL.createObjectURL(inputFile.files[0]);
    imageView.style.backgroundImage = `url(${imgLink})`;
    imageView.textContent = "";
    imageView.style.border = "none";
    imageView.querySelector("img").style.display = "none"; // Menyembunyikan ikon input default
    imageView.querySelector("p").style.display = "none"; // Menyembunyikan teks deskripsi
    imageView.querySelector("span").style.display = "none"; // Menyembunyikan file supported info
  }
}

dropArea.addEventListener("dragover", function (e) {
  e.preventDefault();
});
dropArea.addEventListener("drop", function (e) {
  e.preventDefault();
  inputFile.files = e.dataTransfer.files;
  uploadImage();
});
