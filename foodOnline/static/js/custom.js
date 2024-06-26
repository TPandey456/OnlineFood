let autocomplete;

function initAutoComplete() {
  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById("id_address"),
    {
      types: ["geocode", "establishment"],
      // establishment-- means all address like office address, hotel address restaurant address all the bussiness adress
      //default in this app is "IN" - add your country code
      componentRestrictions: { country: ["in"] },
    }
  );
  // function to specify what should happen when the prediction is clicked
  autocomplete.addListener("place_changed", onPlaceChanged);
}

function onPlaceChanged() {
  var place = autocomplete.getPlace();

  // User did not select the prediction. Reset the input field or alert()
  if (!place.geometry) {
    document.getElementById("id_address").placeholder = "Start typing...";
  } else {
    // console.log("place name=>", place.name);
  }
  // get the address components and assign them to the fields
}

// cart-item
$(document).ready(function () {
  // add to cart
  $(".add_to_cart").on("click", function (e) {
    e.preventDefault();

    food_id = $(this).attr("data-id");
    url = $(this).attr("data-url");
    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        // console.log(response);
        if (response.status == "login_required") {
          swal(response.message, "", "info").then(function () {
            window.location = "/login";
          });
        } else if (response.status == "Failed") {
          swal(response.message, "", "error");
        } else {
          $("#cart_counter").html(response.cart_counter["cart_count"]);
          $("#qty-" + food_id).html(response.qty);
          applyCartAmounts(
            response.cart_amount["subtotal"],
            response.cart_amount["tax_dict"],
            response.cart_amount[
              "grand_total"
            ] /* yhe pr isko likhne j mtlb ki page ko refresh ni krne pdge direct update hojyege kuki y views aare hai  */
          );
        }
      },
    });
  });

  // place the cart item quantity on load
  $(".item_qty").each(function () {
    var the_id = $(this).attr("id");
    var qty = $(this).attr("data-qty");
    $("#" + the_id).html(qty);
  });

  // decrease cart
  $(".decrease_Cart").on("click", function (e) {
    e.preventDefault();

    food_id = $(this).attr("data-id");
    url = $(this).attr("data-url");
    cart_id = $(this).attr("id");

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        // console.log(response);
        if (response.status == "login_required") {
          swal(response.message, "", "info").then(function () {
            window.location = "/login";
          });
        } else if (response.status == "Failed") {
          swal(response.message, "", "error");
        } else {
          $("#cart_counter").html(response.cart_counter["cart_count"]);
          $("#qty-" + food_id).html(response.qty);

          applyCartAmounts(
            response.cart_amount["subtotal"],
            response.cart_amount["tax_dict"],
            response.cart_amount["grand_total"]
          );

          if (window.location.pathname == "/cart/") {
            /* isse sirf cart page p rhege to hi delete hoge   */
            removeCartItem(
              response.qty,
              cart_id
            ); /* with the help of this jaise hi cart decrease krte 0 hoge to automatic delete hjyege */
            checkEmptyCart();
          }
        }
      },
    });
  });

  // DELETE CART ITEM
  $(".delete_Cart").on("click", function (e) {
    e.preventDefault();

    cart_id = $(this).attr("data-id");
    url = $(this).attr("data-url");

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        // console.log(response);
        if (response.status == "Failed") {
          swal(response.message, "", "error");
        } else {
          $("#cart_counter").html(response.cart_counter["cart_count"]);
          swal(response.status, response.message, "success");

          applyCartAmounts(
            response.cart_amount["subtotal"],
            response.cart_amount["tax_dict"],
            response.cart_amount["grand_total"]
          );

          removeCartItem(0, cart_id);
          checkEmptyCart();
        }
      },
    });
  });
  //

  // delete the cart element if the qty is 0 yhe p jaise hi delete krege to vo delete hjyege
  function removeCartItem(cartItemQty, cart_id) {
    if (cartItemQty <= 0) {
      // remove the cart item element
      document.getElementById("cart-item-" + cart_id).remove();
    }
  }

  // check cart item yhe jaise hai cart item m kch bhi ni hoge to cart empty shiw krege

  function checkEmptyCart() {
    let cart_counter = document.getElementById("cart_counter").innerHTML;
    if (cart_counter == 0) {
      document.getElementById("empty-cart").style.display = "block";
    }
  }

  //   cart amounts isko krne se hmlog total vgeere krlege
  function applyCartAmounts(subtotal, tax_dict, grand_total) {
    if (window.location.pathname == "/cart/") {
      $("#subtotal").html(subtotal);
      $("#total").html(grand_total);
// 
      for(key1 in tax_dict){
        console.log(key1)
        for(key2 in tax_dict[key1]){
            console.log(tax_dict[key1][key2])
            $('#tax-'+key1).html(tax_dict[key1][key2])

            // with the help of this we can print dynamic CGST AND SGST data
        }
      }
    }
  }

  // add hour
  $('.add_hour').on('click', function(e){
    e.preventDefault();
    var day = document.getElementById('id_day').value
    var from_hour = document.getElementById('id_from_hour').value
    var to_hour = document.getElementById('id_to_hour').value
    var is_closed = document.getElementById('id_is_closed').checked
    var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
    var url = document.getElementById('add_hour_url').value

    // console.log(day, from_hour, to_hour, is_closed, csrf_token)

    if(is_closed){
        is_closed = 'True'
        condition = "day != ''"
    }else{
        is_closed = 'False'
        condition = "day != '' && from_hour != '' && to_hour != ''"
    }

    if(eval(condition)){
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'day': day,
                'from_hour': from_hour,
                'to_hour': to_hour,
                'is_closed': is_closed,
                'csrfmiddlewaretoken': csrf_token,
            },
            success: function(response){
                if(response.status == 'success'){
                    if(response.is_closed == 'Closed'){
                        html = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>Closed</td><td><a href="#" class="remove_hour" data-url="/vendor/opening-hours/remove/'+response.id+'/">Remove</a></td></tr>';
                    }else{
                        html = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>'+response.from_hour+' - '+response.to_hour+'</td><td><a href="#" class="remove_hour" data-url="/vendor/opening-hours/remove/'+response.id+'/">Remove</a></td></tr>';
                    }
                    
                    $(".opening_hours").append(html)
                    document.getElementById("opening_hours").reset();
                }else{
                    swal(response.message, '', "error")
                }
            }
        })
    }else{
        swal('Please fill all fields', '', 'info')
    }
});

// REMOVE OPENING HOUR
$(document).on('click', '.remove_hour', function(e){
    e.preventDefault();
    url = $(this).attr('data-url');
    
    $.ajax({
        type: 'GET',
        url: url,
        success: function(response){
            if(response.status == 'success'){
                document.getElementById('hour-'+response.id).remove()
            }
        }
    })
})


});
