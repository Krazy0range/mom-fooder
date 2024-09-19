let table = document.getElementById('products-table');
let search = document.getElementById('search');

search.addEventListener('keydown', (e) => {
    if (e.key == 'Enter') {
        updateTable(e);
    }
});

function updateTable(e) {
    let searchText = e.target.value.toLowerCase();
    for (let row of table.rows) {
        let cell = row.cells[0];
        let cellText = cell.innerText.toLowerCase();
        const result = fuzzysort.single(searchText, cellText);
        if ((result && result.score >= 0.5) || cell.innerText == "Product" || searchText == '')
            row.style.display = '';
        else
            row.style.display = 'none';
    }
}