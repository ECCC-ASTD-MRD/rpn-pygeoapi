<?php ?>

<input type="number" id="lat-min" placeholder="Lat Min" step="1" , value="10">
<input type="number" id="lon-min" placeholder="Lon Min" step="1" , value="10">
<input type="number" id="lat-max" placeholder="Lat Max" step="1" , value="12">
<input type="number" id="lon-max" placeholder="Lon Max" step="1" , value="12">

<button id="update-map-btn" onclick=updateMap()>Update Map</button>
<script>

    let latMin = document.getElementById('lat-min').value;
    let lonMin = document.getElementById('lon-min').value;
    let latMax = document.getElementById('lat-max').value;
    let lonMax = document.getElementById('lon-max').value;

    const updateCoords = () => {

        latMin = document.getElementById('lat-min').value;
        lonMin = document.getElementById('lon-min').value;
        latMax = document.getElementById('lat-max').value;
        lonMax = document.getElementById('lon-max').value;

        // const params = new URLSearchParams({
        //     bbox: `${lonMin},${lonMin},${lonMin},${lonMin}`
        // });


    }
    updateCoords();
</script>
