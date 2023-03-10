// Get all the note div elements
const notes = document.querySelectorAll('.note');

// Calculate the number of notes and the midpoint
const numNotes = notes.length;
const midPoint = Math.floor(numNotes / 2);

// Loop through each note element and assign random top, left and animation durations
notes.forEach((note, index) => {
  const randomTop = Math.floor(Math.random() * (window.innerHeight-50));
  let randomLeft;

  if (index < midPoint) {
    randomLeft = Math.floor(Math.random() * (window.innerWidth * 0.3));
  } else {
    randomLeft = Math.floor(Math.random() * (window.innerWidth * 0.3)) + (window.innerWidth * 0.6);
  }

  const randomDuration = Math.floor(Math.random() * 10) + 2; // Random duration between 2 and 11 seconds

  note.style.top = `${randomTop}px`;
  note.style.left = `${randomLeft}px`;
  note.style.animationDuration = `${randomDuration}s`;
});
