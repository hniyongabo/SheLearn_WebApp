document.addEventListener("DOMContentLoaded", function () {
    const selected = document.querySelector(".select-selected");
    const items = document.querySelector(".select-items");
    const options = document.querySelectorAll(".select-items div");
    const hiddenInput = document.getElementById("region-input");

    function closeDropdown() {
        items.classList.add("select-hide");
        selected.classList.remove("select-active");
    }

    // Toggle dropdown
    selected.addEventListener("click", function (e) {
        e.stopPropagation();
        items.classList.toggle("select-hide");
        selected.classList.toggle("select-active");
    });

    // Handle option selection
    options.forEach(option => {
        option.addEventListener("click", function (e) {
            e.stopPropagation();
            // Update the display text
            selected.innerHTML = this.innerHTML;

            // Update the hidden input value for form submission
            hiddenInput.value = this.getAttribute("data-value");

            // Remove selection class from all others and add to clicked
            const sameAsSelected = this.parentNode.querySelectorAll(".same-as-selected");
            for (let i = 0; i < sameAsSelected.length; i++) {
                sameAsSelected[i].classList.remove("same-as-selected");
            }
            this.setAttribute("class", "same-as-selected");

            // Change selected text color to signify choice made
            selected.style.color = "#333";

            // Close dropdown
            closeDropdown();
        });
    });

    // Close the dropdown if the user clicks anywhere outside of it
    document.addEventListener("click", function (e) {
        if (!e.target.matches('.select-selected')) {
            if (!items.classList.contains('select-hide')) {
                closeDropdown();
            }
        }
    });
});
