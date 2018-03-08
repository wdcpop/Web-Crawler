import React, {Component} from 'react';
import {Icon, Input, Button, Form, Row, Col} from 'antd';

const InputGroup = Input.Group;
const FormItem = Form.Item;

let Search = React.createClass({
  getInitialState(){
    return {
      value: this.props.value || '',
      loading: false
    }
  },
  handleInputChange(e){
    var v = e.target.value
    this.props.callbackChange && this.props.callbackChange(v);
    this.setState({
      value: v
    });
  },
  handleSearch(e){
    e.preventDefault();
    this.props.callbackParent && this.props.callbackParent(this.state.value);
  },
  componentWillReceiveProps(nextProp) {
    this.setState({ value: nextProp.value })
  },
  render(){
    return (
        <Form horizontal className="advanced-search-form" onSubmit={this.handleSearch}>
          <Row>
            <Col span="22">
              <FormItem wrapperCol={{span:23}}>
                <Input
                    type="text"
                    placeholder={this.props.placeholder || "Search..."}
                    value={this.state.value}
                    onChange={this.handleInputChange}
                />
              </FormItem>
            </Col>
            <Col span="2">
              <Button
                  type="ghost"
                  htmlType="submit"
                  shape="circle"
                  size="large"
              >
                <Icon type="search"/>
              </Button>
            </Col>
          </Row>
        </Form>
    )
  }
});

Search = Form.create()(Search);

export function renderSearchBar(placeholder, value, callbackNewInput, callbackChange) {
  return <Search
      placeholder={placeholder}
      value={value}
      callbackParent={callbackNewInput}
      callbackChange={callbackChange}
  />
}

export default Search
