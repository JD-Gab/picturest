//JS For the sign up password validation
const password_repeat = (event) => {
        const password = document.getElementById('pass').value;
        const password2 = document.getElementById('re_pass').value;

        if (password !== password2) {
            password2.setCustomValidity("Passwords don't match");
        } else {
            password2.setCustomValidity('');
        }
    }


/* ***************************************************************************** */
// Edit button in the modal functionality to be shown/hidden
let editButtons = document.querySelectorAll('.editImageButton');
editButtons.forEach(button => {
    button.addEventListener('click', event => {

        const modal = button.closest('.modal');

        const showDiv = modal.querySelector('.hiddenEditOptions');
        showDiv.style.display = 'block';

        //Next line of codes are for the preview images found on the modal

        var output = modal.querySelector('.blah');
        if (output.src == ""){
        output.style.display = 'none';
        }
        
        imagePreviewClass = modal.querySelector('.imagePreviewClass');
        imagePreviewClass.addEventListener('change', event => {

        output.style.display = 'block';
        output.src = URL.createObjectURL(event.target.files[0]);
        output.onload = function() {
        URL.revokeObjectURL(output.src)
        }
        });


    });
});


/* ***************************************************************************** */
//Script to make alert disappear after 8 seconds
alertDiv = document.querySelector('.alert');
if (alertDiv){
setTimeout(() => {
    alertDiv.style.display = 'none';
}, 8000);
}

/* ***************************************************************************** */
//script for submitting the profile change form from the button outside of the form
try {
const profilebutton = document.querySelector('.transition-btn');
if (profilebutton) {
    profilebutton.addEventListener('click', function() {
    const profileForm = document.getElementById('profile-pic-form');
    profileForm.submit();
    });
}

} catch (error){
  //console.log(error);
}


/******************************************************************************** */
try {
    const textarea = document.getElementById('descriptionInput');
    const counter_text = document.querySelector('.count-text');
    if (textarea){
        textarea.addEventListener('input', function() {
            if(parseInt(textarea.value.length) >= 900){
                counter_text.textContent = 900;
            }
            counter_text.textContent = textarea.value.length;
        });
    }
        
}
catch(error){

}