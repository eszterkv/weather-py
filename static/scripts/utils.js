window.onload = () => {
  // navigator.geolocation && navigator.geolocation.getCurrentPosition((pos) =>
  //   console.log(pos.coords.latitude, pos.coords.longitude)
  // );
  // locationDetector.submit();

  const locationChooser = document.querySelector('#locationChooser');
  locationChooser.onkeypress = (key) => {
    if (key.which == 13) {
      locationChooserForm.submit();
    }
  }
}
