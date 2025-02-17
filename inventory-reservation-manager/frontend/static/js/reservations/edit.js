const userColors = {}; // Store assigned colors
const colors = [
    "#FF5733", "#33FF57", "#3357FF", "#FF33A8", "#FFB833", "#8A33FF", "#33FFF5",
    "#FF3333", "#33FF8A", "#5733FF", "#FF8A33", "#A833FF", "#33FFA8", "#FF33F5",
    "#B8FF33", "#FF338A", "#338AFF", "#8AFF33", "#F5FF33", "#33A8FF", "#FF33C2",
    "#33FF33", "#FF8333", "#3385FF", "#85FF33", "#FF3385", "#3383FF", "#83FF33",
    "#FF8335", "#33FF83", "#3385FF"
];

function getUserColor(name) {
    if (!userColors[name]) {
        userColors[name] = colors[Object.keys(userColors).length % colors.length];
    }
    return userColors[name];
}

function addOneDay(dateStr) {
    const date = new Date(dateStr);

    date.setDate(date.getDate() + 1);

    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Month is 0-indexed
    const day = String(date.getDate()).padStart(2, '0');

    return `${year}-${month}-${day}`;
}

document.addEventListener("DOMContentLoaded", function() {
    const calendarEl = document.getElementById("calendar");
    let selectedEvent = null;
    let startDate = null;
    let endDate = null;
    let startEvent = null;
    let endEvent = null;

    function initializeCalendar(datas = []) {
        let calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: "dayGridMonth",
            selectable: true, // Enable selecting dates
            selectMirror: true,
            firstDay: 1, // Start week on Monday
            locale: "cs",
            events: datas.reserved.map(date => ({ 
                title: datas.clients[date], 
                start: date, 
                allDay: true,
                backgroundColor: getUserColor(datas.clients[date]), 
                borderColor: getUserColor(datas.clients[date])
            })),
            dateClick: function (info) {
                if (selectedEvent) {
                    selectedEvent.remove();
                }

                if (!startDate) {
                    // First click: Set start date marker
                    startDate = info.dateStr;
                    
                    if (startEvent) startEvent.remove(); // Remove previous start marker
                    startEvent = calendar.addEvent({
                        title: "",
                        start: startDate,
                        color: "blue",
                        allDay: true
                    });

                } else if (!endDate) {
                    // Second click: Set end date marker
                    endDate = info.dateStr;

                    if (endEvent) endEvent.remove(); // Remove previous end marker
                    endEvent = calendar.addEvent({
                        title: "",
                        start: endDate,
                        color: "blue",
                        allDay: true
                    });

                    // Ensure the start date is before the end date
                    if (new Date(startDate) > new Date(endDate)) {
                        [startDate, endDate] = [endDate, startDate]; // Swap if needed
                    }

                    // Update form fields
                    document.querySelector("input[name='start']").value = startDate;
                    document.querySelector("input[name='end']").value = endDate;
                    
                    // Add new selection event
                    selectedEvent = calendar.addEvent({
                        title: "Výběr",
                        start: startDate,
                        end: addOneDay(endDate),
                        color: "blue",
                        allDay: true
                    });

                    console.info(endDate)
                    
                    startDate = null;
                    endDate = null;
                    
                    if (startEvent) startEvent.remove();
                    if (endEvent) endEvent.remove();
                }
            },
            eventClick: function (info) {
                if (info.event.title === "Reserved") {
                    alert("This date is already reserved!");
                    info.jsEvent.preventDefault();
                }
            },
            headerToolbar: {
                left: 'title',
                center: '',
                right: 'today prev,next'
            },
            buttonText: {
                today: 'Dnes', // Customize the "Today" button text for Czech
            }
        });

        selectedEvent = calendar.addEvent({
            title: "Výběr",
            start: document.querySelector("input[name='start']").value,
            end: addOneDay(document.querySelector("input[name='end']").value),
            color: "blue",
            allDay: true
        });

        calendar.render();
    }

    // Load reservations for initially selected item
    let itemId = itemSelect.value;
    fetchReservations(itemId, initializeCalendar);

    // Update calendar when item changes
    itemSelect.addEventListener("change", function() {
        fetchReservations(this.value, initializeCalendar);
    });


    const imageContainer = document.getElementById("item-image-container");
    const imageElement = document.getElementById("item-image");

    function updateImage() {
        const selectedItem = itemSelect.options[itemSelect.selectedIndex];
        const imageUrl = selectedItem.getAttribute("data-image-url");

        if (imageUrl) {
            imageElement.src = imageUrl;
            imageContainer.style.display = "initial";
        } else {
            imageContainer.style.display = "none";
        }
    }

    itemSelect.addEventListener("change", updateImage);
    updateImage(); // Run on page load in case item is pre-selected
});