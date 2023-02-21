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
const slider = document.querySelector('.slider');
const dots = document.querySelectorAll('.dot');
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
    $('#slider-' + sliderId).removeClass('greyed-out');
    $('#slider-' + sliderId).find('*').removeClass('greyed-out');
  } else {
    $('#slider-' + sliderId).addClass('greyed-out');
    $('#slider-' + sliderId).find('*').addClass('greyed-out');
  }
});
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
const $myButton = $('#generate_bt');
$myButton.click(send_selections);
document.querySelectorAll('.slider').forEach(function(sliderInput) {
  sliderInput.addEventListener('input', function(event) {
    // get the slider value
    const sliderValue = event.target.value;
    document.getElementById('low-' + event.target.id.split('-')[2]).style.opacity = '.4';
    document.getElementById('medium-' + event.target.id.split('-')[2]).style.opacity = '.4';
    document.getElementById('high-' + event.target.id.split('-')[2]).style.opacity = '.4';
    // show the span element corresponding to the slider value
    if (sliderValue == 1) {
      document.getElementById('low-' + event.target.id.split('-')[2]).style.opacity = '.7';
    } else if (sliderValue == 2) {
      document.getElementById('medium-' + event.target.id.split('-')[2]).style.opacity = '.8';
    } else {
      document.getElementById('high-' + event.target.id.split('-')[2]).style.opacity = '1';
    }
  });
});