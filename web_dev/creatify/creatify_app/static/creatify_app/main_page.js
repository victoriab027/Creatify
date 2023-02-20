function toggleButtonClass(button) {
    button.classList.toggle('clicked');
    button.classList.toggle('unclicked');
  }
  const coll = document.getElementsByClassName("collapsible");
  
  for (let i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
      this.classList.toggle("active");
      var content = this.nextElementSibling;
      if (content.style.maxHeight){
        content.style.maxHeight = null;
      } else {
        content.style.maxHeight = content.scrollHeight + "px";
      }
    });
  }
  const filterInput = document.querySelector('#genre-filter');
  const genreTable = document.querySelector('#genre-table');
  const genreButtons = genreTable.querySelectorAll('button');
  
  filterInput.addEventListener('input', () => {
    const filterText = filterInput.value.toLowerCase();
  
    genreButtons.forEach(button => {
      const genre = button.dataset.genre.toLowerCase();
      const td = button.parentNode;
      if (button.classList.contains('clicked')) {
        return false;
      }
      if (!genre.includes(filterText)) {
        td.style.display = 'none';
      } else {
        td.style.display = '';
      }
    });
  });

// Get the slider element
const slider = document.querySelector('.slider');

// Get the dots elements
const dots = document.querySelectorAll('.dot');
// Loop through each dot
dots.forEach(dot => {
  // Get the value of the dot
  const value = dot.id.split(' ')[0];
  // Add an event listener to the slider
  slider.addEventListener('input', () => {
    // If the slider value matches the dot value, hide the dot, else show it
    if (slider.value === value) {
      dot.style.display = 'none';
    } else {
      dot.style.display = 'block';
    }
  });
});
$('.custom-checkbox').change(function() {
  var sliderId = $(this).attr('id');
  if ($(this).is(':checked')) {
    $('#slider-' + sliderId).show();
  } else {
    $('#slider-' + sliderId).hide();
  }
});
