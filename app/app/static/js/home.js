document.addEventListener("DOMContentLoaded", function () {
  const yearSelect = document.getElementById("year");
  const currentYear = new Date().getFullYear();

  for (let year = currentYear; year >= 1960; year--) {
    const option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    yearSelect.appendChild(option);
  }
});
document.addEventListener("DOMContentLoaded", function () {
  const puissanceSelect = document.getElementById("puissance");

  for (let i = 4; i <= 17; i++) {
    const option = document.createElement("option");
    option.value = i;
    option.textContent = i;
    puissanceSelect.appendChild(option);
  }
});
fetch("http://127.0.0.1:8000/api/villes/")
  .then((response) => response.json()) // Parse the JSON response
  .then((data) => {
    data.sort((a, b) => a.name.localeCompare(b.name)); // Sort the data alphabetically
    const villeSelect = document.getElementById("ville"); // Get the select element

    // Loop through the array and create an option for each city
    data.forEach((item) => {
      const option = document.createElement("option");
      option.value = item.id; // Set the value as the city name
      option.textContent = item.name; // Set the display text as the city name
      villeSelect.appendChild(option); // Append the option to the select
    });
  })
  .catch((error) => {
    console.error("Error fetching data:", error); // Log any errors to the console
  });

fetch("http://127.0.0.1:8000/api/marques/")
  .then((response) => response.json()) // Parse the JSON response
  .then((data) => {
    data.sort((a, b) => a.name.localeCompare(b.name)); // Sort the data alphabetically
    const marque = document.getElementById("marque"); // Get the select element

    // Loop through the array and create an option for each brand
    data.forEach((item) => {
      const option = document.createElement("option");
      option.value = item.id; // Set the value as the brand name
      option.textContent = item.name; // Set the display text as the brand name
      marque.appendChild(option); // Append the option to the select
    });
  })
  .catch((error) => {
    console.error("Error fetching data:", error); // Log any errors to the console
  });

document.addEventListener("DOMContentLoaded", function () {
  const marqueSelect = document.getElementById("marque");
  const modeleSelect = document.getElementById("modele");
  const villeSelect = document.getElementById("ville");
  const secteurSelect = document.getElementById("secteur");

  // 🎯 Handle Marque → Modele
  marqueSelect.addEventListener("change", function () {
    const selectedMarque = this.value;
    modeleSelect.innerHTML =
      "<option value='' disabled='' selected=''>Sélectionner</option>"; // Clear previous options

    if (selectedMarque) {
      fetch(`http://127.0.0.1:8000/api/modeles_by_marque/${selectedMarque}/`)
        .then((response) => response.json())
        .then((data) => {
          data.sort((a, b) => a.name.localeCompare(b.name)); // Sort the data alphabetically
          data.forEach((item) => {
            const option = document.createElement("option");
            option.value = item.id;
            option.textContent = item.name;
            modeleSelect.appendChild(option);
          });
          modeleSelect.disabled = false;
        })
        .catch((error) => {
          console.error("Error fetching modèles:", error);
        });
    }
  });

  villeSelect.addEventListener("change", function () {
    const selectedVille = this.value;
    secteurSelect.innerHTML =
      "<option value='' disabled='' selected=''>Sélectionner</option>"; // Clear previous options

    if (selectedVille) {
      fetch(`http://127.0.0.1:8000/api/secteurs_by_ville/${selectedVille}/`)
        .then((response) => response.json())
        .then((data) => {
          data.sort((a, b) => a.name.localeCompare(b.name)); // Sort the data alphabetically
          data.forEach((item) => {
            const option = document.createElement("option");
            option.value = item.id;
            option.textContent = item.name;
            secteurSelect.appendChild(option);
          });
          secteurSelect.disabled = false;
        })
        .catch((error) => {
          console.error("Error fetching secteurs:", error);
        });
    }
  });
});

function predictPrice() {
  // Get all the form values
  const age =
    new Date().getFullYear() - parseInt(document.getElementById("year").value);
  const modele =
    document.getElementById("modele").options[
      document.getElementById("modele").selectedIndex
    ].text;
  const marque =
    document.getElementById("marque").options[
      document.getElementById("marque").selectedIndex
    ].text;
  const boite = document.getElementById("boite").value;
  const carburant = document.getElementById("carburant").value;
  const km = parseInt(document.getElementById("km").value);
  const puissance = parseInt(document.getElementById("puissance").value);
  const ville =
    document.getElementById("ville").options[
      document.getElementById("ville").selectedIndex
    ].text;
  const secteur =
    document.getElementById("secteur").options[
      document.getElementById("secteur").selectedIndex
    ].text;

  const origine = document.getElementById("origine").value;

  // Prepare the data to send
  const formData = {
    "Age (annees)": age,
    Modele: modele,
    Marque: marque,
    "Boite de vitesses_Manuelle": boite === "manuelle" ? 1 : 0,
    "Puissance fiscale": puissance,
    "Type de carburant_Essence": carburant === "essence" ? 1 : 0,
    "Kilometrage lisse (en milliers km)": km,
    "Type de carburant_Diesel": carburant === "diesel" ? 1 : 0,
    Secteur: secteur,
    Ville: ville,
    "Origine_WW au Maroc": origine === "ww" ? 1 : 0,
    Origine_Dédouanée: origine === "dedouanee" ? 1 : 0,
  };

  // Send the form data to the server for prediction
  fetch("http://127.0.0.1:8000/api/predict/", {
    method: "POST",
    body: JSON.stringify(formData),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data && data.predictions && data.predictions.length > 0) {
        const predictedPrice = Math.round(data.predictions[0]);

        // Fill in price
        document.getElementById(
          "price-value"
        ).textContent = `${predictedPrice} DH`;

        // Prepare info list
        const carInfoList = document.getElementById("car-info");
        carInfoList.innerHTML = `
                    <li><strong>Marque:</strong> ${marque}</li>
                    <li><strong>Modèle:</strong> ${modele}</li>
                    <li><strong>Âge:</strong> ${age} années</li>
                    <li><strong>Kilométrage:</strong> ${km}K km</li>
                    <li><strong>Boîte de vitesses:</strong> ${boite}</li>
                    <li><strong>Carburant:</strong> ${carburant}</li>
                    <li><strong>Puissance fiscale:</strong> ${puissance}</li>
                    <li><strong>Origine:</strong> ${origine}</li>
                    <li><strong>Ville:</strong> ${ville}</li>
                    <li><strong>Secteur:</strong> ${secteur}</li>
                  `;

        // Show popup
        document.getElementById("result-popup").classList.remove("hidden");
      } else {
        console.error("Invalid prediction format:", data);
      }
    })
    .catch((error) => {
      console.error("Error during prediction:", error);
    });
}

// Close popup on button click
document.getElementById("close-popup").addEventListener("click", () => {
  document.getElementById("result-popup").classList.add("hidden");
});
