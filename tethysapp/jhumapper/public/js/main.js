const map = L.map('map', {
    zoom: 4,
    minZoom: 2,
    zoomSnap: .5,
    boxZoom: true,
    maxBounds: L.latLngBounds(L.latLng(-100.0, -270.0), L.latLng(100.0, 270.0)),
    center: [0, 0],
})
const URL_OPENSTREETMAP = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const layerOSM = L.tileLayer(URL_OPENSTREETMAP, {attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'});
const basemaps = {"Open Street Maps": layerOSM.addTo(map)};
const layerControl = L.control.layers(basemaps).addTo(map);

let layerSchigella = null;


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
    }).addTo(map);
    layerControl.addOverlay(layerSchigella, "Schigella Layer")
};