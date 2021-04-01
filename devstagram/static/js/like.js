$(".pic_pk").on('click', function (e) {
    e.preventDefault();
    let link = $(this).attr('href')
    let curSpan = $(this).siblings('.like-span')
    let curHeart = $(this).children('.fa-heart')
    $.ajax({
        cache: false,
        type: 'GET',
        url: link,
        success: function (data) {
            let likes = data['likes']
            let userId = data['user_id']
            let idList = data['id_list']
            let action = data['action']
            curSpan.text(likes + ' likes')

            if (action === 'unlike') {
                curHeart.removeClass('fas')
                curHeart.addClass('far')
            } else {
                curHeart.removeClass('far')
                curHeart.addClass('fas')
            }
        }
    })

})
