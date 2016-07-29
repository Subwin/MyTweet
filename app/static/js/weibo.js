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

weibo.ajax = function(url, method, form, response) {
    var request = {
        url: url,
        type: method,
        contentType: 'application/json',
        // 回调函数中的r就是返回的对象
        success: function (r) {
            log('post success', url, method, form, r);
            response(r);
        },
        // 以上两个success是不一样的，上面的代表成功返回后回调，下面的是一个函数。
        error: function (err) {
            r = {
                success: false,
                message: '失败',
                data: err
            };
            log('weibo err', url, err);
            response(r);
        }
    };
    if(method == 'post') {
        var data = JSON.stringify(form);
        request.data = data;
    }
    $.ajax(request);
};


weibo.get = function(url, response) {
    var method = 'get';
    var form = {};
    this.ajax(url, method, form, response);
};

weibo.post = function(url, form, response) {
    var method = 'post';
    this.ajax(url, method, form, response);
};


weibo.register = function(form, response) {
    var url = '/register';
    this.post(url, form, response);
};

weibo.login = function(form, response) {
    var url = '/login';
    this.post(url, form, response);
};

weibo.push_tweet = function (form, response) {
    var url = '/api/tweet/add';
    this.post(url, form, response);
};

weibo.push_comment = function (form, response) {
    var id = form['id'];
    var url = '/api/tweet/comments/' + id;
    this.post(url, form, response);
};

weibo.delete = function (form, response) {
    var tweet_id = form['id'];
    var url = '/api/tweet/delete/' + tweet_id;
    this.post(url, form, response);
};

weibo.update_tweet = function (form, response) {
    var tweet_id = form['id'];
    var url = '/api/tweet/update/' + tweet_id;
    this.post(url, form, response);
};

weibo.get_all_tweets = function (response) {
    var url = '/api/tweets';
    this.get(url, response)
};
