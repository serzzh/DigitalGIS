// initalize leaflet map

const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
const map = L.map('map')
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: attribution }).addTo(map);

const raster_url = "http://oin-hotosm.s3.amazonaws.com/5afeda152b6a08001185f11a/0/5afeda152b6a08001185f11b.tif";
parseGeoraster(raster_url).then(georaster => {
console.log(georaster.height);
const options = { left: 0, top: 0, right: 4000, bottom: 4000, width: 10, height: 10 };
georaster.getValues(options).then(values => {
  console.log("clipped values are", values);
});
});
