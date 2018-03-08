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
            sourceList: [],
        }
        this.request = new HttpService()
    }
    showModal() {
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
        let reqParam = new RequestParam().setUrl(url).setData(fieldsVals)
            .setSuccess(() => {
                this.setState({
                    editProcessing: false,
                    modalVisible: false
                })
                message.success('添加成功！')
                // self.props.ee.emit('reload_sources');
            })
            .setError(() => {
                this.setState({
                    editProcessing: false,
                    modalVisible: false
                })
                message.error('添加失败！')
            })
        this.request.doPut(reqParam)
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
                                <FormItem label="视图名称（一经确定无法修改）" {...formItemLayout}>
                                    {/*{getFieldDecorator('title', { initialValue: item['title'] })(*/}
                                        <Input
                                        {...getFieldProps('name', {initialValue: item['name']})}
                                        placeholder="请输入视图名称："
                                        />
                                    {/*)}*/}
                                </FormItem>
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