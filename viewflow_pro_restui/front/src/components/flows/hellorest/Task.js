import React, { Component } from 'react'
import {alert} from 'notie'
import { Alert, Button, Form, Modal, ModalHeader, ModalBody, ModalFooter, Progress } from 'reactstrap';

import TextInput from '../../TextInput'
import * as API from '../../../api'

export default class Task extends Component {
  constructor(props) {
    super(props)
    this.closeOnParent = props.close
  }

  state = {
    inProgress: false,
    text: "",
    errors: {}
  }

  close = () => {
    if(!this.state.inProgress) {
      this.closeOnParent()
    }
  }

  setProgress = inProgress => {
    this.setState({inProgress: inProgress})
  }
  render() {
    return (
      <Modal isOpen={true} toggle={this.close}>
        {this.state.inProgress?<Progress animated value="100" className="progress--top"/>:""}
        <ModalHeader toggle={this.close}>Start Flow</ModalHeader>
        <ModalBody>
          {this.state.errors.non_field_errors? <Alert color="danger">{this.state.errors.non_field_errors}</Alert>:""}
          <Form>
            <TextInput name="text" label="Message" value={this.state.value} error={this.state.errors.text}
                       onChange={this.handleTextChange} getRef={input => input && input.focus()}/>
          </Form>
        </ModalBody>
        <ModalFooter>
          <Button color="primary" onClick={this.startFlow} disabled={this.state.inProgress}>Start</Button>{' '}
          <Button color="secondary" onClick={this.close} disabled={this.state.inProgress}>Cancel</Button>
        </ModalFooter>
      </Modal>
    )
  }
}
