let selectedPiece = undefined;
let squares = document.querySelectorAll(".square");
squares.forEach(function(square)
{
    square.addEventListener("click", function()
    {
        document.querySelectorAll(".selected").forEach(function(selected)
        {
            selected.classList.remove("selected");
        });
        this.classList.add("selected");

        const coordinate = this.getAttribute("id");
        const piece = getPiece(coordinate);
        if (selectedPiece != undefined)
        {
            move(selectedPiece, coordinate);
        }
        if (piece != undefined)
        {
            selectedPiece = coordinate;
        }
    });
});

function move(source, destination)
{
    const piece = getPiece(source);
    if (piece == undefined)
    {
        return;
    }

    document.getElementById(destination).innerHTML = piece.outerHTML;
    document.getElementById(source).innerHTML = '';
}
function getPiece(coordinate)
{
    const element = document.getElementById(coordinate);
    return element.querySelector(".piece");
}