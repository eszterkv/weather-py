window.onload = () => {
  const locationChooser = document.querySelector('#locationChooser');
  locationChooser.onkeypress = (key) => {
    if (key.which == 13) {
      locationChooserForm.submit();
    }
  }
}
