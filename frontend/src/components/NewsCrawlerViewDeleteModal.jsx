import React, { Component } from 'react'
import { Table, Icon, Popconfirm, message, Row, Col, Tooltip, Button, Spin, Form, Input, Select, BackTop, Modal, Checkbox, Radio, Switch } from 'antd'
const RadioGroup = Radio.Group;
const FormItem = Form.Item;
import { Link } from 'react-router'
import EventEmitter from 'events'

// modules
import apiAddress from './lib/apiAddress';
import HttpService from './lib/HttpService';
import RequestParam from './lib/RequestBean';


class NewsCrawlerViewAddModal extends Component {
    constructor(props, context) {
        super(props, context)
        this.state = {
            modalVisible: false,
            editProcessing: false,
            viewList: [],
        }
        this.request = new HttpService()
    }
    showModal() {
        this.initViews()
        this.setState({
            modalVisible: true,
        });
    }
    handleEditModelOk() {
        this.setState({
            editProcessing: true
        })
        this.handleFormSubmit()
    }
    handleEditModelCancel() {
        this.setState({
            modalVisible: false,
        });
    }
    onRadioChange(e) {
        this.setState({
            proxy_type: e.target.value,
        });
    }
    handleFormSubmit(e) {
        var self = this
        typeof e !== 'undefined' && e.preventDefault();
        console.log('Received values of form:', this.props.form.getFieldsValue());

        let url = apiAddress.newsCrawler.views;
        let fieldsVals = this.props.form.getFieldsValue();
        console.log(fieldsVals)
        let reqParam = new RequestParam().setUrl(url).setData(fieldsVals)
            .setSuccess(() => {
                this.setState({
                    editProcessing: false,
                    modalVisible: false
                })
                message.success('删除成功！')
                // self.props.ee.emit('reload_sources');
            })
            .setError(() => {
                this.setState({
                    editProcessing: false,
                    modalVisible: false
                })
                message.error('删除失败！')
            })
        this.request.doDelete(reqParam)
    }
    componentDidMount() {
        this.initViews()
    }
    initViews() {
        var self = this
        let url = apiAddress.newsCrawler.views;
        let reqParam = new RequestParam().setUrl(url)
            .setSuccess((d) => {
                var viewList = d['data'];
                self.setState({viewList: viewList})
            })
            .setError(() => {
                console.log('get views err!');
                this.setState({
                    editProcessing: false,
                    modalVisible: false
                })
            })
        this.request.doGet(reqParam)
    }
    componentWillUnmount() {

    }
    render() {
        var self = this;
        var item = this.props.item || {}

        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        }

        const { getFieldProps, getFieldsValue } = this.props.form;

        const radios = this.state.viewList.map(function(item) {
            return <Radio key={item['name']} value={item['name']}>{item['name']}</Radio>
        })

        return (
            <div style={this.props.inline ? {display: 'inline-block'}: {display: 'block'}}>
                <div onClick={self.showModal.bind(this)}>
                    {this.props.children}
                </div>
                {this.state.modalVisible && <Modal width={800} title="添加视图" visible={self.state.modalVisible}
                                                   onOk={self.handleEditModelOk.bind(this)}
                                                   onCancel={self.handleEditModelCancel.bind(this)}
                                                   confirmLoading={this.state.editProcessing}
                                                   okText="OK" cancelText="Cancel"
                >
                    <Form onSubmit={this.handleFormSubmit.bind(this)}>
                        <Row>
                            <Col>
                                <RadioGroup
                                    {...getFieldProps('name', {initialValue: item['name'] || ''})}
                                >
                                    {radios}
                                </RadioGroup>
                            </Col>
                        </Row>
                    </Form>

                </Modal>}
            </div>
        )
    }
}

NewsCrawlerViewAddModal = Form.create()(NewsCrawlerViewAddModal);

// NewsCrawlerViewEditModal.defaultProps = {
//     // dependencies from upper component
//     item: {}
// };

export default NewsCrawlerViewAddModal