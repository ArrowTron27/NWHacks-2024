// document.addEventListener("DOMContentLoaded", function() {
//     console.log("Script loaded and started")

//     var submitBtn = document.getElementById("submit-btn");
//     console.log("Submit button:", submitBtn);

//     var uploadForm = document.getElementById("upload-form");
//     console.log("Upload form:", uploadForm);  // Check if the form is found

//     document.getElementById("upload-form").addEventListener("submit", function(event) {
//         event.preventDefault();  // Prevent default form submission

//         console.log("Form submitted!");

//         // Your custom code here...

//         // Example: Simulate asynchronous behavior with a setTimeout
//         setTimeout(function() {
//             console.log("Async code executed");

//         }, 1000);  // Adjust the delay as needed
//     });


//     uploadForm.addEventListener("submit", function(event) {
//         console.log("hello");
//         submitBtn.disabled = true;
//         submitBtn.value = "Uploading...";
//     });
// });