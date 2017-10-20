import React, { Component } from 'react'
import ui from 'redux-ui';
import { Alert, Button, Form, Modal, ModalHeader, ModalBody, ModalFooter, Progress } from 'reactstrap';
import { connect } from 'react-redux'
import { push } from 'react-router-redux'

import TextInput from '../../../components/TextInput'
import { apiErrorReducer } from '../../../reducers/ui/api'
import { start } from '../../../actions/hellorest'

export class Start extends Component {
  state = {
    text: "",
  }

  close = () => {
    this.props.close()
  }

  startFlow = () => {
    this.props.start(this.state.text)
  }

  handleTextChange = (event) => {
    this.setState({text: event.target.value});
  }

  render() {
    const errors = this.props.ui.errors

    return (
      <Modal isOpen={true} toggle={this.close}>
        {this.state.inProgress?<Progress animated value="100" className="progress--top"/>:""}
        <ModalHeader toggle={this.close}>Start Flow</ModalHeader>
        <ModalBody>
          {errors.non_field_errors? <Alert color="danger">{errors.non_field_errors}</Alert>:""}
          <Form>
            <TextInput name="text" label="Message" value={this.state.value} error={errors.text}
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

const mapDispatchToProps = (dispatch, ownProps) => ({
    start: async (text) => {
      const response = await dispatch(start(text))
      if(!response.error) {
        ownProps.onComplete()
        dispatch(push('../'))
      }
    },
    close: () => {
      ownProps.onComplete()
      dispatch(push('../'))
    }
})

export default connect(
  null,
  mapDispatchToProps
)(
  ui({
    key: 'auth',
    reducer: apiErrorReducer,
    state: {errors: []}
  })(Start)
)
