function update_filter(f) {
    let filter = f ? f.value.toLowerCase() : "";
    let rows = document.querySelectorAll("#inventory > tbody > tr");

    rows.forEach(row => {
        let titleElement = row.querySelector("[data-id='item_name']");
        let titleText = titleElement ? titleElement.getAttribute("data-value").toLowerCase() : "";
        let clientElement = row.querySelector("[data-id='item_client']");
        let clientText = clientElement ? clientElement.getAttribute("data-value").toLowerCase() : "";

        row.style.display = (titleText.includes(filter) || clientText.includes(filter)) ? "" : "none";
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