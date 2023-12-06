const response = await fetch(
  "$api_url$api_path?" + new URLSearchParams({
        lon: "13.438596",
        lat: "52.519854"
  })
);
const data = await response.json();

// prints the name of the first result
console.log(data.features[0].properties.name);
