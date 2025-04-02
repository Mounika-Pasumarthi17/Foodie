document.getElementById('searchBar').addEventListener('keyup', function() {
  let filter = this.value.toUpperCase();
  let foodItems = document.querySelectorAll('.food-item li');
  
  foodItems.forEach(function(item) {
      let text = item.textContent || item.innerText;
      if (text.toUpperCase().indexOf(filter) > -1) {
          item.style.display = "";
      } else {
          item.style.display = "none";
      }
  });
});

// Sample restaurant data
const restaurants = [
    {
      name: "Burger King",
      image: "https://via.placeholder.com/300x200",
      cuisine: "Burgers, Fast Food",
      rating: 4.2
    },
    {
      name: "Pizza Hut",
      image: "https://via.placeholder.com/300x200",
      cuisine: "Pizza, Italian",
      rating: 4.5
    },
    {
      name: "Sushi Palace",
      image: "https://via.placeholder.com/300x200",
      cuisine: "Japanese, Sushi",
      rating: 4.7
    }
  ];
  
  // Function to display restaurants
  function displayRestaurants(restaurants) {
    const restaurantList = document.getElementById("restaurant-list");
    restaurantList.innerHTML = ""; // Clear existing content
  
    restaurants.forEach(restaurant => {
      const card = document.createElement("div");
      card.className = "restaurant-card";
  
      card.innerHTML = `
        <img src="${restaurant.image}" alt="${restaurant.name}">
        <h3>${restaurant.name}</h3>
        <p>Cuisine: ${restaurant.cuisine}</p>
        <p>Rating: ${restaurant.rating} ⭐</p>
      `;
  
      restaurantList.appendChild(card);
    });
  }
  
  // Initial display of restaurants
  displayRestaurants(restaurants);
  
  // Search functionality
  document.getElementById("search").addEventListener("input", (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const filteredRestaurants = restaurants.filter(restaurant =>
      restaurant.name.toLowerCase().includes(searchTerm)
    );
    displayRestaurants(filteredRestaurants);
  });
//   function scrollLeft() {
//     document.getElementById("food_container").scrollBy({ left: -200, behavior: 'smooth' });
// }

// function scrollRight() {
//     document.getElementById("food_container").scrollBy({ left: 200, behavior: 'smooth' });
// }
// function scrollLeft1() {
//   document.getElementById("food_container1").scrollBy({ left: -200, behavior: 'smooth' });
// }
// function scrollRight1() {
//   document.getElementById("food_container1").scrollBy({ left: 200, behavior: 'smooth' });
// }

// function scrollLeft(containerId) {
//   let container = document.getElementById(containerId);
//   if (container) {
//       container.scrollBy({ left: -200, behavior: "smooth" });
//   }
// }

// function scrollRight(containerId) {
//   let container = document.getElementById(containerId);
//   if (container) {
//       container.scrollBy({ left: 200, behavior: "smooth" });
//   }
// }


function scrollContainer(containerId, direction) {
  const container = document.getElementById(containerId);
  if (container) {
      const scrollAmount = 200 * direction; // -200 for left, 200 for right
      container.scrollBy({ left: scrollAmount, behavior: "smooth" });
  }
}

function showDetails(title, description) {
  document.getElementById('food-title').innerText = title;
  document.getElementById('food-description').innerText = description;
  document.getElementById('food-details').style.display = 'block';
}

function placeOrder() {
  alert('Order placed successfully!');
}

function addToCart() {
  alert('Item added to cart!');
}
