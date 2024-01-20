let post = document.getElementById('id_post')

if (post){
    window.addEventListener('load', function () {
    if (post.getElementsByTagName('textarea')[0].value){
       post.setAttribute('style', 'height: 20ex;')
    }})

// post.getElementsByTagName('textarea')[0].addEventListener('focusin', function (){
//        post.setAttribute('style', 'height: 20ex;')
// })
//
// post.getElementsByTagName('textarea')[0].addEventListener('focusout', function (){
//     if (!post.getElementsByTagName('textarea')[0].value){
//        post.setAttribute('style', 'height: 4ex;')
//     }
// })

    post.addEventListener('click', function (){
           post.setAttribute('style', 'height: 20ex;')
    })

    document.addEventListener('click', (e) =>{
        const withinBoundaries = e.composedPath().includes(post)
        if (!withinBoundaries && !post.getElementsByTagName('textarea')[0].value) {
            post.setAttribute('style', 'height: 4ex;')
        }
    })
}


// кнопка выбора фото
$('.input-file input[type=file]').on('change', function(){
	let file = this.files[0]
	$(this).closest('.input-file').find('.input-file-text').html(file.name)
})

