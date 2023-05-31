// Activating all Bootstrap(v5.3) Tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
// Tooltips Ends

$(document).ready(function () {
  // For Side-Bar
  $("#sidebar").mCustomScrollbar({
      theme: "minimal"
  });
  
  // For Side-Bar
  $('#sidebarCollapse').on('click', function () {
      $('#sidebar, #content').toggleClass('active');
      $('.collapse.in').toggleClass('in');
      $('a[aria-expanded=true]').attr('aria-expanded', 'false');
  });
  
  // Buttons on Inventory to switch between GRID and TILE view
  $('#btnCard').on('click', function () {
    $('#dispCard').removeClass('d-none');
    $('#btnCard').removeClass('bg-transparent');
    $('#dispTable').addClass('d-none');
    $('#btnTable').addClass('bg-transparent');
    console.log("btnCard clicked");
  });
  
  // Buttons on Inventory to switch between GRID and TILE view
  $('#btnTable').on('click', function () {
    $('#dispTable').removeClass('d-none');
    $('#btnTable').removeClass('bg-transparent');
    $('#dispCard').addClass('d-none');
    $('#btnCard').addClass('bg-transparent');
    console.log('btnTable clicked');
  });

  // Inventory-Add Item Form 
  // 1). Add measuring unit where-ever required in 
  //     the form after it has been entered/changed
  $('#mu-1-in').change(function() {
    $('#actual-qty-unit, #gst-qty-unit, #min-stock-unit, #gst-surplus-unit, #gst-defecit-unit').html($('#mu-1-in').val());
    if(($('#mu-2-in').val()) && ($('#mu-1-in').val())) {
      $('#measuring_relation').removeClass('invisible');
      $('#mu-1-put').html($('#mu-1-in').val());
      $('#mu-2-put').html($('#mu-2-in').val());
      $('#mr-in').prop('required',true);
    }
    else {
      $('#measuring_relation').addClass('invisible');
      $('#mr-in').prop('required',false);
      $('#mr-in').val('');        
    }
  });

  // 2). Make measuring-relation visible when-ever
  //     there is a change detected in any of the 
  //     measuring-unit field
  $('#mu-2-in').change(function() {
    if(($('#mu-1-in').val()) && ($('#mu-2-in').val())) {
      $('#measuring_relation').removeClass('invisible');
      $('#mu-1-put').html($('#mu-1-in').val());
      $('#mu-2-put').html($('#mu-2-in').val());
      $('#mr-in').prop('required',true);
    }
    else {
      $('#measuring_relation').addClass('invisible');
      $('#mr-in').prop('required',false);
      $('#mr-in').val('');
    }
  });
  
});

// Bootstrap validation for Form Inputs
(() => {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }

      form.classList.add('was-validated')
    }, false)
  })
})()
