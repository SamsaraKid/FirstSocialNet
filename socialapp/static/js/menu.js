let menuIsOpen = false

// Показать-скрыть меню
function showHideMenu(){

    if (!menuIsOpen) {
        $('#narrowMenuWrap').removeClass('menuUpAnim')
        $('#narrowMenuWrap').addClass('menuDownAnim')
        $('#narrowMenuWrap').css('height', '460px')
        menuIsOpen = true
    }   else {
        $('#narrowMenuWrap').removeClass('menuDownAnim')
        $('#narrowMenuWrap').addClass('menuUpAnim')
        $('#narrowMenuWrap').css('height', '0px')
        menuIsOpen = false
    }
    setTimeout(function () {
        $('#narrowMenuWrap').removeClass('menuUpAnim')
        $('#narrowMenuWrap').removeClass('menuDownAnim')
        }, 300)
}

$('#menuBut').click(showHideMenu)