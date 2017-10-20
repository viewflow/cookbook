import React, { Component } from 'react'
import ui from 'redux-ui';
import { Alert, Label, Button, Form, Modal, ModalHeader, ModalBody, ModalFooter, Input } from 'reactstrap';
import { connect } from 'react-redux'
import { push } from 'react-router-redux'

import { apiErrorReducer } from '../../../reducers/ui/api'
import { approve } from '../../../actions/hellorest'

export class Approve extends Component {
  state = {
    approved: false,
  }

  approve = () => {
    this.props.approve(this.state.approved)
  }

  handleChange = (event) => {
    this.setState({approved: event.target.checked});
  }

  render() {
    const errors = this.props.ui.errors

    return (
      <Modal isOpen={true} toggle={this.props.close}>
        <ModalHeader toggle={this.close}>Approve</ModalHeader>
        <ModalBody>
          {errors.non_field_errors? <Alert color="danger">{errors.non_field_errors}</Alert>:""}
          <Form>
            <Label check>
              <Input name="approve"
                     type="checkbox"
                     checked={this.state.value}
                     onChange={this.handleChange}
              />
              {' '}Approve
            </Label>
          </Form>
        </ModalBody>
        <ModalFooter>
          <Button color="primary" onClick={this.approve}>Approve</Button>{' '}
          <Button color="secondary" onClick={this.props.close}>Cancel</Button>
        </ModalFooter>
      </Modal>
    )
  }
}


const mapDispatchToProps = (dispatch, ownProps) => ({
  approve: async (approved) => {
    const response = await dispatch(approve(ownProps.match.params.process_id, ownProps.match.params.task_id, approved))
    if(!response.error) {
      ownProps.onComplete()
      dispatch(push('../../'))
    }
  },
  close: () => {
    dispatch(push('../../'))
  }
})

export default connect(
  null,
  mapDispatchToProps
)(
  ui({
    key: 'auth',
    reducer: apiErrorReducer,
    state: { errors: [] }
  })(Approve)
)
