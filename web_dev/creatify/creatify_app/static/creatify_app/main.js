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