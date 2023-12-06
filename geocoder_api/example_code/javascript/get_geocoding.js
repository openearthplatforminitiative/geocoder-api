const response = await fetch(
  "$api_url$api_path?" + new URLSearchParams({ q: "Berlin" })
);
const data = await response.json();

// prints the coordinates of the first result
console.log(data.features[0].geometry.coordinates);
