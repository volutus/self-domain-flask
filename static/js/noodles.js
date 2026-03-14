$(document).ready(function() 
{ 
    $(".review-grade").click(function() 
    {
        const parent = $(this).parent();
        $(parent).children(".review-toggle").toggle(250);
    });
});