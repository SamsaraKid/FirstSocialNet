function change_status(user_id, community_id, stat){
    let url = '/changeadminstatus'
    $.ajax(url, {
    method: 'POST',
    data: {'user_id': user_id, 'community_id': community_id, 'stat': stat},
    success: function (responce){
        console.log(responce.mes)
        location.reload()},
    error: function (responce){
        console.log(responce.mes)}
    })
}
