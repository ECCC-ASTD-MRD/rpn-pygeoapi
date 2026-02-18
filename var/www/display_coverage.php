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
    </style>
</head>

<body>
    <h1>
        <?= $title ?> - <span id="status" style="color: orange;">Chargement...</span>
    </h1>

    <div id="map"></div>
    <div id="debug">En attente de données...</div>

    <script>
tomate cerise 
        const DATA_URL = "http://localhost:5000/collections/public-zarr/coverage?f=json&properties=10m_u_component_of_wind&datetime=2020-01-01T00:00:00/2020-01-01T00:00:00";

        const map = L.map('map').setView([45, -73], 4);

        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://www.openstreetgorg/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 19
        }).addTo(map);/*
        
        L.tileLayer.wms('https://geo.weather.gc.ca/geomet?', {
            layers: 'GDPS.ETA_TT',
            version: '1.3.0',
            opacity: 0.5,
        }).addTo(map);*/

        async function loadAndDrawLayer() {
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

                const canvas = document.createElement('canvas');
                canvas.width = width;
                canvas.height = height;
                const ctx = canvas.getContext('2d');

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

        loadAndDrawLayer();

    </script>
</body>

</html>
