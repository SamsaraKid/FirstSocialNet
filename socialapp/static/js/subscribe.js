let sub_but = document.getElementById('subscribe-button')
let unsub_but = document.getElementById('unsubscribe-button')
if (sub_but){sub_but.onclick = f1}
if (unsub_but){unsub_but.onclick = f2}

function f1(){
    let user_id = document.getElementById('user_id').textContent
    let profile_id = document.getElementById('profile_id').textContent
    if (user_id&&profile_id){

        let url = '/subscribe'
        $.ajax(url, {
            method: 'POST',
            data: {'user_id': user_id, 'profile_id': profile_id},
            success: function (responce){
                console.log(responce.mes)
                window.location.href = responce.link},
            error: function (responce){
                console.log(responce.mes)}
        })
    }
    else{
        alert('not ok')
    }
}


function f2(){
    let user_id = document.getElementById('user_id').textContent
    let profile_id = document.getElementById('profile_id').textContent
    if (user_id&&profile_id){

        let url = '/unsubscribe'
        $.ajax(url, {
            method: 'POST',
            data: {'user_id': user_id, 'profile_id': profile_id},
            success: function (responce){
                console.log(responce.mes)
                window.location.href = responce.link},
            error: function (responce){
                console.log(responce.mes)}
        })
    }
    else{
        alert('not ok')
    }
}