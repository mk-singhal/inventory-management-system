// Activating all Bootstrap(v5.3) Tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
// Tooltips Ends

// Formating prices to round to max 2 decimal digits
var format = new Intl.NumberFormat('en-IN', {
  style: 'currency',
  currency: 'INR',
  minimumFractionDigits: 0,
  maximumFractionDigits: 2,
});

// Converts amount to words in Indian Rupee System (no decimals)
function price_in_words(price) {
  var sglDigit = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"],
    dblDigit = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"],
    tensPlace = ["", "Ten", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"],
    handle_tens = function(dgt, prevDgt) {
      return 0 == dgt ? "" : " " + (1 == dgt ? dblDigit[prevDgt] : tensPlace[dgt])
    },
    handle_utlc = function(dgt, nxtDgt, denom) {
      return (0 != dgt && 1 != nxtDgt ? " " + sglDigit[dgt] : "") + (0 != nxtDgt || dgt > 0 ? " " + denom : "")
    };

  var str = "",
    digitIdx = 0,
    digit = 0,
    nxtDigit = 0,
    words = [];
  if (price += "", isNaN(parseInt(price))) str = "";
  else if (parseInt(price) > 0 && price.length <= 10) {
    for (digitIdx = price.length - 1; digitIdx >= 0; digitIdx--) switch (digit = price[digitIdx] - 0, nxtDigit = digitIdx > 0 ? price[digitIdx - 1] - 0 : 0, price.length - digitIdx - 1) {
      case 0:
        words.push(handle_utlc(digit, nxtDigit, ""));
        break;
      case 1:
        words.push(handle_tens(digit, price[digitIdx + 1]));
        break;
      case 2:
        words.push(0 != digit ? " " + sglDigit[digit] + " Hundred" : "");
        break;
      case 3:
        words.push(handle_utlc(digit, nxtDigit, "Thousand"));
        break;
      case 4:
        words.push(handle_tens(digit, price[digitIdx + 1]));
        break;
      case 5:
        words.push(handle_utlc(digit, nxtDigit, "Lakh"));
        break;
      case 6:
        words.push(handle_tens(digit, price[digitIdx + 1]));
        break;
      case 7:
        words.push(handle_utlc(digit, nxtDigit, "Crore"));
        break;
      case 8:
        words.push(handle_tens(digit, price[digitIdx + 1]));
        break;
      case 9:
        words.push(0 != digit ? " " + sglDigit[digit] + " Hundred" + (0 != price[digitIdx + 1] || 0 != price[digitIdx + 2] ? "" : " Crore") : "")
    }
    str = words.reverse().join("")
  } else str = "";
  return str;
};


$(document).ready(function () {
  // {all pages} -- Collapse side-bar on button press
  $('#sidebarCollapse').on('click', function () {
      $('#sidebar, #content').toggleClass('active');
      $('.collapse.in').toggleClass('in');
      $('a[aria-expanded=true]').attr('aria-expanded', 'false');
  });
  
  // inventory/inventory.html -- Buttons on Inventory to switch 
  //                             between GRID and TILE view
  $('#btnCard').on('click', function () {
    $('#dispCard').removeClass('d-none');
    $('#btnCard').removeClass('bg-transparent');
    $('#dispTable').addClass('d-none');
    $('#btnTable').addClass('bg-transparent');
    console.log("btnCard clicked");
  });
  
  // inventory/inventory.html -- Buttons on Inventory to switch 
  //                             between GRID and TILE view
  $('#btnTable').on('click', function () {
    $('#dispTable').removeClass('d-none');
    $('#btnTable').removeClass('bg-transparent');
    $('#dispCard').addClass('d-none');
    $('#btnCard').addClass('bg-transparent');
    console.log('btnTable clicked');
  });

  // inventory/addProduct.html -- 1). Add measuring unit where-
  //                                  ever required in the form
  //                                  after it has been entered/changed
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

  // inventory/addProduct.html -- 2). Make measuring-relation 
  //                                  visible when-ever there is a
  //                                  change detected in any of the 
  //                                  measuring-unit field
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

  // sale/sale.html -- Submit the form on change
  $('#sale-filters').change(function() {
    this.submit();
  });

  // sale/createSale.html -- Select the Type of Sale i.e.  
  //                         Inter-state or Intra-state
  $.fn.gstType = function() {
    vl = $('#create-sale-select-gst').val();
    if (vl == 1) {
      $('thead tr th#cgst, tbody tr td#cgst').attr('hidden', false);
      $('thead tr th#sgst, tbody tr td#sgst').attr('hidden', false);
      $('thead tr th#utgst, tbody tr td#utgst').attr('hidden', true);
      $('thead tr th#igst, tbody tr td#igst').attr('hidden', true);
    }
    else if (vl == 2) {
      $('thead tr th#cgst, tbody tr td#cgst').attr('hidden', true);
      $('thead tr th#sgst, tbody tr td#sgst').attr('hidden', true);
      $('thead tr th#utgst, tbody tr td#utgst').attr('hidden', false);
      $('thead tr th#igst, tbody tr td#igst').attr('hidden', true);
    }
    else if (vl == 3) {
      $('thead tr th#cgst, tbody tr td#cgst').attr('hidden', true);
      $('thead tr th#sgst, tbody tr td#sgst').attr('hidden', true);
      $('thead tr th#utgst, tbody tr td#utgst').attr('hidden', true);
      $('thead tr th#igst, tbody tr td#igst').attr('hidden', false);
    }
  }

  $('#create-sale-select-gst').on('change', function() {
    $.fn.gstType();
  });
  
  $.fn.populateRowCalc = function() { 
    let total_taxable_val = 0;
    let total_gst = 0;
    console.log('Function Called !!');
    $('#sale-table tbody tr').each(function(i) {
      if (i != $('#sale-table tr').length-2) {
        let gst_rate = $(this).children('td').eq(8).find('span').html();
        if (gst_rate == '--') {
          $(this).find('#sale-taxable-value').html('₹--');
          $(this).find('#sale-tax-cgst').html('₹--');
          $(this).find('#sale-tax-sgst').html('₹--');
          $(this).find('#sale-tax-utgst').html('₹--');
          $(this).find('#sale-tax-igst').html('₹--');
          $(this).find('#sale-total').html('₹--');
        }
        else {
          let qty = $(this).children('td').eq(1).find('input').val();
          let rate = $(this).children('td').eq(2).find('input').val();
          let discount = $(this).children('td').eq(3).find('input').val();
          let taxable_val = (qty*rate) - ((discount*0.01)*(qty*rate));
          let gst = gst_rate*0.01*taxable_val;
          let total = taxable_val + gst;
          $(this).find('#sale-taxable-value').html(format.format(taxable_val));
          $(this).find('#sale-tax-cgst').html(format.format(gst/2));
          $(this).find('#sale-tax-sgst').html(format.format(gst/2));
          $(this).find('#sale-tax-utgst').html(format.format(gst));
          $(this).find('#sale-tax-igst').html(format.format(gst));
          $(this).find('#sale-total').html(format.format(total));
          console.log('Called !!');
          total_taxable_val = total_taxable_val + (qty*rate) - ((discount*0.01)*(qty*rate));
          total_gst = total_gst + gst_rate*0.01*taxable_val;
        }
      }
    });
    $('#sale-table tbody tr:last').children('td').eq(4).html(format.format(total_taxable_val));
    $('#sale-table tbody tr:last').children('td').eq(5).html(format.format(total_gst/2));
    $('#sale-table tbody tr:last').children('td').eq(6).html(format.format(total_gst/2));
    $('#sale-table tbody tr:last').children('td').eq(7).html(format.format(total_gst));
    $('#sale-table tbody tr:last').children('td').eq(8).html(format.format(total_gst));
    $('#sale-table tbody tr:last').children('td').eq(9).html(format.format(total_taxable_val+total_gst));
    $('#sale-taxable-amt').html(format.format(total_taxable_val));
    $('#sale-total-tax').html(format.format(total_gst));
    $('#sale-total-amt').html(format.format(total_taxable_val+total_gst));
    
    var splittedNum = ((total_taxable_val+total_gst).toFixed(2)).toString().split('.');
    // console.log(splittedNum);
    var nonDecimal=splittedNum[0];
    if (splittedNum[1] && splittedNum[1] != '00') {
      var decimal=splittedNum[1];
      if (splittedNum[0] != '0')
      var value=price_in_words(Number(nonDecimal))+" rupee and "+price_in_words(Number(decimal))+" paise only";
      else var value="Zero rupee and "+price_in_words(Number(decimal))+" paise only";
    }
    else {
      var value = price_in_words(Number(nonDecimal))+" rupee only";
    }
    $('#sale-total-amt-words').html(value);
  }

  // sale/createSale.html -- Populate Taxable value, GST, Total 
  //                         fields after a change in Qty, Rate 
  //                         or Discount
  $('table#sale-table').on('change', function() {
    $.fn.populateRowCalc();
  });

  $('table#sale-table').on('change', 'select', function() {
    $.fn.populateRowCalc();
  });

  $('table#sale-table').on('click', 'button#sale-del-product', function(){
    $(this).closest('tr').remove();
    $.fn.populateRowCalc();
  });

  // sale/createSale.html -- Remove dropdown from Select-Customers
  //                         for unregistered Customer
  $('#sale-customer-status input').on('change', function() {
    if ($(this).val() == 'no') {
      $('#select-customer').prop('disabled', true);
      $('#select-customer').next(".select2-container").hide();
      // Enable Name Field
      $('#sale-bill-to').children('input').eq(0).val('');
      $('#sale-bill-to').children('input').eq(0).prop('hidden', false);
      $('#sale-bill-to').children('input').eq(0).prop('disabled', false);
      // Enable Address-1
      $('#sale-bill-to').children('input').eq(1).val('');
      $('#sale-bill-to').children('input').eq(1).prop('disabled', false);
      $('#sale-bill-to').children('input').eq(1).prop('readonly', false);
      // Enable Address-2
      $('#sale-bill-to').children('input').eq(2).val('');
      $('#sale-bill-to').children('input').eq(2).prop('disabled', false);
      $('#sale-bill-to').children('input').eq(2).prop('readonly', false);
      // Enable Select-State
      $('#sale-bill-to').children('select').prop('hidden', false);
      $('#sale-bill-to').children('select').prop('disabled', false);
      $('#sale-ship-to').children('select').prop('hidden', false);
      $('#sale-ship-to').children('select').prop('disabled', false);
      // Disable GSTIN
      $('#sale-bill-to').children('input').eq(3).prop('hidden', true);
      $('#sale-ship-to').children('input').eq(3).prop('disabled', true);
      $('#sale-ship-to').children('input').eq(3).prop('hidden', true);
    }
    else {
      // Enable Select-Customer
      $('#select-customer').prop('disabled', false);
      $('#select-customer').next(".select2-container").show();
      // Enable Name Field
      $('#sale-bill-to').children('input').eq(0).prop('hidden', true);
      $('#sale-bill-to').children('input').eq(0).prop('disabled', true);
      // Enable Address-1
      $('#sale-bill-to').children('input').eq(1).val('');
      $('#sale-bill-to').children('input').eq(1).prop('disabled', true);
      $('#sale-bill-to').children('input').eq(1).prop('readonly', true);
      // Enable Address-2
      $('#sale-bill-to').children('input').eq(2).val('');
      $('#sale-bill-to').children('input').eq(2).prop('disabled', true);
      $('#sale-bill-to').children('input').eq(2).prop('readonly', true);
      // Enable Select-State
      $('#sale-bill-to').children('select').prop('hidden', true);
      $('#sale-bill-to').children('select').prop('disabled', true);
      $('#sale-ship-to').children('select').prop('hidden', true);
      $('#sale-ship-to').children('select').prop('disabled', true);
      // Disable GSTIN
      $('#sale-bill-to').children('input').eq(3).prop('hidden', false);
      $('#sale-ship-to').children('input').eq(3).prop('disabled', false);
      $('#sale-ship-to').children('input').eq(3).prop('hidden', false);
    }
    if ($('#sale-same-as-bill-to').is(':checked')) {
      $.fn.sameAsBillTo();
    } 
  });

  // sale/createSale.html -- Populate 'Ship To' when 'same as Bill TO'
  //                         checkbox is checked 
  $.fn.sameAsBillTo = function() {
    $('#sale-ship-to').children('input').each(function (i) {
      if(i==0 && $("input[name='customer_status']:checked").val()=='yes') {
        console.log("Select", i);
        $(this).val($('#select-customer').find(':selected').text());
      }
      else {
        console.log("Not Select", i);
        $(this).val($('#sale-bill-to').children('input').eq(i).val());
      }
      $('#sale-ship-to').children('select').val($('#sale-bill-to').find(":selected").val()).change();
    });
  }

  $('#sale-same-as-bill-to').on('change', function() {
    if ($(this).is(':checked')) {
      console.log('Same as Bill To-Checked!!');
      $.fn.sameAsBillTo();
    }
  });

  $('#sale-bill-to').on('change', function(){
    if ($('#sale-same-as-bill-to').is(':checked')) {
      $.fn.sameAsBillTo();
    } 
  });

  // sale/createSale.html -- Populate Customer-details in 
  //                         Create-Sale Form on
  //                         change of option
  $('#select-customer').on('change', function(){
    customer_id = $(this).val();
    if (customer_id == '') {
      $('#sale-bill-to').children('input').eq(1).val('');
      $('#sale-bill-to').children('input').eq(2).val('');
      $('#sale-bill-to').children('input').eq(3).val('');
      if ($('#sale-same-as-bill-to').is(':checked')) {
        $.fn.sameAsBillTo();
      };
    }
    else {
      request_url = '/customer/get-customer/' + customer_id + '/';
      $.ajax({
        url: request_url,
        success: function(data){
          console.log("data: ", data);
          $('#sale-bill-to').children('input').eq(1).val(data['address1']);
          $('#sale-bill-to').children('input').eq(2).val(data['address2']);
          $('#sale-bill-to').children('input').eq(3).val(data['gstin']);
          if ($('#sale-same-as-bill-to').is(':checked')) {
            $.fn.sameAsBillTo();
          };
        }
      });
    }
    return false;
  });

  // purchase/createPurchase.html -- Populate Seller-details in 
  //                                 Create-Purchase Form on
  //                                 change of option
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

  

  // purchase/createPurchase.html, -- Populate Product-details in 
  // sale/createSale.html             Create-Purchase/ Create-Sale
  //                                  Form on change of option
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
        // console.log("\n\n$$$$", curr_product, curr_product.parent().siblings('#mu').children('div span#tot-qty'));
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
        curr_product.closest('tr').children('td').eq(5).find('span').html(data['gst']/2);
        curr_product.closest('tr').children('td').eq(6).find('span').html(data['gst']/2);
        curr_product.closest('tr').children('td').eq(7).find('span').html(data['gst']);
        curr_product.closest('tr').children('td').eq(8).find('span').html(data['gst']);
        curr_product.closest('tr').children('td').eq(2).find('input').val(data['price']);
      }
    });
    return false;
  });

  // sale/createSale.html -- Changes the names of Input 
  //                         field sequentially and also
  //                         sends the total sold products,
  //                         gst sale type in the form
  $('#sale-order-form').submit(function() {
    $('#sale-table tbody tr').each(function (i) {
      $(this).find('select').attr('name', 'select_products_' + i)
      $(this).find('input#sale-qty').attr('name', 'sale_qty_' + i);
      $(this).find('input#sale-rate').attr('name', 'sale_rate_' + i);
      $(this).find('input#sale-dis').attr('name', 'sale_dis_' + i);
      console.log(i, $(this).find('select').attr('name'));
      console.log(i, $(this).find('input#sale-qty').attr('name'));
      console.log(i, $(this).find('input#sale-rate').attr('name'));
      console.log(i, $(this).find('input#sale-dis').attr('name'));
    });
    var tb_length = $('table tr').length;
    var ip_1 = $("<input>")
                   .attr("type", "hidden")
                   .attr("name", "total_product")
                   .val(tb_length-2);
    var ip_2 = $("<input>")
                   .attr("type", "hidden")
                   .attr("name", "gst_sale_type")
                   .val(
                    $('#create-sale-select-gst').val()
                   );
    var ip_3 = $("<input>")
                   .attr("type", "hidden")
                   .attr("name", "customer_registered")
                   .val(
                    $("input[name='customer_status']:checked").val()
                   );
    $('form').append($(ip_3));
    $('form').append($(ip_2));
    $('form').append($(ip_1));
  });

  // purchase/createPurchase.html -- Changes the names of Input 
  //                                 field sequentially and also
  //                                 sends the total purchased 
  //                                 products in the form
  $('#purchase-order-form').submit(function() {
    $('#create-purchase-table tbody tr').each(function (i) {
      $(this).find('select').attr('name', 'select_products_' + i)
      $(this).find('div#qty > input').attr('name', 'qty_' + i);
      $(this).find('div#cost-price > input').attr('name', 'cost_price_' + i);
      console.log(i, $(this).find('select').attr('name'));
      console.log(i, $(this).find('div#qty > input').attr('name'));
      console.log(i, $(this).find('div#cost-price > input').attr('name'));
    });
    var tb_length = $('table tr').length;
    var input = $("<input>")
                   .attr("type", "hidden")
                   .attr("name", "total_product")
                   .val(tb_length-1);
    $('form').append($(input));
  });

  // sale/viewSale.html -- (printThis-JS Plugin) prints the bill
  $('#print-bill').click(function () {
    $('#page').printThis();
  });
  
  // sale/viewSale.html -- Select Original/Duplicate/Triplicate Bill
  $('#view-sale-whichBill').on('change', function() {
    $("#view-sale-whichBillValue").html($(this).find('option:selected').text());
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
