function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i += 1) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === `${name}=`) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('add-category-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const categoryName = document.getElementById('category-name').value;
    const data = { categoryName };

    fetch('/api/category/', {
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      method: 'POST',
    })
      .then((response) => response.json())
      .then((responseData) => {
        if (responseData.success) {
          alert('Catégorie ajoutée avec succès.');
          window.location.reload();
        } else {
          alert(responseData.message || 'Une erreur est survenue.');
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  });
});
