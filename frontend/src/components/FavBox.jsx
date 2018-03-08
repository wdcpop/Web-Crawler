import React, { Component } from 'react'
import { Icon, Popconfirm, message, Row, Col, Tooltip, Button, Spin, Form, Select, BackTop, notification, Switch, Popover } from 'antd'
import { Link } from 'react-router'

var Table = require('antd/lib/table');
import {tableDecoratorAddColumnCloseButton, tableDecoratorAddColumnWidthAlter} from './lib/AntOverride/overrideTable'
var Table = tableDecoratorAddColumnCloseButton(Table);

import EventEmitter from 'events'
var favEE = new EventEmitter();



function getFavObj(uid) {
  var favJson = window.localStorage.getItem(uid+"FavJson") || '{}';
  return JSON.parse(favJson)
}

function getFavList(uid) {
  var favObj = getFavObj(uid)
  var favList = Object.keys(favObj).map((key, index) => {
    return favObj[key]
  });
  return favList.reverse()
}

function setFavObj(favObj, uid) {
  window.localStorage.setItem(uid+"FavJson", JSON.stringify(favObj));
}

//所有收藏对象0.5天过期
function cleanupOutdatedItemsInFavObj(uid) {
  var favObj = getFavObj(uid)
  for (var id in favObj) {
    if (favObj.hasOwnProperty(id)) {
      if (Date.now() - favObj[id].favTime > 3600 * 12 * 1000) {
        delete favObj[id];
      }
    }
  }
  setFavObj(favObj, uid)
}

class OperationHeart extends Component {
  constructor(props, context) {
    super(props, context)

    var record = this.props.record || {}
    var favObj = getFavObj(this.props.uid)
    this.state = {
      hearted: favObj[record.id] || false
    }
    this.updateFavList = this.updateFavList.bind(this)
    cleanupOutdatedItemsInFavObj(this.props.uid)
    // console.log(2)
    favEE.on(this.props.uid+'FavUpdated', (fromClass) => {
      this.refresh()
    });
  }

  refresh() {
    var record = this.props.record || {}
    var favObj = getFavObj(this.props.uid)
    // console.log(favObj)
    this.setState({
      hearted: favObj[record.id] || false
    })
  }

  updateFavList() {
    // console.log(this.state.hearted)
    // console.log(this.props.record)
    var record = this.props.record
    if (!record || !record.id) {
      console.log('record not found for adding to fav')
      return
    }
    var r = record

    var favObj = getFavObj(this.props.uid)
    if (this.state.hearted) {
      r.favTime = Date.now()
      favObj[r.id] = r
    } else {
      delete favObj[r.id];
    }
    setFavObj(favObj, this.props.uid)
    favEE.emit(this.props.uid+'FavUpdated', 'OperationHeart');
  }

  render() {
    return (
      <Icon type={this.state.hearted ? "heart" : "heart-o"} onClick={(e) => {
        this.setState({hearted: !this.state.hearted}, this.updateFavList)
      }}/>
    )
  }
}


class FavTable extends Component {
  constructor(props, context) {
    super(props, context)
    this.state = {
      favList: getFavList(this.props.uid)
    }
    // console.log(1)
    favEE.on(this.props.uid+'FavUpdated', (fromClass) => {
      if (fromClass != 'FavTable') {
        this.setState({
          favList: getFavList(this.props.uid)
        })
      }
    });
  }

  render() {

    var columns = [{
      title: '标题',
      index: 'title',
      dataIndex: 'title',
      width: 200,
      render: (item, record, dataIndex) => {
        return <a href="javascript:void(0)" onClick={(e) => {
          //console.log(jQuery(e.target));
          //jQuery(e.target).addClass('news-viewed');
          this.props.onClickTitle(item, record, dataIndex)
        }}>
          {item}
        </a>
      }
    },{
      title: '来源',
      index: 'source',
      dataIndex: 'name',
      width: 50
    },{
      title: '收藏时间',
      index: 'favTime',
      dataIndex: 'favTime',
      width: 50,
      render: (text, record) => {
        var d = new Date(text),
          month = '' + (d.getMonth() + 1),
          day = '' + d.getDate(),
          year = d.getFullYear(),
          hour = '' +d.getHours(),
          min = '' +d.getMinutes(),
          sec = '' +d.getSeconds();

        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;
        if (hour.length < 2) hour = '0' + hour;
        if (min.length < 2) min = '0' + min;
        if (sec.length < 2) sec = '0' + sec;

        return [hour, min, sec].join(':')
      }
    },{
      title: '网表时间',
      index: 'ctime',
      dataIndex: 'ctime',
      width: 50,
      render: (text, record) => {
        var d = new Date(text * 1000),
          month = '' + (d.getMonth() + 1),
          day = '' + d.getDate(),
          year = d.getFullYear(),
          hour = '' +d.getHours(),
          min = '' +d.getMinutes(),
          sec = '' +d.getSeconds();

        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;
        if (hour.length < 2) hour = '0' + hour;
        if (min.length < 2) min = '0' + min;
        if (sec.length < 2) sec = '0' + sec;

        return [hour, min].join(':')
      }
    },{
      title: '操作',
      index: 'operations',
      width: 50,
      render: (record) => {
        return <div>
          <a href="javascript:void(0)">
            <Icon type="search" onClick={() => {
              this.setState({keyword: record.title}, () => {
                this.props.handleSearchInput && this.props.handleSearchInput(record.title, true)
              })
            }}/>
          </a>
          <span className="ant-divider"></span>
          <a href="javascript:void(0)">
            <Icon type="delete" onClick={() => {
              var favObj = getFavObj(this.props.uid)
              delete favObj[record.id]
              setFavObj(favObj, this.props.uid)
              var newFavList = this.state.favList.filter((item, index) => {
                return item.id !== record.id
              })
              this.setState({favList: newFavList})

              favEE.emit(this.props.uid+'FavUpdated', 'FavTable')
            }}/>
          </a>
        </div>
      }
    }]

    columns = this.props.tableAlter ? this.props.tableAlter(columns) : columns

    return (
      <div>
        <div>{'（小贴士：程序将自动清除超过12小时的收藏，无需手动清理哦！）'}</div>
        <Table
          columns={columns}
          dataSource={this.state.favList.slice(0, 5)}
          pagination={false}
          rowKey={record => record.id}
          size="small"
        />
        <div style={{textAlign: 'center'}}>{this.state.favList.length > 5 ? '...': ''}</div>
      </div>
    )
  }
}


export default class FavBox {
  constructor(uid) {
    class NewOperationHeart extends Component {
      render() {
        return <OperationHeart
          record={this.props.record}
          uid={uid}
        />
      }
    }

    class NewFavTable extends Component {
      render() {
        return <FavTable
          handleSearchInput={this.props.handleSearchInput.bind(this)}
          onClickTitle={this.props.onClickTitle.bind(this)}
          tableAlter={this.props.tableAlter && this.props.tableAlter.bind(this)}
          uid={uid}
        />
      }
    }

    this.getFavObj = () => { getFavObj(uid) }
    this.OperationHeart = NewOperationHeart
    this.FavTable = NewFavTable
  }
}
