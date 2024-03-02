import '../css/home.css';

function debounce(func, wait) {
  let timeout;
  return function debounced(...args) {
    const context = this;
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(context, args), wait);
  };
}

document.addEventListener('DOMContentLoaded', function onDOMContentLoaded() {
  const searchInput = document.getElementById('search-input');
  const autocompleteList = document.getElementById('autocomplete-list');
  const searchForm = document.getElementById('searchForm');

  if (!searchInput || !autocompleteList || !searchForm) return;

  const fetchAutocompleteData = debounce(function fetchAutocomplete(input) {
    if (!input) {
      autocompleteList.innerHTML = '';
      searchInput.style.borderBottomLeftRadius = '';
      searchInput.style.borderBottomRightRadius = '';
      autocompleteList.style.borderWidth = '';
      return;
    }

    searchInput.style.borderBottomLeftRadius = '0';
    searchInput.style.borderBottomRightRadius = '0';
    autocompleteList.style.borderWidth = '1px';

    fetch(`/api/search-autocomplete/?term=${input}`)
      .then((response) => response.json())
      .then((data) => {
        autocompleteList.innerHTML = '';
        data.forEach((item) => {
          const div = document.createElement('div');
          div.textContent = item;
          div.addEventListener('click', function onItemClick() {
            searchInput.value = this.textContent;
            autocompleteList.innerHTML = '';
            searchForm.submit();
          });
          autocompleteList.appendChild(div);
        });
      })
      .catch((error) => console.error('Error:', error));
  }, 250);

  searchInput.addEventListener('input', function onInput() {
    fetchAutocompleteData(this.value);
  });
});
