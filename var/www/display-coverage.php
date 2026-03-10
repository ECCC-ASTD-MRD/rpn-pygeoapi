<?php
header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
header("Cache-Control: post-check=0, pre-check=0", false);
header("Pragma: no-cache");

$title = "Visualisation Données Zarr";
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>
        <?= $title ?>
    </title>

    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
        integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
        integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

    <!-- Sidebar control panel -->
    <link rel="stylesheet" href="./assets/css/style.css" />
    <script type="text/javascript" src="https://livejs.com/live.js"></script>

    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: sans-serif;
            background: #222;
            color: #fff;
        }

        h1 {
            padding: 10px;
            margin: 0;
            font-size: 1.2rem;
            text-align: center;
            background: #333;
        }

        #map {
            height: 90vh;
            width: 100%;
        }

        #debug {
            position: absolute;
            bottom: 10px;
            left: 10px;
            z-index: 1000;
            background: rgba(0, 0, 0, 0.7);
            padding: 5px;
            font-size: 0.8rem;
            pointer-events: none;
        }

        .active {
            width: 50px;
            overflow: scroll;
            padding: 10px;
        }
    </style>
</head>

<body>
    <h1>
        <?= $title ?> - <span id="status" style="color: orange;">Chargement...</span>
    </h1>

    <!-- ############ SIDEBAR CONTROL PANEL STARTS HERE ############ -->
    <div id="control-panel" class="sidebar">
        <button style="position:absolute; top:0; right:0;margin:10px;" id="toggle-btn"
            onclick="toggleSidebar()">–</button>
        <script>
            const toggleBtn = document.getElementById('toggle-btn');
            const controlPanel = document.getElementById('control-panel');
            toggleBtn.addEventListener('click', () => {
                controlPanel.classList.toggle('active');
            });
        </script>
        <?php include __DIR__ . '/control-panel.php'; ?>

    </div>

    <!-- ############ SIDEBAR CONTROL PANEL ENDS HERE ############ -->

    <div id="map"></div>
    <div id="debug">En attente de données...</div>

    <script>


        const map = L.map('map').setView([0, 180], 2)

        // L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        //     attribution: '&copy; <a href="https://www.openstreetgorg/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        //     subdomains: 'abcd',
        //     maxZoom: 19
        // }).addTo(map);

        // L.tileLayer.wms('https://geo.weather.gc.ca/geomet?', { 
        //     layers: 'GDPS.ETA_TT', 
        //     version: '1.3.0', 
        //     opacity: 0.5, 
        // }).addTo(map);

        async function updateMap() {
            await updateCoords();
            await loadAndDrawLayer(lonMin, latMin, lonMax, latMax)
        };

        async function updateLayer(canvas = null, lonMin = 0, latMin = -90, lonMax = 360, latMax = 90) {
            let DATA_URL = `http://localhost:5000/collections/public-zarr/coverage?f=json&properties=10m_u_component_of_wind&datetime=2020-01-01T00:00:00/2020-01-01T00:00:00&bbox=${lonMin},${latMin},${lonMax},${latMax}`;

            console.log(DATA_URL);


            const statusElem = document.getElementById('status');
            const debugElem = document.getElementById('debug');

            try {
                debugElem.innerText = "Fetch en cours vers " + DATA_URL;
                const response = await fetch(DATA_URL);

                if (!response.ok) throw new Error(`Erreur HTTP: ${response.status}`);

                const data = await response.json();

                debugElem.innerText = "Données reçues. Traitement...";
                console.log("Données Zarr reçues:", data);

                const varName = '10m_u_component_of_wind';

                if (!data.ranges || !data.ranges[varName]) {
                    throw new Error("Structure JSON inattendue : clé 'ranges' ou variable manquante.");
                }

                const values = data.ranges[varName].values;
                const axes = data.domain.axes;

                const width = axes.x.num;
                const height = axes.y.num;

                const minLon = Math.min(axes.x.start, axes.x.stop);
                const maxLon = Math.max(axes.x.start, axes.x.stop);
                const minLat = Math.min(axes.y.start, axes.y.stop);
                const maxLat = Math.max(axes.y.start, axes.y.stop);

                msgCoords = document.createElement("p");
                msgCoords.innerText = `Étendue des données [minLon, maxLon, minLat, maxLat] : ${minLon}, ${maxLon}, ${minLat}, ${maxLat}`;
                console.log(msgCoords);
                controlPanel.appendChild(msgCoords);

                console.log(minLon, maxLon, minLat, maxLat);
                console.log(width, height);

                console.log(canvas);

                const imgData = ctx.createImageData(width, height);

                let minVal = -18.02; // Valeur min approximative pour l'échelle de couleur
                let maxVal = 18.86;  // Valeur max approximative

                const isLatDescending = axes.y.start > axes.y.stop;

                for (let y = 0; y < height; y++) {
                    for (let x = 0; x < width; x++) {
                        const dataIndex = y * width + x;
                        const val = values[dataIndex];

                        let normalized = (val - minVal) / (maxVal - minVal);
                        normalized = Math.max(0, Math.min(1, normalized))

                        const r = Math.floor(30 + normalized * 210);
                        const g = Math.floor(144 + (104 * normalized));
                        const b = 255;
                        const alpha = 180;

                        const canvasY = isLatDescending ? y : (height - 1) - y;
                        const index = (canvasY * width + x) * 4;

                        imgData.data[index] = r;     // R
                        imgData.data[index + 1] = g; // G
                        imgData.data[index + 2] = b; // B
                        imgData.data[index + 3] = alpha; // Alpha
                    }
                }
                console.log(map);
                map.eachLayer((layer) => {
                    if (layer instanceof L.imageOverlay)
                        map.removeLayer(layer);
                });
                ctx.putImageData(imgData, 0, 0);

                const imageUrl = canvas.toDataURL();

                const imageBounds = [[minLat, minLon], [maxLat, maxLon]];

                L.imageOverlay(imageUrl, imageBounds, { opacity: 0.8 }).addTo(map);

                statusElem.innerText = "Chargé !";
                statusElem.style.color = "#4caf50";
                debugElem.innerText = "Layer ajouté avec succès.";

            } catch (error) {
                console.error(error);
                statusElem.innerText = "Erreur";
                statusElem.style.color = "red";
                debugElem.innerText = "Erreur: " + error.message;
            }
        }


        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        let windLayer = null;

        async function loadAndDrawLayer(lonMin = 0, latMin = -90, lonMax = 360, latMax = 90) {
            let DATA_URL = `http://localhost:5000/collections/public-zarr/coverage?f=json&properties=10m_u_component_of_wind&datetime=2020-01-01T00:00:00/2020-01-01T00:00:00&bbox=${lonMin},${latMin},${lonMax},${latMax}`;

            console.log(DATA_URL);

            if (windLayer) {
                map.removeLayer(windLayer);
            }

            const statusElem = document.getElementById('status');
            const debugElem = document.getElementById('debug');

            try {
                debugElem.innerText = "Fetch en cours vers " + DATA_URL;
                const response = await fetch(DATA_URL);

                if (!response.ok) throw new Error(`Erreur HTTP: ${response.status}`);

                const data = await response.json();
                debugElem.innerText = "Données reçues. Traitement...";
                console.log("Données Zarr reçues:", data);

                const varName = '10m_u_component_of_wind';

                if (!data.ranges || !data.ranges[varName]) {
                    throw new Error("Structure JSON inattendue : clé 'ranges' ou variable manquante.");
                }

                const values = data.ranges[varName].values;
                const axes = data.domain.axes;

                const width = axes.x.num;
                const height = axes.y.num;

                const minLon = Math.min(axes.x.start, axes.x.stop);
                const maxLon = Math.max(axes.x.start, axes.x.stop);
                const minLat = Math.min(axes.y.start, axes.y.stop);
                const maxLat = Math.max(axes.y.start, axes.y.stop);


                console.log(minLon, maxLon, minLat, maxLat);
                console.log(width, height);

                // msgCoords = document.createElement("p");
                // msgCoords.innerText = `Étendue des données \n [minLon, maxLon, minLat, maxLat] :\n [${minLon}, ${maxLon}, ${minLat}, ${maxLat}]`;
                // console.log(msgCoords);
                // controlPanel.appendChild(msgCoords);

                canvas.width = width;
                canvas.height = height;


                const imgData = ctx.createImageData(width, height);

                let minVal = -18.02; // Valeur min approximative pour l'échelle de couleur
                let maxVal = 18.86;  // Valeur max approximative

                const isLatDescending = axes.y.start > axes.y.stop;

                for (let y = 0; y < height; y++) {
                    for (let x = 0; x < width; x++) {
                        const dataIndex = y * width + x;
                        const val = values[dataIndex];

                        let normalized = (val - minVal) / (maxVal - minVal);
                        normalized = Math.max(0, Math.min(1, normalized))

                        const r = Math.floor(30 + normalized * 210);
                        const g = Math.floor(144 + (104 * normalized));
                        const b = 255;
                        const alpha = 180;

                        const canvasY = isLatDescending ? y : (height - 1) - y;
                        const index = (canvasY * width + x) * 4;

                        imgData.data[index] = r;     // R
                        imgData.data[index + 1] = g; // G
                        imgData.data[index + 2] = b; // B
                        imgData.data[index + 3] = alpha; // Alpha
                    }
                }

                ctx.putImageData(imgData, 0, 0);

                const imageUrl = canvas.toDataURL();

                const imageBounds = [[minLat, minLon], [maxLat, maxLon]];

                windLayer = L.imageOverlay(imageUrl, imageBounds, { opacity: 0.8 }).addTo(map);

                statusElem.innerText = "Chargé !";
                statusElem.style.color = "#4caf50";
                debugElem.innerText = "Layer ajouté avec succès.";

            } catch (error) {
                console.error(error);
                statusElem.innerText = "Erreur";
                statusElem.style.color = "red";
                debugElem.innerText = "Erreur: " + error.message;
            }
        }

        loadAndDrawLayer();

    </script>
</body>

</html>
