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

    changePlaylistName(button.id);
  }
  function changePlaylistName(title) {
    $.ajax({
      url: "{% url 'change_playlist_name' %}",
      method: "POST",
      data: { title: title },
      success: function(response) {
        // Handle success response
      },
      error: function(xhr) {
        // Handle error response
      }
    });
  }

  