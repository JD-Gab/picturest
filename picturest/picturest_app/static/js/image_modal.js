/* ***************************************************************************** */
//main script for activating image modals and displaying the data through fetch/get

document.querySelector('.container-fluid-pin').addEventListener('click', event => {
    const modalTrigger = event.target.closest('.activate-modal');

    if (modalTrigger) {
    let picturest_modal1 = document.querySelector('.picturest-modal');
    let img_data = modalTrigger.getAttribute('data-img');


    fetch(`/get-img-data/?id=${img_data}`)
    .then(res => res.json())
    .then(data => {
    
    let request_user = picturest_modal1.querySelector('.modal-body').dataset.username;
    if (data.uploader === request_user){
        picturest_modal1.querySelector('.show-edit').style.display = 'block';
        picturest_modal1.querySelector('.show-delete').style.display = 'block';
    }
    else {
        picturest_modal1.querySelector('.show-edit').style.display = 'none';
        picturest_modal1.querySelector('.show-delete').style.display = 'none';
        picturest_modal1.querySelector('.hiddenEditOptions').style.display = 'none';
    }

    picturest_modal1.querySelector('.modal-user-profile-picture').src = data.uploader_profile_picture ? data.uploader_profile_picture : url_default_avatar;
    picturest_modal1.querySelector('.modal-user-profile-picture').alt = data.uploader;
    picturest_modal1.querySelector('.modal-header a').href = `/user-profile/${data.uploader}/`;
    picturest_modal1.querySelector('.modal-title').textContent = data.uploader;
    picturest_modal1.querySelector('.modal-description').textContent = data.description;
    picturest_modal1.querySelector('.image-main').src = `${data.image}`;
    picturest_modal1.querySelector('.modal-body h3').innerText = data.title;
    picturest_modal1.querySelector('.modal-body p').innerText = `Uploaded at: ${data.upload_date}`;
    picturest_modal1.querySelector('.modal-form').action = `/image-edit/${data.id}/`;
    picturest_modal1.querySelector('.titlefile').value = data.title;
    picturest_modal1.querySelector('.titlefile').placeholder = data.title;
    picturest_modal1.querySelector('.newdescription').value = data.description;
    picturest_modal1.querySelector('.blah').src = data.image;

    document.getElementById('deleteform').action = `/image-delete/${data.id}/`;

    });

    

        } //endblock of if(modalTrigger)
        
});