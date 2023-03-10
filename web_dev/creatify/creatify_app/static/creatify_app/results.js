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
  
    // Add 'button_active' class to clicked button
    button.classList.remove('button');
    button.classList.add('button_active');
  }
  