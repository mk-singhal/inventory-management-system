// Activating all Bootstrap(v5.3) Tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
// Tooltips Ends

$(document).ready(function () {
  // For Side-Bar
  // $("#sidebar").mCustomScrollbar({
  //     theme: "minimal"
  // });
  
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

  // Populate Seller-details in Create-Purchase Form
  // on change of option
  $('#select-seller').on('change', function(){
    seller_id = $(this).val();
    if (seller_id == '') {
      $('#seller-pic').attr('src', '/static/img/noImg.png');
      $('#seller-pic').attr('alt', 'No Image !');
      $('#seller-gstin').html('- - -');
      $('#seller-mob_no').html('- - -');
      $('#seller-email').html('- - -');
      $('#seller-address').html('- - -');
    }
    request_url = '/seller/get-seller/' + seller_id + '/';
    $.ajax({
      url: request_url,
      success: function(data){
        console.log("data: ", data);
        $('#seller-pic').attr('src', data['pic_url']);
        $('#seller-pic').attr('alt', data['name']);
        if (data['gstin']) $('#seller-gstin').html(data['gstin']);
        else $('#seller-gstin').html('- - -');
        if (data['mob_no']) $('#seller-mob_no').html(data['mob_no']);
        else $('#seller-mob_no').html('- - -');
        if (data['email']) $('#seller-email').html(data['email']);
        else $('#seller-email').html('- - -');
        if (data['address']) $('#seller-address').html(data['address']);
        else $('#seller-address').html('- - -');
      }
    });
    return false;
  });

  

  // Populate Product-details in Create-Purchase Form
  // on change of option
  $('table').on('change', 'select', function(){
    var curr_product = $(this);
    // console.log("\n###\n")
    product_id = curr_product.val();
    if (product_id == '') {
      curr_product.parent().siblings('#product-pic').children('img').attr('src', '/static/img/noImg.png');
      curr_product.parent().siblings('#product-pic').children('img').attr('alt', 'No Image !');
      curr_product.parent().siblings('#product-gst').html('- -');
      curr_product.siblings('#product-hsn_code').html('- - -');
    }
    request_url = '/inventory/get-product/' + product_id + '/';
    $.ajax({
      url: request_url,
      success: function(data){
        console.log("\n\n$$$$", curr_product, curr_product.parent().siblings('#mu').children('div span#tot-qty'));
        curr_product.parent().siblings('#product-pic').children('img').attr('src', data['pic_url']);
        curr_product.parent().siblings('#product-pic').children('img').attr('alt', data['name']);
        if (data['gst']) curr_product.parent().siblings('#product-gst').html(data['gst']+'%');
        else curr_product.parent().siblings('#product-gst').html('- -');
        if (data['hsn_code']) curr_product.siblings('#product-hsn_code').html(data['hsn_code']);
        else curr_product.siblings('#product-hsn_code').html('- - -');
        curr_product
            .parent()
            .siblings('#mu')
            .children()
            .children('span')
            .html(data['mu_1']);
      }
    });
    return false;
  });

  $('#purchase-order-form').submit(function() {
    
    $('#create-purchase-table tbody tr').each(function (i) {
      $(this).find('select').attr('name', 'select_products_' + i)
      $(this).find('div#qty > input').attr('name', 'qty_' + i);
      // $(this).find('div#qty-bill > input').attr('name', 'qty_bill_' + i);
      // $(this).find('div#noqty-bill > input').attr('name', 'noqty_bill_' + i);
      $(this).find('div#cost-price > input').attr('name', 'cost_price_' + i);
      console.log(i, $(this).find('select').attr('name'));
      console.log(i, $(this).find('div#qty > input').attr('name'));
      // console.log(i, $(this).find('div#qty-bill > input').attr('name'));
      // console.log(i, $(this).find('div#noqty-bill > input').attr('name'));
      console.log(i, $(this).find('div#cost-price > input').attr('name'));
    });
    var tb_length = $('table tr').length;
    var input = $("<input>")
                   .attr("type", "hidden")
                   .attr("name", "total_product")
                   .val(tb_length-1);
    $('form').append($(input));
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
