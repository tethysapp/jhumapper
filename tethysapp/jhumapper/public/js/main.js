const map = L.map('map', {
    zoom: 3,
    minZoom: 2,
    zoomSnap: .5,
    boxZoom: true,
    maxBounds: L.latLngBounds(L.latLng(-100.0, -270.0), L.latLng(100.0, 270.0)),
    center: [0, 0],
    timeDimension: true,
    timeDimensionControl: true,
    timeDimensionControlOptions: {
        position: "bottomleft",
        autoPlay: true,
        loopButton: true,
        backwardButton: true,
        forwardButton: true,
        timeSliderDragUpdate: true,
        minSpeed: 2,
        maxSpeed: 6,
        speedStep: 1,
    },
})

let layerShigella = null;

const layerDraw = new L.FeatureGroup();
layerDraw.addTo(map);
const drawControl = new L.Control.Draw({
    position: 'topleft',
    draw: {
        polyline: false,
        // polygon: {
        //     allowIntersection: false, // Restricts shapes to simple polygons
        // },
        polygon: false,
        circle: false, // Turns off this drawing tool
        rectangle: true,
        marker: true
    },
    edit: {
        featureGroup: layerDraw
    }
});

const URL_OPENSTREETMAP = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const layerOSM = L.tileLayer(URL_OPENSTREETMAP, {attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'});
const basemaps = {"Open Street Maps": layerOSM.addTo(map)};
const layerControl = L.control.layers(basemaps, {"Drawings": layerDraw}, {collapsed: false}).addTo(map);

const legend = L.control({position: 'bottomright'});
legend.onAdd = () => {
    let div = L.DomUtil.create('div', 'legend');
    let url = `${URL_THREDDS}?REQUEST=GetLegendGraphic&LAYER=${$("#select-layers").val()}&COLORSCALERANGE=0,50`;
    div.innerHTML = `<img src="${url}" alt="legend" style="width:100%; float:right;">`
    return div
};

const addWMS = function () {
    let layer = $("#select-layers").val()
    if (layerShigella !== null) {
        layerControl.removeLayer(layerShigella);
        map.removeLayer(layerShigella);
    }
    layerShigella = L.tileLayer.wms(URL_THREDDS, {
        layers: layer,
        format: "image/png",
        transparent: true,
        crossOrigin: false,
        colorscalerange: '0,50',
    });
    if (layer === 'probability') {
        layerShigella = L.timeDimension.layer.wms(layerShigella, {
            name: 'time',
            requestTimefromCapabilities: true,
            updateTimeDimension: true,
            updateTimeDimensionMode: 'replace',
            cache: 20,
        })
    }
    layerShigella.addTo(map)
    layerControl.addOverlay(layerShigella, "Shigella Layer")
    legend.addTo(map);
};

$("#select-layers").change(() => {
    addWMS()
})

addWMS();

map.addControl(drawControl);
map.on("draw:drawstart", function (event) {
    layerDraw.clearLayers();
})
map.on("draw:created", function (event) {
    layerDraw.addLayer(event.layer);
    let data = {}
    if (event.layerType === "marker") {
        data.point = [event.layer._latlng.lat, event.layer._latlng.lng]  // event.layer._latlng -> json {lat, lng}
    } else if (event.layerType === "rectangle") {
        data.rectangle = [
            event.layer._latlngs[0][0].lat,
            event.layer._latlngs[0][0].lng,
            event.layer._latlngs[0][2].lat,
            event.layer._latlngs[0][2].lng,
        ]  // array of 4 {lat, lng}, clockwise from bottom left
    } else if (event.layerType === "polygon") {
        data.polygon = layerDraw.toGeoJSON()  // geojson object
    }

    queryValues(data)
});

const queryValues = function (querydata) {
    $.ajax({
        method: 'GET',
        url: URL_QUERYVALUES,
        data: querydata,
        success: function (result) {
            $("#chart_modal").modal("show");
            plotlyTimeseries(result)
        },
    })
}

function plotlyTimeseries(data) {
    let layout = {
        title: 'Schigella Probability v Time',
        xaxis: {title: 'Time'},
        yaxis: {title: 'Probability (%)'}
    };

    let values = {
        x: data.x,
        y: data.y,
        title: 'probabilities',
        mode: 'lines+markers',
        type: 'scatter'
    };
    Plotly.newPlot('chart', [values], layout);
    let chart = $("#chart");
    chart.css('height', 500);
    Plotly.Plots.resize(chart[0]);
}