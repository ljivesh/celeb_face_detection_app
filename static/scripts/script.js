document.getElementById('imageInput').addEventListener('change', previewImage);

function previewImage() {
  const fileInput = document.getElementById('imageInput');
  const file = fileInput.files[0];
  const validImageTypes = ['image/jpeg', 'image/png', 'image/gif'];

  if (file && validImageTypes.includes(file.type)) {
    const blobURL = URL.createObjectURL(file);

    const imageContainer = document.querySelector('.image-container');
    if (imageContainer) {
      const img = imageContainer.querySelector('img');
      img.src = blobURL;
      imageContainer.style.display = 'block';
    } else {
      const newImageContainer = document.createElement('div');
      newImageContainer.classList.add('image-container');
      const img = document.createElement('img');
      img.src = blobURL;
      img.alt = 'Selected Image';
      newImageContainer.appendChild(img);

      const uploadContainer = document.querySelector('.upload-container');
      uploadContainer.insertAdjacentElement('afterend', newImageContainer);
      newImageContainer.style.display = 'block';
    }
  } else {
    alert('Please upload a valid image file (JPEG, PNG, GIF).');
    const imageContainer = document.querySelector('.image-container');
    if (imageContainer) {
      imageContainer.style.display = 'none';
    }
  }
}

function uploadImage() {
  const fileInput = document.getElementById('imageInput');
  const file = fileInput.files[0];

  if (file) {
    const formData = new FormData();
    formData.append('file', file);

    fetch('/recognize-celebrity', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => displayCelebrityInfo(data))
    .catch(error => console.error(error));
  } else {
    alert('Please select an image to upload.');
  }
}

function displayCelebrityInfo(celebrityData) {
  const infoContainer = document.getElementById('infoContainer');
  const celebrityImage = document.getElementById('celebrityImage');
  const celebrityName = document.getElementById('celebrityName');
  const extract = document.getElementById('extract');

  celebrityImage.src = celebrityData.image;
  celebrityName.textContent = celebrityData.name;
  extract.textContent = celebrityData.extract;

  infoContainer.style.display = 'block';
}
