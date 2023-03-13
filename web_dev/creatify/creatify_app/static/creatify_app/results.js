// LOADER
window.addEventListener('load', function() {
    var loadingOverlay = document.getElementById('loading-overlay');
    loadingOverlay.style.display = 'none';
  });

  function toggleButtonClass(button) {
    // Remove 'button_active' class from all buttons
    var buttons = document.querySelectorAll('button');
    buttons.forEach(function(btn) {
      btn.classList.remove('button_active');
      btn.classList.add('button');
    });

    //sp.playlist_change_details("5VUcXnkEGvX3AqoVv3CaWL",name = "new name!")
  
    // Add 'button_active' class to clicked button
    button.classList.remove('button');
    button.classList.add('button_active');

    changePlaylistName(button.id,button.textContent);
  }
  function changePlaylistName(id, title) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  const request = new Request('/results/', {
    method: 'POST',
    headers: {'X-CSRFToken': csrftoken},
    mode: 'same-origin',
    body: JSON.stringify({
      'nameChange': true,
      'newName' : title,
      'playlistID': id,
    })    
  });
  fetch(request).then(function(response) {
    if (response.ok) {
      window.location.href = '/results/'; // Replace with the URL of the new page
    } else {
      throw new Error('Network response was not ok.');
    }
  }).catch(function(error) {
    console.log('There was a problem with the fetch operation:', error.message);
  });
  }

  