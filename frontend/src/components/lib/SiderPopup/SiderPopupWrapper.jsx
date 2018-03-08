import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import { Table, Icon, Popconfirm, message, Row, Col, Tooltip, Button, Spin, Form, Select, BackTop, Tabs } from 'antd'
const TabPane = Tabs.TabPane;
import { Link } from 'react-router'

import './SiderPopupWrapper.css'

var isContainerResizing = false;

class SiderPopupWrapper extends Component {
  constructor(props) {
    super(props)
    this.state = {
      activated: false,
      renderedElement: null
    }
    this._openAndFillElements = this._openAndFillElements.bind(this);
    this._closeAndCleanElements = this._closeAndCleanElements.bind(this);
    this._fillElements = this._fillElements.bind(this);
    this._cleanElements = this._cleanElements.bind(this);
    this._open = this._open.bind(this);
    this._close = this._close.bind(this);
    this.btnMoved = false;
    this.btnOffsetRight = null;
    this.btnOffsetTop = null;
    this.btnOffsetBottom = null;
  }
  componentDidMount() {
    this.addContainerDraggableEffect()
  }
  componentWillUnmount() {
    this._closeAndCleanElements()
    this.cleanupDraggableEffect()
  }
  addContainerDraggableEffect() {
    var self = this;
    var $ = jQuery;
    var container = $('.sider-popup-sider'),
      handleBtn = $('.sider-popup-container-resize-btn');

    handleBtn.on('mousedown', function (e) {
      isContainerResizing = true;
    });

    $(document).on('mousemove', function (e) {

      // we don't want to do anything if we aren't resizing.
      if (!isContainerResizing)
        return;

      // x
      var windowWidth = $(window).width();
      var mouseX = e.clientX;
      var offsetRight = windowWidth - mouseX;
      self.btnOffsetRight = offsetRight;

      // y
      var containerHeight = container.height();
      var containerWindowTop = container.offset().top - $(window).scrollTop();
      var mouseY = e.clientY;

      if (mouseY <= 80) {
        mouseY = 80
      }
      if (mouseY >= containerHeight - 40) {
        mouseY = containerHeight - 40
      }

      var offsetTop = mouseY - containerWindowTop;
      var offsetBottom = containerHeight - offsetTop;
      self.btnOffsetTop = offsetTop;
      self.btnOffsetBottom = offsetBottom;

      self.btnMoved = true;
      self.setResizedElementsIntoPosition();
    }).on('mouseup', function (e) {
      // stop resizing
      isContainerResizing = false;
    });
  }
  setResizedElementsIntoPosition() {
    var self = this;
    if (self.btnMoved) {
      $('.sider-popup-sider').css('width', self.btnOffsetRight);
      $('.spbox-item-0').css('height', self.btnOffsetTop);
      $('.spbox-item-1').css('height', self.btnOffsetBottom);
      $('.sider-popup-container-resize-btn').css('top', self.btnOffsetTop);
    }
  }
  cleanupDraggableEffect() {
    $('.sider-popup-container-left-side-btn-area').off('mousedown');
  }
  _openAndFillElements(boxElements) {
    var self = this;
    this._open();
    setTimeout(() => {
      self._fillElements(boxElements);
    }, 50);
  }
  _closeAndCleanElements() {
    this._cleanElements();
    this._close();
  }
  _fillElements(boxElements) {
    this.setState({
      renderedElement: this.getRenderingElements(boxElements)
    });
    this.setResizedElementsIntoPosition();
  }
  _open() {
    let self = this;
    this.setState({
      activated: true
    });
  }
  _cleanElements() {
    this.setState({
      renderedElement: null
    })
  }
  _close() {
    this.setState({
      activated: false
    })
    $('.sider-popup-container-resize-btn').css('top', '');
  }
  getRenderingElements(boxElements) {
    var self = this;
    let boxNum = boxElements.length;
    if (boxNum <= 0) {
      return (<div></div>)
    }
    var content = [];

    boxElements.forEach((elem, index) => {
      content[index] = (
        <div className={"sider-popup-box spbox-num-"+boxNum+" spbox-item-"+index} key={index}
        >
          <div className={"sider-popup-box-inner"}>
            <div className={"sider-popup-box-inner-inner"}>
              {elem}
            </div>
          </div>
        </div>
      )
    })

    return content;
  }
  render() {
    var self = this;
    return (
      <div className={"sider-popup-wrap" + (this.state.activated ? " active" : " inactive")} ref="siderPopupWrap">
        <div className={"sider-popup-body"}>
          {this.props.children}
        </div>
        <div className={"sider-popup-sider"} ref="siderPopupSider">
          {this.state.renderedElement}
          <div className="sider-popup-container-left-side-btn-area">
            <Button className={"sider-popup-container-resize-btn"} icon="shrink"/>
            <Button className={"sider-popup-close-btn"} onClick={this._closeAndCleanElements} icon="right" />
            <Button className={"sider-popup-reset-btn"} onClick={typeof this.props.onClickReset === 'function' ? this.props.onClickReset : function(){console.log('no prop')}} icon="retweet" />
          </div>

        </div>
      </div>
    )
  }
}

SiderPopupWrapper.defaultProps = {
  // dependencies from upper component
  onClickReset: () => {}
};

export default SiderPopupWrapper;
