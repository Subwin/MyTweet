/**
 * Created by Subwin on 2016/7/11.
 */

//tweet
    
    
var bindAddTweetAction = function (after_id) {
    $('#id-button-add').on('click', function () {
        var self = $(this);
        var content = $('#id-input-content').val();
        var form = {
            'content': content
        };
        var success = function (r) {
            if (r.success) {
                    console.log('add success', r);
                    $('#id-template-tweet').tmpl(r.data).insertAfter(after_id);
                    $('#id-input-content').val("");
            }
        };
        var error = function (err) {
            log('reg, ', err);
        };
        weibo.push_tweet(form, success, error);
    });
};


var bindAddCommentAction = function () {
    $('#id-button-add').on('click', function () {
        var self = $(this);
        var content = $('#id-input-content').val();
        var id = $('#id-content-comment').attr("tweet_id")
        var form = {
            'content': content,
            'id': id
        };
        var success = function (r) {
            if (r.success) {
                console.log('add success', r);
                $('#id-template-tweet').tmpl(r.data).insertAfter('#id-comment-title');
                $('#id-input-content').val("");
            }
        };
        var error = function (err) {
            log('reg, ', err);
        };
        weibo.push_comment(form, success, error);
    });
};


var bindDeleteAction = function() {
    $('body').on('click', '.button-delete', function () {
        var self = $(this);
        var tweet_id = this.dataset.id;
        var form = {
            'id': tweet_id
        }
        var success = function (r) {
            console.log(r);
            if (r.success) {
                self.parent().remove();
            }
        };
        var error = function (r) {
            console.log(r);
        };
        weibo.delete(form, success, error)
    });
};