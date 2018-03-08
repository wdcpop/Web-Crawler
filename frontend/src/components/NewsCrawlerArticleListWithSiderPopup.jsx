import React, { Component } from 'react'
import { Table, Icon, Popconfirm, message, Row, Col, Tooltip, Button, Spin, Form, Select, BackTop, Tabs } from 'antd'
const TabPane = Tabs.TabPane;

// modules
import { renderSearchBar } from './lib/Search'
import apiAddress from './lib/apiAddress';
import { formatTime, reachBottom } from './lib/util'
import HttpService from './lib/HttpService';
import RequestParam from './lib/RequestBean';

// components
import NewsCrawlerArticleList from './NewsCrawlerArticleList'
import SiderPopupWrapper from './lib/SiderPopup/SiderPopupWrapper'


class PreviewBox extends Component {
  constructor(props) {
    super(props)
    this.state = {
      iframeOn: true
    }
  }
  onTabChange(key) {
    if (key == 2) {
      let hide = message.info('已打开原网页预览，可能会有点卡噢，需要关闭时点击左侧的"抓取内容"或关闭侧边栏即可。')
      this.setState({iframeOn: true})
    } else {
      this.setState({iframeOn: false})
    }
  }
  componentWillUnmount() {
    this.setState({iframeOn: false})
  }
  render() {
    if (!this.props.record) {
      return <div></div>
    }

    function stripScripts(s) {
      var div = document.createElement('div');
      div.innerHTML = s;
      var scripts = div.getElementsByTagName('script');
      var i = scripts.length;
      while (i--) {
        scripts[i].parentNode.removeChild(scripts[i]);
      }
      return div.innerHTML;
    }

    return (
        <Tabs type="card" onChange={this.onTabChange.bind(this)}>
          <TabPane tab="抓取内容" key="1">
            <div className="preview-info-box">
              <h1 className="preview-info-header">{this.props.record.title}</h1>
              <div className="preview-info-span">
                <span>{"作者："+this.props.record.name}</span>
                <span>{"来源："+this.props.record.host}</span>
                <span>{"时间："+formatTime(this.props.record.ctime * 1000)}</span>
                <a target="_blank" href={this.props.record.link}>{"原文链接"}</a>
              </div>
              <div className="preview-info-body" dangerouslySetInnerHTML={{__html:stripScripts(this.props.record.content)}}></div>
            </div>
          </TabPane>
          <TabPane tab="原网页" key="2" ref="iframeWrap">
            {this.state.iframeOn && <iframe ref="iframeBox" src={this.props.record.link} style={{position: 'absolute', height: '100%', border: 'none'}}></iframe>}
          </TabPane>
        </Tabs>
    )
  }
}


class NewsCrawlerArticleListWithSiderPopup extends Component {
  constructor(props) {
    super(props)
    this.state = {
      showArticleList: true
    }
    this._closePopup = this._closePopup.bind(this);
    this._resetPopup = this._resetPopup.bind(this);
    this._refreshList = this._refreshList.bind(this);
  }
// <ArticleEdit
// preLink={record.link}
// preTitle={record.title}
// preSource={record.name}
// PreMode={"add"}
// afterSubmitSuccessCallback={this.refs['SiderPopupWrapper']._closeAndCleanElements}
// />
  onClickTitle(item, record, dataIndex) {
    console.log(record);
    this.refs['SiderPopupWrapper']._cleanElements();
    this.refs['SiderPopupWrapper']._openAndFillElements([
      this.props.getRightTopBoxFromRecord(record),
      <PreviewBox record={record}/>
    ]);
  }
  _resetPopup() {
    var self = this;
    this.refs['SiderPopupWrapper']._cleanElements();
    setTimeout(() => {
      self.refs['SiderPopupWrapper']._fillElements([
        this.props.getRightTopBoxNew()
      ]);
    }, 0)
  }
  _closePopup() {
    this.refs['SiderPopupWrapper']._closeAndCleanElements();
  }
  _refreshList() {
    var self = this;
    // self.setState({showArticleList: false})
    // setTimeout(() => {
    //   self.setState({showArticleList: true})
    // }, 100);
    this.refs['NewsCrawlerArticleList']._refreshList()
  }
  render(){
    var self = this;
    return (
      <div>
        <SiderPopupWrapper
          ref="SiderPopupWrapper"
          positon="right"
          onClickReset={this._resetPopup}
          resetBtnTitle="新建一篇崭新的文章"
        >
          {this.state.showArticleList && <NewsCrawlerArticleList
            ref="NewsCrawlerArticleList"
            renderOperation={this.props.renderOperation}
            onClickTitle={this.onClickTitle.bind(this)}
            columnsAlter={this.props.columnsAlter}
          />}
        </SiderPopupWrapper>
      </div>
    )
  }
}

NewsCrawlerArticleListWithSiderPopup.defaultProps = {
  // dependencies from upper component
  renderOperation: (item, record, dataIndex) => { return <div>待集成的编辑区域</div> },
  onClickTitle: (item, record, dataIndex) => {},
  columnsAlter: (columns) => {return columns},
  getRightTopBoxFromRecord: (record) => {return <div>待集成的发表文章区域</div>},
  getRightTopBoxNew: () => {return <div>待集成的发表文章区域</div>}
};

export default NewsCrawlerArticleListWithSiderPopup
