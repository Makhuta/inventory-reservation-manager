function decide_stock_display(on_warehouse_filter, itemStockedValue) {
    if(!on_warehouse_filter) return true;
    if(on_warehouse_filter.value == "warehouse_all") return true;
    if(on_warehouse_filter.value == "warehouse_borrowed" && !itemStockedValue) return true;
    if(on_warehouse_filter.value == "warehouse_returned" && itemStockedValue) return true;

    return false;
}

function update_filter(f) {
    let filter = f ? f.value.toLowerCase() : "";
    let on_warehouse_filter = document.getElementById("on_warehouse_filter");
    let rows = document.querySelectorAll("#inventory > tbody > tr");

    rows.forEach(row => {
        let titleElement = row.querySelector("[data-id='item_name']");
        let titleText = titleElement ? titleElement.getAttribute("data-value").toLowerCase() : "";
        let inventoryNumberElement = row.querySelector("[data-id='item_inventory_number']");
        let inventoryNumberText = inventoryNumberElement ? inventoryNumberElement.getAttribute("data-value").toLowerCase() : "";
        let itemStockedElement = row.querySelector("[data-id='item_stocked']");
        let itemStockedValue = (itemStockedElement ? itemStockedElement.getAttribute("data-value").toLowerCase() : "false") == "true";

        row.style.display = ((titleText.includes(filter) || inventoryNumberText.includes(filter)) && decide_stock_display(on_warehouse_filter, itemStockedValue)) ? "" : "none";
    });
}

document.getElementById("tableFilter").addEventListener("keyup", function () {
    update_filter(this);
});

function replace_class(obj, from, to) {
    if(!obj || !obj.classList) return;
    obj.classList.remove(from);
    obj.classList.add(to);
}

function clean_return_filter(obj) {
    for(var ch of obj.querySelectorAll("i")) {
        ch.classList.add("d-none");
    }
    obj.querySelector("#warehouse_all").classList.remove("d-none")
    obj.value = "warehouse_all"
    obj.querySelector("#warehouse_all").classList.remove("d-none")
    for(var type of ["primary", "secondary", "success", "danger", "warning", "info", "light", "dark", "white"]) {
        obj.classList.remove(`btn-outline-${type}`);
    }
    obj.classList.add(`btn-outline-warning`);
}

document.querySelector("#on_warehouse_filter").addEventListener("click", function(event) {
    let filterInput = document.getElementById("tableFilter");
    let on_warehouse_filter = document.getElementById("on_warehouse_filter");
    for(var ch of on_warehouse_filter.querySelectorAll("i")) {
        ch.classList.add("d-none");
    }
    switch(on_warehouse_filter.value) {
        case "warehouse_all":
            on_warehouse_filter.value = "warehouse_returned"
            on_warehouse_filter.querySelector("#warehouse_returned").classList.remove("d-none")
            replace_class(on_warehouse_filter, "btn-outline-warning", "btn-outline-success")
            break;
        case "warehouse_returned":
            on_warehouse_filter.value = "warehouse_borrowed"
            on_warehouse_filter.querySelector("#warehouse_borrowed").classList.remove("d-none")
            replace_class(on_warehouse_filter, "btn-outline-success", "btn-outline-danger")
            break;
        case "warehouse_borrowed":
            on_warehouse_filter.value = "warehouse_all"
            on_warehouse_filter.querySelector("#warehouse_all").classList.remove("d-none")
            replace_class(on_warehouse_filter, "btn-outline-danger", "btn-outline-warning")
            break;
        default:
            clean_return_filter(on_warehouse_filter);
            break;
    }
    update_filter(filterInput);
});

document.querySelector("#clean_filter").addEventListener("click", function(event) {
    let filterInput = document.getElementById("tableFilter");
    filterInput.value = "";
    let on_warehouse_filter = document.getElementById("on_warehouse_filter");
    clean_return_filter(on_warehouse_filter);
    update_filter(filterInput);
});