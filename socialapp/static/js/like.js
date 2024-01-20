function flike(button, id, type){
    let url = '/like'
    $.ajax(url, {
        method: 'POST',
        data: {'id': id, 'type': type},
        success: function (responce){
            console.log(responce.mes)
            change_like_stat(button, responce.mes, responce.num_likes)},
        error: function (responce){
            console.log(responce.mes)}
    })
}

function change_like_stat(button, mes, num_likes){
    img = button.getElementsByTagName('img')[0]
    num = button.getElementsByTagName('h3')[0]
    if (mes === 'Лайк поставлен'){
        img.setAttribute('src', '/static/img/like.png')
        if (num){
            num.textContent = String(num_likes)
        } else {
            let likes_count = document.createElement('h3')
            likes_count.textContent = num_likes
            button.appendChild(likes_count)
        }
    } else {
        img.setAttribute('src', '/static/img/like_not.png')
        if (num){
            if (Number(num_likes) > 0){
            num.textContent = String(num_likes)
            } else {
                button.removeChild(num)
            }
        }
    }
}