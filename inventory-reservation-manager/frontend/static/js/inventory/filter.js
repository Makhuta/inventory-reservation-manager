function update_filter(f) {
    let filter = f ? f.value.toLowerCase() : "";
    let rows = document.querySelectorAll("#inventory > tbody > tr");

    rows.forEach(row => {
        let titleElement = row.querySelector("[data-id='item_name']");
        let titleText = titleElement ? titleElement.getAttribute("data-value").toLowerCase() : "";
        let inventoryNumberElement = row.querySelector("[data-id='item_inventory_number']");
        let inventoryNumberText = inventoryNumberElement ? inventoryNumberElement.getAttribute("data-value").toLowerCase() : "";

        row.style.display = (titleText.includes(filter) || inventoryNumberText.includes(filter)) ? "" : "none";
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