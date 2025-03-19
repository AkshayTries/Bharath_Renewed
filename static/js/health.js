function toggleDetails(id) {
    var element = document.getElementById(id);
    element.style.display = (element.style.display === "none" || element.style.display === "") ? "block" : "none";
}