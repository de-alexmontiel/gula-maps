// Document Ready
$(document).ready(function () {
  // Initial page setup
  initPage();


  // Handle page navigation links (Inicio, Servicios, etc.)
  $('.tm-page-link').on('click', function (event) {
    event.preventDefault();
    const targetPage = $(this.hash); // Get the target page by hash
    // Highlight the selected menu item
    highlightMenu($(this));
    // Show the correct page and hide the rest
    showPage(targetPage);
  });

  // Handle tab navigation within the food section (Restaurantes, Bares, Cafeterías)
  $('.tm-tab-link').on('click', function (event) {
    event.preventDefault();
    openTab($(this).data('id'));
  });

  // Search filtering logic (Modificado para buscar en todas las categorías)
  $('#search-input').on('input', function () {
    const searchText = $(this).val().toLowerCase();
    // Filter items across all categories based on the search text
    $('.tm-list-item').each(function () {
      const placeName = $(this).find('.tm-list-item-name').text().toLowerCase();
      $(this).toggle(placeName.includes(searchText));
    });

    // Si el input de búsqueda está vacío, mostrar la categoría seleccionada
    if (searchText === "") {
      const activeTabId = $('.tm-tab-link.active').data('id');
      $('.tm-tab-content').hide(); // Oculta todas las categorías
      $('#' + activeTabId).show(); // Muestra la categoría activa
    } else {
      // Si se está buscando algo, mostrar todos los elementos que coinciden con el texto
      $('.tm-tab-content').show(); // Mostrar todas las categorías para la búsqueda
    }
  });
});

function initPage() {
  // Ocultar todo el contenido de las páginas excepto la página de inicio
  $('.tm-page-content').hide();
  $('#food').show(); // Mostrar la sección de Gula Maps

  // Inicializar las pestañas de Gula Maps
  $('.tm-tab-content').hide(); // Ocultar todas las categorías
  $('#resta').show(); // Mostrar Restaurantes por defecto
  $('.tm-tab-link').removeClass('active');
  $('.tm-tab-link[data-id="resta"]').addClass('active');
}



function openTab(id) {
  // Hide all tab content
  $('.tm-tab-content').hide();
  // Show the selected tab content
  $('#' + id).show();
  // Deactivate all tabs and activate the selected one
  $('.tm-tab-link').removeClass('active');
  $('.tm-tab-link[data-id="' + id + '"]').addClass('active');
}

function highlightMenu(menuItem) {
  // Deactivate all menu items and activate the selected one
  $('.tm-page-link').removeClass('active');
  menuItem.addClass('active');
}

function showPage(page) {
  // Oculta todas las secciones
  $('.tm-page-content').hide(); // Oculta todo el contenido de la página
  $('.tm-tab-content').hide();  // Oculta las categorías de Gula Maps

  // Verificar si la página actual es "Gula Maps"
  if (page.attr('id') === 'food') {
    // Mostrar Gula Maps y la primera categoría (restaurantes)
    $('#food').show();
    $('#resta').show();
    $('.tm-tab-link').removeClass('active');
    $('.tm-tab-link[data-id="resta"]').addClass('active');
  } else {
    // Mostrar la página seleccionada (Servicios, Contacto, etc.)
    page.show();
  }
}


document.addEventListener('DOMContentLoaded', function () {
  const dropdownBtn = document.querySelector('.tm-dropdown-btn');
  const dropdownOptions = document.getElementById('dropdown-options');
  const dropdownIcon = dropdownBtn.querySelector('i');

  // Toggle visibility of dropdown options and arrow direction on button click
  dropdownBtn.addEventListener('click', function () {
    const isVisible = dropdownOptions.style.display === 'block';

    dropdownOptions.style.display = isVisible ? 'none' : 'block';
    dropdownIcon.classList.toggle('fa-chevron-up', !isVisible);
    dropdownIcon.classList.toggle('fa-chevron-down', isVisible);
  });

  // Close the dropdown and reset the arrow if the user clicks outside of it
  window.addEventListener('click', function (event) {
    if (!event.target.matches('.tm-dropdown-btn')) {
      dropdownOptions.style.display = 'none';
      dropdownIcon.classList.remove('fa-chevron-up');
      dropdownIcon.classList.add('fa-chevron-down');
    }
  });

  // Close the dropdown when an option is selected
  document.querySelectorAll('#dropdown-options a').forEach(function (link) {
    link.addEventListener('click', function () {
      dropdownOptions.style.display = 'none';
      dropdownIcon.classList.remove('fa-chevron-up');
      dropdownIcon.classList.add('fa-chevron-down');
    });
  });
});


document.getElementById('city-filter-btn').addEventListener('click', function () {
  document.getElementById('city-splash').style.display = 'flex';
});

document.getElementById('close-splash').addEventListener('click', function () {
  document.getElementById('city-splash').style.display = 'none';
});


document.addEventListener('DOMContentLoaded', function () {
  const cityFilterBtn = document.getElementById('city-filter-btn');
  const splash = document.getElementById('city-splash');
  const closeSplash = document.getElementById('close-splash');
  const selectedCity = document.getElementById('selected-city');

  // Abrir el splash solo si no hay una ciudad seleccionada (o cuando el botón es presionado)
  let cityFromCookie = getCookie('ciudad'); // Obtener ciudad de la cookie
  if (!cityFromCookie) {
    splash.style.display = 'flex';
  }

  // Abrir el splash al hacer clic en el botón
  cityFilterBtn.addEventListener('click', function () {
    splash.style.display = 'flex';
  });

  // Cerrar el splash
  closeSplash.addEventListener('click', function () {
    splash.style.display = 'none';
  });

  // Cambiar el icono de la flecha según el estado del splash
  cityFilterBtn.addEventListener('click', function () {
    const icon = this.querySelector('i');
    if (splash.style.display === 'flex') {
      icon.classList.remove('fa-chevron-down');
      icon.classList.add('fa-chevron-up');
    } else {
      icon.classList.remove('fa-chevron-up');
      icon.classList.add('fa-chevron-down');
    }
  });

  // Función para obtener el valor de una cookie por su nombre
  function getCookie(name) {
    let match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    if (match) {
      return match[2];
    } else {
      return null;
    }
  }
});

