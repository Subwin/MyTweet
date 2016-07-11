/**
 * Created by gua on 7/6/16 1:48:01
 */

// log
var log = function () {
    console.log(arguments);
};


// form 把keys的值全部取到，保存到form
var formFromKeys = function(keys, prefix) {
    var form = {};
    for(var i = 0; i < keys.length; i++) {
        var key = keys[i];
        var tagid = prefix + key;
        var value = $('#' + tagid).val();
        if (value.length < 1) {
            // alert('字段不能为空');
            break;
        }
        form[key] = value;
    }
    return form;
};

// weibo API
var weibo = {};

weibo.post = function(url, form, success, error) {
    var data = JSON.stringify(form);
    var request = {
        url: url,
        type: 'post',
        contentType: 'application/json',
        data: data,
        success: function (r) {
            log('post success', url, r);
            success(r);
        },
        // 以上两个success是不一样的，上面的代表成功返回后回调，下面的是一个函数。
        error: function (err) {
            log('post err', url, err);
            error(err);
        }
    };
    $.ajax(request);
};

weibo.register = function(form, success, error) {
    var url = '/register';
    this.post(url, form, success, error);
};

weibo.login = function(form, success, error) {
    var url = '/login';
    this.post(url, form, success, error);
};

weibo.push_tweet = function (form, success, error) {
    var url = '/timeline';
    this.post(url, form, success, error);
};

weibo.push_comment = function (form, success, error) {
    var id = form['id'];
    var url = '/tweet/comments/' + id;
    this.post(url, form, success, error);
};

weibo.delete = function (form, success, error) {
    var tweet_id = form['id'];
    var url = '/tweet/delete/' + tweet_id;
    this.post(url, form, success, error);
};