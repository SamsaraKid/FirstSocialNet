let sub_but = document.getElementById('subscribe-button')
if (sub_but){sub_but.onclick = f1}

function f1(){
    let user_id = document.getElementById('user_id').textContent
    let profile_id = document.getElementById('profile_id').textContent
    if (user_id&&profile_id){
        let url = '/subscribe'
        $.ajax(url, {
            method: 'POST',
            data: {'user_id': user_id, 'profile_id': profile_id},
            success: function (responce){
                console.log(responce.mes)},
            error: function (responce){
                console.log(responce.mes)}
        })
        if (sub_but.classList.contains('button-inverted')){
            sub_but.classList.remove('button-inverted')
            sub_but.textContent = 'Подписаться'}
        else {
            sub_but.classList.add('button-inverted')
            sub_but.textContent = 'Отписаться'}
    }
    else{
        alert('not ok')
    }
}

