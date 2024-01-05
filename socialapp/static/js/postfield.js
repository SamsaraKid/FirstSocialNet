let post = document.getElementById('id_post')

window.addEventListener('load', function () {
    if (post.getElementsByTagName('textarea')[0].value){
       post.setAttribute('style', 'height: 20ex;')
    }})

post.getElementsByTagName('textarea')[0].addEventListener('focusin', function (){
       post.setAttribute('style', 'height: 20ex;')
})

post.getElementsByTagName('textarea')[0].addEventListener('focusout', function (){
    if (!post.getElementsByTagName('textarea')[0].value){
       post.setAttribute('style', 'height: 4ex;')
    }
})

