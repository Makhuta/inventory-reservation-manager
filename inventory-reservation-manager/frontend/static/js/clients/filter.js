function update_filter(f) {
    let filter = f ? f.value.toLowerCase() : "";
    let rows = document.querySelectorAll("#inventory > tbody > tr");

    rows.forEach(row => {
        let nameElement = row.querySelector("[data-id='client_name']");
        let nameText = nameElement ? nameElement.getAttribute("data-value").toLowerCase() : "";
        let phoneElement = row.querySelector("[data-id='client_phone']");
        let phoneText = phoneElement ? phoneElement.getAttribute("data-value").toLowerCase() : "";
        let emailElement = row.querySelector("[data-id='client_email']");
        let emailText = emailElement ? emailElement.getAttribute("data-value").toLowerCase() : "";

        row.style.display = (nameText.includes(filter) || phoneText.includes(filter) || emailText.includes(filter)) ? "" : "none";
    });
}

document.getElementById("tableFilter").addEventListener("keyup", function () {
    update_filter(this);
});

document.querySelector("#clean_filter").addEventListener("click", function(event) {
    let filterInput = document.getElementById("tableFilter");
    filterInput.value = "";
    update_filter(filterInput);
})