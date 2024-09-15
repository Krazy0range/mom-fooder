import fuzzysort from 'fuzzysort'

let table = document.getElementById('products-table');
let search = document.getElementById('search');
search.oninput = updateTable;

function updateTable(e) {
    let searchText = e.target.value;
    console.log(searchText);
    for (let row of table.rows) {
        let cell = row.cells[0];
        // TODO
        if ( || cell.innerText == "Product")
            row.style.display = '';
        else
            row.style.display = 'none';
    }
}