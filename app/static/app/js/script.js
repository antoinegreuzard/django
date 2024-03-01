if (document.getElementById('searchInput')) {
  document.getElementById('searchInput').addEventListener('input', function () {
    const input = this.value;
    const autocompleteList = document.getElementById('autocomplete-list');
    if (!input) {
      document.getElementById('autocomplete-list').innerHTML = '';
      this.style.borderBottomLeftRadius = ''
      this.style.borderBottomRightRadius = ''
      autocompleteList.style.borderWidth = ''
      return;
    } else {
      this.style.borderBottomLeftRadius = '0'
      this.style.borderBottomRightRadius = '0'
      autocompleteList.style.borderWidth = '1px'
    }


    fetch(`/api/search-autocomplete/?term=${input}`)
      .then(response => response.json())
      .then(data => {
        autocompleteList.innerHTML = '';
        data.forEach(item => {
          const div = document.createElement('div');
          div.innerHTML = item;
          div.addEventListener('click', function () {
            document.getElementById('searchInput').value = this.innerText;
            autocompleteList.innerHTML = '';
            document.getElementById('searchForm').submit();
          });
          autocompleteList.appendChild(div);
        });
      })
      .catch(error => console.log('Error:', error));
  });
}