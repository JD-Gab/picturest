/* ***************************************************************************** */
//Script for displaying the preview of profile picture and banner in the edit-profile section
//plus the script for disabling and enabling the submit button
try {
const output = document.querySelector('.profile-pic-edit');
      const imagePreviewClass = document.querySelector('.profile-pic-input');
      let ischanged = false;

      imagePreviewClass.addEventListener('change', event => {
        const file = event.target.files[0];
        if (file) {

          output.src = URL.createObjectURL(file);
          output.onload = () => {
            URL.revokeObjectURL(output.src);
          };
          
          ischanged = true;
          checkChanges(ischanged);
        } else {
          ischanged = false;
          checkChanges(ischanged);
        }
      }); //End codeblock for checking if profile picture is changed/updated 

      var bannerOutput = document.querySelector('.banner-edit');
      var bannerInput = document.querySelector('#banner_picture');
      bannerInput.addEventListener('change', event => {

        ischanged = true;
        checkChanges(ischanged);
        let banner = document.querySelector('.banner_image');
        banner.files = bannerInput.files;
        bannerOutput.src = URL.createObjectURL(event.target.files[0]);
        bannerOutput.onload = function() {
        URL.revokeObjectURL(bannerOutput.src)
      }
      }); //End codeblock for checking if banner picture is changed/updated

      //Code for checking if changes is true or not, enable the save button
      function checkChanges(ischanged) {
        if (!ischanged) return; // If no changes, do nothing
        const profilebutton = document.querySelector('.transition-btn');
        profilebutton.classList.replace('btn-secondary','btn-main'); // Show the button
        profilebutton.disabled = false; // Enable the button
      }
} catch (error) {
    //console.log(error);
}