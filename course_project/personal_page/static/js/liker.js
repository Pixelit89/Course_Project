/**
 * Created by pixelit on 30.11.16.
 */
$(document).ready(function() {
    $('.post-likes').click(function() {
        var id;
        var username;
        id = $(this).attr('data-post-id');
        username = $('.username').attr('data-user-id');
        $.get('/like-blog/', {
            post_id: id,
            user_name: username
        }, function(data) {
            $('.like_count_blog_'+id).html(data);
        });
    });
});
