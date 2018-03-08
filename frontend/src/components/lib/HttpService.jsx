// import $ from 'jquery';
import {message} from 'antd';

class HttpService {
  constructor() {
  }

  doGet(requestBean) {
    let request = $.ajax({
      url: requestBean.getUrl(),
      method: 'get',
      headers: {'X-Appgo-Token': globalToken},
      data: requestBean.getData(),
      timeout: 10000,
      success: (result) => {
        if (result.errcode) {
          if(result.errcode == 40100) {
            message.error('登录已失效,请点击登出按钮后重新登录', 3);
            return;
          } else {
            console.log(result)
            message.error(`errcode: ${result.errcode}, ${result.errmsg}`);
          }
        }
        this.successCallback = requestBean.getSuccess();
        if (this.successCallback) {
          this.successCallback(result);
        }
      },
      error: (result) => {
        if (result.statusText =='abort') {
            return;
        }
        console.log(result);
        if(result.errcode) {
          message.error(`errcode: ${result.errcode}, ${result.errmsg}`);
        }
        this.errorCallback = requestBean.getError();
        if (this.errorCallback) {
          this.errorCallback(result);
        }
      }
    })
    return request
  }

  doPost(requestBean, params) {
    let option = Object.assign({}, {
      url: requestBean.getUrl(),
      method: 'post',
      timeout: 10000,
      contentType: 'application/json',
      headers: {'X-Appgo-Token': globalToken},
      data: JSON.stringify(requestBean.getData()),
      beforeSend: () => {
        this.beforeSendCallback = requestBean.getBeforeSend();
        if (this.beforeSendCallback) {
          this.beforeSendCallback();
        }
      },
      success: (result)=> {
        if (result.errcode) {
          if(result.errcode == 40100) {
            message.error('登录已失效,请点击登出按钮后重新登录', 3);
            return;
          } else {
            console.log(result)
            message.error(`errcode: ${result.errcode}, ${result.errmsg}`);
          }
        }
        this.successCallback = requestBean.getSuccess();
        if (this.successCallback) {
          this.successCallback(result);
        }
      },
      error: (result)=> {
        console.log(result)
        if(result.errcode) {
          message.error(`errcode: ${result.errcode}, ${result.errmsg}`);
        }
        this.errorCallback = requestBean.getError();
        if (this.errorCallback) {
          this.errorCallback(result);
        }
      }
    }, params)
    $.ajax(option)
  }

  doPut(requestBean) {
    $.ajax({
      url: requestBean.getUrl(),
      method: 'put',
      timeout: 10000,
      contentType: 'application/json',
      headers: {'X-Appgo-Token': globalToken},
      data: JSON.stringify(requestBean.getData()),
      beforeSend: () => {
        this.beforeSendCallback = requestBean.getBeforeSend();
        if (this.beforeSendCallback) {
          this.beforeSendCallback();
        }
      },
      success: (result)=> {
        if (result.errcode) {
          if(result.errcode == 40100) {
            message.error('登录已失效,请点击登出按钮后重新登录', 3);
            return;
          } else {
            console.log(result)
            message.error(`errcode: ${result.errcode}, ${result.errmsg}`);
          }
        }
        this.successCallback = requestBean.getSuccess();
        if (this.successCallback) {
          this.successCallback(result);
        }
      },
      error: (result)=> {
        console.log(result);
        if(result.errcode) {
          message.error(`errcode: ${result.errcode}, ${result.errmsg}`);
        }
        this.errorCallback = requestBean.getError();
        if (this.errorCallback) {
          this.errorCallback(result);
        }
      }
    })
  }

  doDelete(requestBean) {
    $.ajax({
      url: requestBean.getUrl(),
      method: 'delete',
      timeout: 10000,
      headers: {'X-Appgo-Token': globalToken},
      data: requestBean.getData() ? JSON.stringify(requestBean.getData()) : null,
      success: (result) => {
        if (result.errcode) {
          if(result.errcode == 40100) {
            message.error('登录已失效,请点击登出按钮后重新登录', 3);
            return;
          } else {
            console.log(result)
            message.error(`errcode: ${result.errcode}, ${result.errmsg}`);
          }
        }
        this.successCallback = requestBean.getSuccess();
        if (this.successCallback) {
          this.successCallback(result);
        }
      },
      error: (result) => {
        console.log(result);
        if(result.errcode) {
          message.error(`errcode: ${result.errcode}, ${result.errmsg}`);
        }
        this.errorCallback = requestBean.getError();
        if (this.errorCallback) {
          this.errorCallback(result);
        }
      }
    })
  }
}

export default HttpService;
