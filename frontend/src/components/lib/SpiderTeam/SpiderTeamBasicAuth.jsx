var React = require('react');
var ReactDOM = require('react-dom');
var Modal = require('antd/lib/modal');
var Input = require('antd/lib/input');
var message = require('antd/lib/message');

/**
 * Do Ajax
 * @param apiUrl {string} e.g. 'http://localhost:8085/do_something'
 * @param callbackGood {function}
 * @param callbackError {function}
 */
function fetchGet(apiUrl, basicAuthTicket, callbackGood, callbackError)
{
  var xhr = new XMLHttpRequest();
  xhr.onload = function(){
    if (this.status >= 200 && this.status < 300) {
      var result = JSON.parse(xhr.responseText);
      callbackGood(result);
    } else {
      callbackError({
        status: this.status,
        statusText: xhr.statusText
      });
    }
  };
  xhr.onerror = function () {
    callbackError({
      status: this.status,
      statusText: xhr.statusText
    });
  };
  xhr.open('GET', apiUrl, true);
  xhr.setRequestHeader("Authorization", basicAuthTicket);
  // xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  var sendParam = null;
  xhr.send(sendParam);

  // if your wanna cancel Ajax: call xhr.abort();
  return xhr
}



var SpiderTeamBasicAuth = React.createClass({
  displayName: 'SpiderTeamBasicAuth',

  getInitialState: function() {
    return {
      didMount: false,
      authPassed: false
    }
  },

  _auth: function(ticket) {
      var self = this;
      fetchGet(this.props.authAddress, ticket, function() {
        window.localStorage.setItem("spiderTeamAuthTicket", ticket);
        console.log('验证成功');
        message.success('验证成功');
        self.setState({authPassed: true});
      }, function() {
        console.log('验证失败');
        message.error('验证失败');
      });
  },

  tryAuth: function() {
    var self = this;
    var ele1 = document.getElementById("input-username");
    var ele2 = document.getElementById("input-password");
    if (ele1.value && ele2.value) {
      var basicAuthTicket = "Basic " + btoa(ele1.value+":"+ele2.value);
      self._auth(basicAuthTicket)
    }
  },

  componentDidMount: function() {
    var ticket = window.localStorage.getItem("spiderTeamAuthTicket");
    this._auth(ticket)
    this.setState({didMount: true});
  },

  render: function() {
    var self = this;

    return this.state.authPassed ?
    React.createElement(
      'div',
      { key: 0 },
      this.props.children
    ) :
    React.createElement(
      Modal,
      {
        key: 0,
        title: "请输入验证信息",
        visible: !this.state.authPassed,
        onOk: function() {self.tryAuth()},
        onCancel: function() {},
      },
      [
        React.createElement(
          Input,
          {
            key: 0,
            id: "input-username",
            placeholder: "用户名",
            value: 'baoer'
          },
          null
        ),
        React.createElement(
          Input,
          {
            key: 1,
            id: "input-password",
            placeholder: "密码"
          },
          null
        )
      ]
    );
  }
});

module.exports = SpiderTeamBasicAuth;