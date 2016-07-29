/**
 * Created by Subwin on 2016/7/11.
 */

//tweet
    
    
var bindAddTweetAction = function (after) {
    $('#id-button-add').on('click', function () {
        var self = $(this);
        var content = $('#id-input-content').val();
        var form = {
            'content': content
        };
        var response = function (r) {
            if (r.success) {
                log('add success', r);
                $('#id-input-content').val("");
                var t = tweetTemplate(r.data)
                $(after).after(t);
            }else{
                log('add fail', r)
            }
        };
        weibo.push_tweet(form, response);
    });
};


var bindUpdateTweetAction = function () {
    $('#id-button-submit').on('click', function () {
        log("fuc start");
        var content = $('#id-input-content').val();
        var tweet_id = $('#id-input-content').data('id');
        var form = {
            'content': content,
            'id':tweet_id
        };
        var response = function (r) {
            if (r.success) {
                log('update success', r);
                $('#id-input-content').val("");
                window.location.href = r.next;
            }else{
                log('err, ', err);
            }
        };
        weibo.update_tweet(form, response);
    });
};


var bindAddCommentAction = function () {
    $('#id-button-add').on('click', function () {
        var self = $(this);
        var content = $('#id-input-content').val();
        var id = $('#id-content-comment').data('id')
        var form = {
            'content': content,
            'id': id
        };
        var response = function (r) {
            if (r.success) {
                log('add success', r);
                t = commentTemplate(r.data)
                $('#id-comment-title').after(t);
                $('#id-input-content').val("");
            }else{
                log('err, ', err);
            }
        };
        weibo.push_comment(form, response);
    });
};


var bindDeleteAction = function() {
    $('body').on('click', '.button-delete', function () {
        var self = $(this);
        var tweet_id = this.dataset.id;
        var form = {
            'id': tweet_id
        };
        var response = function (r) {
            console.log(r);
            if (r.success) {
                log(r.message);
                self.closest('.id-one-tweet').remove();
            }else{
                log('err, ', r);
            }
        };
        weibo.delete(form, response)
    });
};


