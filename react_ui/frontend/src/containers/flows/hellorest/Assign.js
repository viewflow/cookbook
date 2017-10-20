import React, { Component } from 'react'
import ui from 'redux-ui';
import { Alert, Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';
import { connect } from 'react-redux'
import { push } from 'react-router-redux'

import { apiErrorReducer } from '../../../reducers/ui/api'
import { approveAssign } from '../../../actions/hellorest'

export class Assign extends Component {
  close = () => {
    this.props.close()
  }

  render() {
    const errors = this.props.ui.errors

    return (
      <Modal isOpen={true} toggle={this.close}>
        <ModalHeader toggle={this.close}>Assign Task</ModalHeader>
        <ModalBody>
          {errors.non_field_errors? <Alert color="danger">{errors.non_field_errors}</Alert>:""}
        </ModalBody>
        <ModalFooter>
          <Button color="primary" onClick={this.props.assign}>Assign</Button>{' '}
          <Button color="secondary" onClick={this.close}>Cancel</Button>
        </ModalFooter>
      </Modal>
    )
  }
}

const mapDispatchToProps = (dispatch, ownProps) => ({
  assign: async (text) => {
    const response = await dispatch(approveAssign(ownProps.match.params.process_id, ownProps.match.params.task_id))
    if(!response.error) {
      ownProps.onComplete()
      dispatch(push('../../../'))
    }
  },
  close: () => {
    dispatch(push('../../../'))
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
  })(Assign)
)
