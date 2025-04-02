document.getElementById("tableFilter").addEventListener("keyup", function () {
    update_filter(this);
});

document.querySelector("#clean_filter").addEventListener("click", function(event) {
    let filterInput = document.getElementById("tableFilter");
    filterInput.value = "";
    update_filter(filterInput);
})