// toggle genres
function toggleButtonClass_cta(button) {
  button.classList.toggle('cta');
  button.classList.toggle('cta_active');
}
const coll = document.getElementsByClassName("cta");
for (let i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("cta_active");
    let content = this.nextElementSibling;
    if (content.style.maxHeight != content.scrollHeight + "px"){
      content.style.maxHeight = content.scrollHeight + "px";
    } else {
      content.style.maxHeight = "0px";
    } 
  });
}
//genre filter from text input
const filterInput = document.querySelector('#genre-filter');
const genreTable = document.querySelector('#genre-table');
const genreButtons = genreTable.querySelectorAll('button');
const resetButton = document.querySelector('.reset');

filterInput.addEventListener('input', () => {
  const filterText = filterInput.value.toLowerCase();

  genreButtons.forEach(button => {
    const genre = button.dataset.genre.toLowerCase();
    const td = button.parentNode;
    if (button.classList.contains('active')) {
      return false;
    }
    if (!genre.includes(filterText)) {
      td.style.display = 'none';
    } else {
      td.style.display = '';
    }
  });
});

resetButton.addEventListener('click', () => {
  filterInput.value = '';
  genreButtons.forEach(button => {
    const td = button.parentNode;
    td.style.display = '';
  });
});


// LOADER
window.addEventListener('load', function() {
  var loadingOverlay = document.getElementById('loading-overlay');
  loadingOverlay.style.display = 'none';
});



// BUTTON WORK
const genre_buttons = document.querySelectorAll('.btn');
const newButton = document.querySelector('#new-btn');
const genre_table = document.querySelector('#genre-table');
let hideButtons = true;
newButton.addEventListener('click', () => {
  genre_buttons.forEach(button => {
    if (!button.classList.contains('active')) { //active
      button.parentElement.style.display = hideButtons ? 'none' : '';
    }
  });
  hideButtons = !hideButtons;
  newButton.firstElementChild.textContent = hideButtons ? 'Collapse Unused Genres' : 'Expand All Genres';
  newButton.lastElementChild.classList.toggle('rotated');
  if (hideButtons) {
    genre_table.style.display = 'block';
  } else {
    genre_table.style.display = 'flex';
  }
});
genre_buttons.forEach(button => {
  button.addEventListener('click', () => {
    button.classList.toggle('active');
    genre_table.style.display = 'flex';
  });
});
// hide desc and grey out slider with checkbox
$("input:checkbox").change(function() {
  var sliderId = $(this).attr('id');
  if ($(this).is(':checked')) {
    $('#slider-' + sliderId).removeClass('greyed-out');
    $('#slider-' + sliderId).find('*').removeClass('greyed-out');
  } else {
    $('#slider-' + sliderId).addClass('greyed-out');
    $('#slider-' + sliderId).find('*').addClass('greyed-out');
  }
});
// opacity and font weight depending on slider position/value
document.querySelectorAll('.slider').forEach(function(sliderInput) {
  sliderInput.addEventListener('input', function(event) {
    // get the slider value
    const sliderValue = event.target.value;
    document.getElementById('low-' + event.target.id.split('-')[2]).style.opacity = '.4';
    document.getElementById('medium-' + event.target.id.split('-')[2]).style.opacity = '.4';
    document.getElementById('high-' + event.target.id.split('-')[2]).style.opacity = '.4';
    document.getElementById('low-' + event.target.id.split('-')[2]).style.fontWeight = '400';
    document.getElementById('medium-' + event.target.id.split('-')[2]).style.fontWeight = '400';
    document.getElementById('high-' + event.target.id.split('-')[2]).style.fontWeight = '400';
    
    // show the span element corresponding to the slider value
    if (sliderValue < 25) {
      document.getElementById('low-' + event.target.id.split('-')[2]).style.opacity = '.7';
      document.getElementById('low-' + event.target.id.split('-')[2]).style.fontWeight = '600';
    } else if (sliderValue > 75) {
      document.getElementById('high-' + event.target.id.split('-')[2]).style.opacity = '1';
      document.getElementById('high-' + event.target.id.split('-')[2]).style.fontWeight = '700';
    } else {
      document.getElementById('medium-' + event.target.id.split('-')[2]).style.opacity = '.8';
      document.getElementById('medium-' + event.target.id.split('-')[2]).style.fontWeight = '700';
    }
  });
});
// send data to view
function send_selections() {
  const genre_buttons = document.querySelectorAll('.btn.active');
  const genres = [];
  genre_buttons.forEach(button => {
    genres.push(button.textContent);
  });
  if (genres.length < 3) {
    alert('Please select at least three genres.');
    return;
  }
  const slider_values = [];
  $('.slider-wrapper').each(function() {
    let slider_name = $(this).attr('id');
    slider_name = slider_name.substring(7);
    if (!$(this).hasClass('greyed-out')) {
      const slider_value = parseInt($(this).find('input.slider').val());
      slider_values.push({
        'Name': slider_name,
        'On': true,
        'Level': slider_value 
      });
    } else {
      slider_values.push({
        'Name': slider_name,
        'On': false,
        'Level': 0
      });
    }
  });
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  const number_of_songs = $("#goal").val();
  const request = new Request('/results/', {
    method: 'POST',
    headers: {'X-CSRFToken': csrftoken},
    mode: 'same-origin',
    body: JSON.stringify({
      'nameChange':false,
      'genres': genres,
      'slider_values': slider_values,
      'goal': number_of_songs
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

//add send_select to button
const $generate_button = $('#iloveowen');
$generate_button.click(send_selections);

// button wrapping
function arrangeButtons() {
  const table = document.getElementById('genre-table');
  const container = document.getElementById('genre-table-container');
  let row = table.insertRow();
  let currentRowWidth = 0;
  
  Array.from(table.getElementsByTagName('td')).forEach((td, index) => {
    row.appendChild(td);
    currentRowWidth += td.offsetWidth;
    
    if (currentRowWidth > container.offsetWidth) {
      row.removeChild(td);
      row = table.insertRow();
      row.appendChild(td);
      currentRowWidth = td.offsetWidth;
    }
  });
}

window.addEventListener('load', arrangeButtons);
window.addEventListener('resize', arrangeButtons);

//input coeherce to numbers
function isNumeric(evt) {
  var charCode = (evt.which) ? evt.which : event.keyCode;
  if (charCode > 31 && (charCode < 48 || charCode > 57)) {
    return false;
  }
  return true;
}