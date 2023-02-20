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

//settings = [{"Name": "danceability", "On": True, "Level": 1},
// {"Name": "energy", "On": True,"Level": -1},
// {"Name": "loudness","On": True, "Level": 1},
// {"Name": "instrumentalness","On": True, "Level": -1},
// {"Name": "liveness", "On": False,"Level": 1}]
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
  console.log(genres);
  console.log(slider_values);
  // $.ajax({
  //   type: "POST",
  //   url: "/path/to/view/",
  //   data: {
  //     'genres': genres,
  //     'slider_values': slider_values
  //   },
  //   success: function(data) {
  //     // Do something with the response from the server
  //   }
  // });
}

const $myButton = $('#generate_bt');
$myButton.click(send_selections);

