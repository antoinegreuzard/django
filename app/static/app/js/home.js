import '../css/home.css';

function debounce(func, wait) {
  let timeout;
  return (...args) => {
    const context = this;
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(context, args), wait);
  };
}

document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('search-input');
  const autocompleteList = document.getElementById('autocomplete-list');
  const searchAndSortForm = document.getElementById('searchAndSortForm');

  if (!searchInput || !autocompleteList || !searchAndSortForm) return;

  const fetchAutocompleteData = debounce((input) => {
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
          div.addEventListener('click', () => {
            searchInput.value = div.textContent;
            autocompleteList.innerHTML = '';
            searchAndSortForm.submit();
          });
          autocompleteList.appendChild(div);
        });
      })
      .catch((error) => console.error('Error:', error));
  }, 250);

  searchInput.addEventListener('input', () => {
    fetchAutocompleteData(searchInput.value);
  });
});
