$(document).ready(function() {
    $('#addData').on('submit', function(event) {
        $.ajax({
            data : {
                item_id : $('#id').val(),
                itemName : $('#itemName').val(),
                quantity : $('#quantity').val(),
                bought : $('#bought').val()

            },
            type : 'POST',
            url : '/insert'
        })
        .done(function(data) {
            if (data.error){
            //todo gówno
            }
            else{
            console.log(data)
            $('#shoppingListTable').append(`<tr><td {% if ${data.bought} == 1 %}style="text-decoration: line-through"{% endif %}> ${data.itemName}</td><td {% if ${data.bought} == 1 %}style="text-decoration: line-through"{% endif %}> ${data.quantity}</td><td><input type="checkbox"{% if ${data.bought} == 1 %}checked{% endif %} disabled></td><td><a href="/bought/${data.id}" class="btn btn-success btn-xs" >Change Item Status</a><a href="/update/${data.id}" class="btn btn-warning btn-xs" data-toggle="modal" data-target="#modalEdit">Edit</a><a href="/delete/${data.id}" class="btn btn-danger btn-xs" onclick="return confirm('Are you sure to delete?')">Delete</a></td></tr>`)
            $('#mymodal').modal('hide')
            }
            })
            event.preventDefault();
        });

    $('button[id^="boughtButton"]').click(function() {
        var id_data = $(this).attr('id').match(/\d+$/)[0];

        $.ajax({
            url: '/bought/' + id_data,
            type: 'PUT',
            success: function() {
                // Zaktualizuj widok w zależności od odpowiedzi z serwera
                console.log(id_data); // Wyświetl odpowiedź w konsoli (do debugowania)
                // Tutaj możesz dodać logikę aktualizacji widoku na podstawie odpowiedzi z serwera
            },
            error: function(xhr, status, error) {
                // Obsługa błędów
                console.error(xhr.responseText);
            }
        });
        event.preventDefault();
    });
    });