class RequestBean {
  constructor() {
  }

  setUrl(url) {
    this.url = url;
    return this;
  }

  getUrl() {
    return this.url;
  }

  setData(data) {
    this.data = data;
    return this;
  }

  getData() {
    return this.data;
  }

  setBeforeSend(beforeSend) {
    this.beforeSend = beforeSend;
    return this;
  }

  getBeforeSend() {
    return this.beforeSend;
  }

  setSuccess(success) {
    this.success = success;
    return this;
  }

  getSuccess() {
    return this.success;
  }

  setError(error) {
    this.error = error;
    return this;
  }

  getError() {
    return this.error;
  }
}

export default RequestBean;
