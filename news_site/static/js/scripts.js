$(document).ready(function () {
    // Dropdown menu functionality for mobile view
    $('.dropdown-toggle').click(function () {
        $(this).next('.dropdown-menu').toggle();
    });

    // Close dropdown when clicking outside
    $(document).click(function (e) {
        if (!$(e.target).closest('.dropdown').length) {
            $('.dropdown-menu').hide();
        }
    });
}); 