const map = L.map('map', {
    zoom: 4,
    minZoom: 2,
    zoomSnap: .5,
    boxZoom: true,
    maxBounds: L.latLngBounds(L.latLng(-100.0, -270.0), L.latLng(100.0, 270.0)),
    center: [0, 0],
})

let layerSchigella = null;
let selectedNetCDF = $("#select-layers option:selected").text();
let selectedLayer = $("#select-layers").val();

const layerDraw = new L.FeatureGroup();
layerDraw.addTo(map);
const drawControl = new L.Control.Draw({
    position: 'topleft',
    draw: {
        polyline: false,
        polygon: {
            allowIntersection: false, // Restricts shapes to simple polygons
        },
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
    let url = `${URL_THREDDS}${selectedNetCDF}?REQUEST=GetLegendGraphic&LAYER=${$("#select-layers").val()}&COLORSCALERANGE=0,50`;
    div.innerHTML = `<img src="${url}" alt="legend" style="width:100%; float:right;">`
    return div
};

const addWMS = function (url, layer) {
    if (layerSchigella !== null) {
        layerControl.removeLayer(layerSchigella);
        map.removeLayer(layerSchigella);
    }
    layerSchigella = L.tileLayer.wms(url, {
        layers: layer,
        format: "image/png",
        transparent: true,
        crossOrigin: false,
        colorscalerange: '0,50',
    }).addTo(map);
    layerControl.addOverlay(layerSchigella, "Schigella Layer")
    legend.addTo(map);
};

$("#select-layers").change(() => {
    selectedNetCDF = $("#select-layers option:selected").text();
    selectedLayer = $("#select-layers").val();
    addWMS(`${URL_THREDDS}${selectedNetCDF}`, selectedLayer)
})

addWMS(`${URL_THREDDS}${selectedNetCDF}`, selectedLayer);
map.addControl(drawControl);
map.on("draw:drawstart", function (event) {
    layerDraw.clearLayers();
})
map.on("draw:created", function (event) {
    layerDraw.addLayer(event.layer);
    let data = {file: selectedNetCDF}
    if (event.layerType === "marker") {
        data.point = event.layer._latlng  // json {lat, lng}
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
    console.log(querydata)
    $.ajax({
        method: 'GET',
        url: URL_QUERYVALUES,
        data: JSON.stringify(querydata),
        contentType: 'application/json',
        success: function (result) {
            alert(result)
        }
    })
}