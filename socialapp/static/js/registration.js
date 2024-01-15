$('#add_new_city').click(f1)

function f1(){
    $('#id_city_tr').toggle()
    $('#id_country_tr').toggle()
    $('#id_city_custom_tr').toggle()
    if ($('#id_country_tr').is(':visible')){
        $('#add_new_city').text('Вернуться к списку городов')
        $('#id_city_custom_sign').prop('checked', true)
    }
    else{
        $('#add_new_city').text('Добавить новый город')
        $('#id_city_custom_sign').prop('checked', false)
    }
}