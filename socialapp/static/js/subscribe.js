let sub_but = document.getElementById('subscribe-button')
if (sub_but){sub_but.onclick = f1}

function f1(){
    let profile_id = document.getElementById('profile_id')
    let community_id = document.getElementById('community_id')
    let object_id = ''
    let type = ''
    console.log('f1')
    if (profile_id){
        object_id = profile_id.textContent
        type = 'profile'
    } else if (community_id){
        object_id = community_id.textContent
        type = 'community'
    }
    if (object_id){
        let url = '/subscribe'
        $.ajax(url, {
            method: 'POST',
            data: {'object_id': object_id, 'type': type},
            success: function (responce){
                console.log(responce.mes)
                if (type === 'community'){
                    location.reload()}},
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

