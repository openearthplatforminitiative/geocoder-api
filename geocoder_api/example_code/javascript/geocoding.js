const response = await fetch(
  "$endpoint_url?" + new URLSearchParams({ q: "Berlin" })
);
const data = await response.json();

// prints the coordinates of the first result
console.log(data.features[0].geometry.coordinates);
