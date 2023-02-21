// toggle genres
function toggleButtonClass(button) {
    button.classList.toggle('clicked');
    button.classList.toggle('unclicked');
}
const coll = document.getElementsByClassName("collapsible");
for (let i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
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
// hide desc and grey out slider with checkbox
$('.custom-checkbox').change(function() {
  var sliderId = $(this).attr('id');
  if ($(this).is(':checked')) {
    $('#slider-' + sliderId).removeClass('greyed-out');
    $('#slider-' + sliderId).find('*').removeClass('greyed-out');
  } else {
    $('#slider-' + sliderId).addClass('greyed-out');
    $('#slider-' + sliderId).find('*').addClass('greyed-out');
    $('#desc-' + sliderId).hide();
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
    if (sliderValue == 1) {
      document.getElementById('low-' + event.target.id.split('-')[2]).style.opacity = '.7';
      document.getElementById('low-' + event.target.id.split('-')[2]).style.fontWeight = '600';
    } else if (sliderValue == 2) {
      document.getElementById('medium-' + event.target.id.split('-')[2]).style.opacity = '.8';
      document.getElementById('medium-' + event.target.id.split('-')[2]).style.fontWeight = '700';
    } else {
      document.getElementById('high-' + event.target.id.split('-')[2]).style.opacity = '1';
      document.getElementById('high-' + event.target.id.split('-')[2]).style.fontWeight = '700';
    }
  });
});
//show description
const sliderHeaders = document.querySelectorAll(".slider-name");
sliderHeaders.forEach(header => {
  header.addEventListener("click", () => {
    // Get the slider description div associated with this header
    const descriptionDiv = header.nextElementSibling.nextElementSibling;
    // Toggle the display of the description div
    if (descriptionDiv.style.display === "none") {
      descriptionDiv.style.display = "block";
    } else {
      descriptionDiv.style.display = "none";
    }
  });
});
// send data to view
function send_selections() {
  const genre_buttons = document.querySelectorAll('button.clicked');
  const genres = [];
  genre_buttons.forEach(button => {
    genres.push(button.textContent);
  });
  const slider_values = [];
  $('.slider-wrapper').each(function() {
    let slider_name = $(this).attr('id');
    slider_name = slider_name.substring(7);
    if (!$(this).hasClass('greyed-out')) {
      const slider_value = parseInt($(this).find('input.slider').val())-2;
      slider_values.push({
        'name': slider_name,
        'On': true,
        'Level': slider_value 
      });
    } else {
      slider_values.push({
        'name': slider_name,
        'On': false,
        'Level': 0
      });
    }
  });
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    headers: {'X-CSRFToken': csrftoken},
    url: "/result/",
    data: {
      'genres': JSON.stringify(genres),
      'slider_values': JSON.stringify(slider_values),
      'csrfmiddlewaretoken': csrftoken
    },
  });
}
//add send_select to button
const $generate_button = $('#generate_bt');
$generate_button.click(send_selections);