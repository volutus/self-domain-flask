let selectedPiece = undefined;
let selectedSquare = undefined;
let squares = document.querySelectorAll(".square");
squares.forEach(function(square)
{
    square.addEventListener("click", function()
    {
        const coordinate = this.getAttribute("id");
        // Handle selection logic for the same square
        if (selectedSquare != undefined && coordinate == selectedSquare)
        {
            const highlighted = document.querySelectorAll(".selected").length > 0;
            if (highlighted)
            {
                clearHighlight();
                resetSelections();
            }
            else
            {
                highlight(this);
            }
            return;
        }

        // Reset highlighter state
        clearHighlight();
        highlight(this);
        selectedSquare = coordinate;

        const piece = getPiece(coordinate);
        if (selectedPiece != undefined && selectedPiece != coordinate)
        {
            move(selectedPiece, coordinate, this);
            resetSelections();
        }
        else if (piece != undefined)
        {
            selectedPiece = coordinate;
        }
    });
});

function clearHighlight()
{
    document.querySelectorAll(".selected").forEach(function(selected)
    {
        selected.classList.remove("selected");
    });
}
function highlight(element)
{
    element.classList.add("selected");
}
function move(source, destination)
{
    const piece = getPiece(source);
    if (piece == undefined)
    {
        return;
    }

    // TODO Handle response!
    response = attemptMove(source, destination);

    // IF VALID
    document.getElementById(destination).innerHTML = piece.outerHTML;
    document.getElementById(source).innerHTML = '';
    clearHighlight();
}

function resetSelections()
{
    selectedSquare = undefined;
    selectedPiece = undefined;
}
function getPiece(coordinate)
{
    const element = document.getElementById(coordinate);
    return element.querySelector(".piece");
}
function attemptMove(source, destination)
{
    // TODO tell the server our move and see what it says

}