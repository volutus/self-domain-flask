$(document).ready(function() 
{ 
    $(".review-grade").click(function() 
    {
        const parent = $(this).parent();
        $(parent).find(".review-toggle").toggle(250);
    });
});