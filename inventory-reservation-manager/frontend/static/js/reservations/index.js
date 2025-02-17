document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".calendar-container").forEach(container => {
            let itemId = container.getAttribute("data-item-id");
            initCalendar(container, itemId);
        });
    });

    function initCalendar(container, itemId) {
        let currentDate = new Date();
        let currentYear = currentDate.getFullYear();
        let currentMonth = currentDate.getMonth();
        let reservedDates = new Set();

        fetchReservations(itemId, function (data) {
            reservedDates = new Set(data.dates);
            if(reservedDates.size > 0) {
                currentDate = new Date(Date.parse(reservedDates.values().next().value, "yyyy-MM-dd"));
                currentYear = currentDate.getFullYear();
                currentMonth = currentDate.getMonth();
            }
            renderCalendar(container, currentYear, currentMonth, reservedDates);
            container.dataset.year = currentYear;
            container.dataset.month = currentMonth;
        });

    }

    function renderCalendar(container, year, month, reservedDates, clients) {
        let calendarBody = container.querySelector(".calendar-body");
        let monthYear = container.querySelector(".month-year");
        calendarBody.innerHTML = "";

        let firstDay = new Date(year, month, 1).getDay();
        firstDay = (firstDay === 0) ? 6 : firstDay - 1;  // Shift Sunday (0) to Monday (1)

        let lastDate = new Date(year, month + 1, 0).getDate();

        let date = 1;
        for (let i = 0; i < 6; i++) {
            let row = document.createElement("tr");
            if (date > lastDate) {
                break;
            }
            for (let j = 0; j < 7; j++) {
                let cell = document.createElement("td");
                if (i === 0 && j < firstDay) {
                    cell.innerHTML = "";
                } else if (date > lastDate) {
                    cell.innerHTML = "";
                } else {
                    let fullDate = `${year}-${String(month + 1).padStart(2, '0')}-${String(date).padStart(2, '0')}`;
                    cell.innerHTML = date;
                    if (reservedDates.has(fullDate)) {
                        cell.classList.add("reserved");
                        cell.style.backgroundColor = "red";
                        cell.style.color = "white";
                    }
                    date++;
                }
                cell.classList.add("border", "calendar");
                row.appendChild(cell);
            }
            calendarBody.appendChild(row);
        }
        monthYear.innerText = new Date(year, month).toLocaleString("default", { month: "long", year: "numeric" });
    }

    function prevMonth(button) {
        let container = button.closest(".calendar-container");
        let year = parseInt(container.dataset.year);
        let month = parseInt(container.dataset.month);
        if (--month < 0) {
            month = 11;
            year--;
        }
        container.dataset.year = year;
        container.dataset.month = month;
        let itemId = container.getAttribute("data-item-id");
        fetchReservations(itemId, function (data) {
            renderCalendar(container, year, month, new Set(data.dates));
        });
    }

    function nextMonth(button) {
        let container = button.closest(".calendar-container");
        let year = parseInt(container.dataset.year);
        let month = parseInt(container.dataset.month);
        if (++month > 11) {
            month = 0;
            year++;
        }
        container.dataset.year = year;
        container.dataset.month = month;
        let itemId = container.getAttribute("data-item-id");
        fetchReservations(itemId, function (data) {
            dates = data.dates;
            renderCalendar(container, year, month, new Set(dates));
        });
    }