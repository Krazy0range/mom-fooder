const request = new Request("https://www.costco.com/")
fetch(request)
    .then((response) => {console.log(response.json())});