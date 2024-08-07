

let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
    // console.log(place);
    var geocoder = new google.maps.geometry()
    var address = document.getElementById('id_address').value

    geocoder.geocode({'address': address}, function(result, status){
        if(status == google.maps.GeocoderStatus.Ok){
            var latitude = result[0].geometry.lat();
            var longitude = result[0].geometry.lng();

            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);

            $('#id_address').val(address);

        }
    });

    // loop through the address compnents and assign other address data.
    for(var i =0; i< place.address_components.length; i ++){
        for(var j =0; j< place.address_components[i].types.length; j ++){
            // get country
            if(place.address_components[i].types[j] == 'country'){
                $('#id_country').val(place.address_components[i].long_name);
            }
            // get state
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name);
            }
            // get city
            if(place.address_components[i].types[j] == 'locality'){
                $('#id_city').val(place.address_components[i].long_name);
            }
            // get pin_code
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_pin_code').val(place.address_components[i].long_name);
            }else{
                $('#id_pin_code').val(" ");
            }
        }
    }

    

}




$(document).ready(function(){
    //Adding to the cart
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        
        var food_id = $(this).attr('data-id');
        var url = $(this).attr('data-url');

        var data={
            food_id : food_id,
        };
        $.ajax({
            
            type : 'GET',
            url : url,
            data : data,
            success: function(response){
                console.log(response);
            },
            error: function(xhr, status,error){
                console.log(xhr.responseText);
            }

        });
    });

    // place the cart item quantity on load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })
});

