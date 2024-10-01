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

  // Search filtering logic
  $('#search-input').on('input', function () {
    const searchText = $(this).val().toLowerCase();
    // Filter items based on the search text
    $('.tm-list-item').each(function () {
      const placeName = $(this).find('.tm-list-item-name').text().toLowerCase();
      $(this).toggle(placeName.includes(searchText));
    });
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

