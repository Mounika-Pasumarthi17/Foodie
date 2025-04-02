// Location Modal Functionality
const modal = document.getElementById('locationModal');
const locationPicker = document.querySelector('.location-picker');
const closeBtn = document.querySelector('.close');
const cityItems = document.querySelectorAll('.city-item');
const citySearchInput = document.querySelector('.search-city input');
const currentLocationText = document.querySelector('.location-picker');

// Event data for different dates
const eventData = {
    today: [
        {            
            image: "{% static 'm1.jpg' %}",
            title: "Hyderabad Live Music Show",
            venue: "Shilpakala Vedika: Hyderabad",
            price: "₹ 499 onwards"
        },
        {
            image: "{% static 'm2.jpg' %}",
            title: "Summer Music Festival",
            venue: "Phoenix Arena: Hyderabad",
            price: "₹ 799 onwards"
        },
        {
            image: "{% static 'm3.jpg' %}",
            title: "Classical Music Night",
            venue: "Ravindra Bharathi: Hyderabad",
            price: "₹ 299 onwards"
        }
    ],
    tomorrow: [
        {
            image: "{% static 'm4.jpg' %}",
            title: "Rock Band Live Performance",
            venue: "Heart Cup Coffee: Hyderabad",
            price: "₹ 599 onwards"
        },
        {
            image: "{% static 'm5.jpg' %}",
            title: "Jazz Night Special",
            venue: "Moonshine Project: Hyderabad",
            price: "₹ 899 onwards"
        },
        {
            image: "{% static 'm7.jpg' %}",
            title: "Sufi Music Evening",
            venue: "Taj Krishna: Hyderabad",
            price: "₹ 699 onwards"
        }
    ],
    weekend: [
        {
            image: "{% static 'm9.jpg' %}",
            title: "Music Festival 2024",
            venue: "HITEX Exhibition Center: Hyderabad",
            price: "₹ 1499 onwards"
        },
        {
            image: "{% static 'm8.jpg' %}",
            title: "International DJ Night",
            venue: "N Convention: Hyderabad",
            price: "₹ 2499 onwards"
        },
        {
            image: "{% static 'm6.jpg' %}",
            title: "Rock Music Festival",
            venue: "AU Engineering College: Vizag",
            price: "₹ 1999 onwards"
        }
    ]
};

// Function to render events
function renderEvents(events) {
    const eventsGrid = document.querySelector('.events-container .row');
    eventsGrid.innerHTML = '';

    events.forEach(event => {
        const eventCard = document.createElement('div');
        eventCard.className = 'col-md-4 mt-4';
        eventCard.innerHTML = `
            <div class="card mb-4 equal-width">
                <img src="${event.image}" class="card-img-top" alt="${event.title}" loading="lazy">
                <div class="card-body">
                    <h3>${event.title}</h3>
                    <p class="venue">${event.venue}</p>
                    <p class="price">${event.price}</p>
                </div>
            </div>
        `;
        eventsGrid.appendChild(eventCard);
    });
}

// Open modal
locationPicker.addEventListener('click', () => {
    modal.style.display = 'block';
    citySearchInput.focus();
});

// Close modal
closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.style.display = 'none';
    }
});

// City search functionality
citySearchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    cityItems.forEach(item => {
        const cityName = item.textContent.toLowerCase();
        if (cityName.includes(searchTerm)) {
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
        }
    });
});

// City selection
cityItems.forEach(item => {
    item.addEventListener('click', () => {
        const selectedCity = item.dataset.city || item.textContent;
        currentLocationText.innerHTML = `<i class="fas fa-map-marker-alt"></i> ${selectedCity}`;
        modal.style.display = 'none';
        
        // Update page title and heading
        document.title = `Music Shows in ${selectedCity} | BookMyShow`;
        document.querySelector('.events-container h1').textContent = `Music Shows in ${selectedCity}`;
    });
});

// Date filter functionality
const dateButtons = document.querySelectorAll('.date-btn');
dateButtons.forEach(button => {
    button.addEventListener('click', () => {
        dateButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        
        const date = button.textContent.toLowerCase();
        renderEvents(eventData[date]);
    });
});

// Footer link functionality
const footerLinks = document.querySelectorAll('.footer-section ul li');
footerLinks.forEach(link => {
    link.addEventListener('click', () => {
        const page = link.textContent;
        alert(`Navigating to ${page} page`);
    });
});

// Initialize the page
// document.addEventListener('DOMContentLoaded', () => {
//     console.log('BookMyShow clone initialized');
//     const todayButton = document.querySelector('.date-btn');
//     todayButton.classList.add('active');
//     renderEvents(eventData.today);
// });


// document.addEventListener('DOMContentLoaded', () => {
    
//     const searchInput = document.querySelector('.search-bar input');
//     const eventCardsContainer = document.querySelector('.events-container');
//     const eventCards = Array.from(document.querySelectorAll('.card'));
//     const noResultsMessage = document.createElement('div'); 

   
//     noResultsMessage.textContent = "No results found!";
//     noResultsMessage.style.display = 'none';  //
//     eventCardsContainer.appendChild(noResultsMessage);

    
//     searchInput.addEventListener('input', () => {
//         const query = searchInput.value.toLowerCase();
//         let matchedEvents = [];
//         let resultsFound = false; 

        
//         eventCards.forEach(card => {
//             const eventTitle = card.querySelector('.card-body h3').textContent.toLowerCase();
//             const eventVenue = card.querySelector('.venue').textContent.toLowerCase();

           
//             if (eventTitle.includes(query) || eventVenue.includes(query)) {
//                 matchedEvents.push(card); 
//                 resultsFound = true;
//             }
//         });

      
//         eventCardsContainer.innerHTML = '';

       
//         matchedEvents.forEach(event => {
//             eventCardsContainer.appendChild(event); 
//         });

        
//         if (!resultsFound) {
//             noResultsMessage.style.display = 'block';  
//         } else {
//             noResultsMessage.style.display = 'none';  
//         }
//     });
// });





