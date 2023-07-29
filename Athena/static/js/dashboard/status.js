// Get all the table cells with the id 'etat'
const cells = document.querySelectorAll('#table td #etat');

// Loop through each cell and change the color to green
cells.forEach(cell => {
  if(cell.innerText == "panding") 
  {
    cell.style.backgroundColor = "rgba(247, 200, 0, 0.1)"
    cell.style.color = "#f7c800"
  }
  else{
    if(cell.innerText == "accepted")
    {
      cell.style.backgroundColor = "rgba(33, 150, 83, 0.1)"
      cell.style.color = "#219653"
    }
  }
});
