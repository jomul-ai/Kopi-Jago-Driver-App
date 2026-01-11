function getLocation() {
    fn.value = driverName.value;
    fs.value = start.value;
    fe.value = end.value;
    navigator.geolocation.getCurrentPosition(p => {
        lat.value = p.coords.latitude;
        lon.value = p.coords.longitude;
        f.submit();
    });
}