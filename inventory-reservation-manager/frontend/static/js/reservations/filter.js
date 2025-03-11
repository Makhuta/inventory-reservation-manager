function decide_stock_display(on_returned_filter, itemReturnedValue) {
    if(!on_returned_filter) return true;
    if(on_returned_filter.value == "returned_all") return true;
    if(on_returned_filter.value == "returned_borrowed" && !itemReturnedValue) return true;
    if(on_returned_filter.value == "returned_returned" && itemReturnedValue) return true;

    return false;
}

function update_filter(f) {
    let filter = f ? f.value.toLowerCase() : "";
    let on_warehouse_filter = document.getElementById("on_warehouse_filter");
    let rows = document.querySelectorAll("#inventory > tbody > tr");

    rows.forEach(row => {
        let titleElement = row.querySelector("[data-id='item_name']");
        let titleText = titleElement ? titleElement.getAttribute("data-value").toLowerCase() : "";
        let clientElement = row.querySelector("[data-id='item_client']");
        let clientText = clientElement ? clientElement.getAttribute("data-value").toLowerCase() : "";
        let itemReturnedElement = row.querySelector("[data-id='item_returned']");
        let itemReturnedValue = (itemReturnedElement ? itemReturnedElement.getAttribute("data-value").toLowerCase() : "false") == "true";

        row.style.display = ((titleText.includes(filter) || clientText.includes(filter)) && decide_stock_display(on_returned_filter, itemReturnedValue)) ? "" : "none";
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
    obj.querySelector("#returned_all").classList.remove("d-none")
    obj.value = "returned_all"
    obj.querySelector("#returned_all").classList.remove("d-none")
    for(var type of ["primary", "secondary", "success", "danger", "warning", "info", "light", "dark", "white"]) {
        obj.classList.remove(`btn-outline-${type}`);
    }
    obj.classList.add(`btn-outline-warning`);
}

document.querySelector("#on_returned_filter").addEventListener("click", function(event) {
    let filterInput = document.getElementById("tableFilter");
    let on_returned_filter = document.getElementById("on_returned_filter");
    for(var ch of on_returned_filter.querySelectorAll("i")) {
        ch.classList.add("d-none");
    }
    switch(on_returned_filter.value) {
        case "returned_all":
            on_returned_filter.value = "returned_returned"
            on_returned_filter.querySelector("#returned_returned").classList.remove("d-none")
            replace_class(on_returned_filter, "btn-outline-warning", "btn-outline-success")
            break;
        case "returned_returned":
            on_returned_filter.value = "returned_borrowed"
            on_returned_filter.querySelector("#returned_borrowed").classList.remove("d-none")
            replace_class(on_returned_filter, "btn-outline-success", "btn-outline-danger")
            break;
        case "returned_borrowed":
            on_returned_filter.value = "returned_all"
            on_returned_filter.querySelector("#returned_all").classList.remove("d-none")
            replace_class(on_returned_filter, "btn-outline-danger", "btn-outline-warning")
            break;
        default:
            clean_return_filter(on_returned_filter);
            break;
    }
    update_filter(filterInput);
});

document.querySelector("#clean_filter").addEventListener("click", function(event) {
    let filterInput = document.getElementById("tableFilter");
    filterInput.value = "";
    let on_returned_filter = document.getElementById("on_returned_filter");
    clean_return_filter(on_returned_filter);
    update_filter(filterInput);
})