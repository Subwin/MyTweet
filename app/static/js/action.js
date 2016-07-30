/**
 * Created by Subwin on 2016/7/11.
 */

//tweet
    
var longTimeAgo = function(unixTime) {
            var timeAgo = function(time, ago) {
              return Math.round(time) + ago;
            };
            var past = parseInt(unixTime);
            var now = Math.round(new Date().getTime() / 1000);
            var ago = (now - past) / 60;
            // log('time ago', e, past, now, ago);
            var yet = 5;
            var oneHour = 60;
            var oneDay = oneHour * 24;
            // var oneWeek = oneDay * 7;
            var oneMonth = oneDay * 30;
            var oneYear = oneMonth * 12;
            var s = '';
            if (ago < yet) {
                s = '刚刚';
            } else if (ago < oneHour) {
                s = timeAgo(ago, '分钟前');
            } else if (ago < oneDay) {
                s = timeAgo(ago/oneHour, '小时前');
            } else if (ago < oneMonth) {
                s = timeAgo(ago / oneDay, '天前');
            } else if (ago < oneYear) {
                s = timeAgo(ago / oneMonth, '月前');
            }
            return s;
            };

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
                var t = tweetTemplate(r.data);
                // longTimeAgo()
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


