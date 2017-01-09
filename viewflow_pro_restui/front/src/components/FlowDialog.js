import React, {Component, PropTypes} from 'react';

import Dialog from 'material-ui/Dialog'

import HelloRestStart from './flows/hellorest/Start'
import HelloRestApprove from './flows/hellorest/Approve'


const taskCompoments = {
  'hellorest/flows.HelloRestFlow.start': HelloRestStart,
  'hellorest/flows.HelloRestFlow.approve': HelloRestApprove,
}



class FlowDialog extends Component {
  renderTask() {
    return React.createElement(taskCompoments[this.props.task.flow_task], {
      'task': this.props.task
    })
  }

  render() {
    return (
      <Dialog
          title={this.props.task.title}
          open={true}>
        {this.renderTask()}
      </Dialog>
    )
  }
}


FlowDialog.propTypes = {
  task: PropTypes.object.isRequired
}


export default FlowDialog;
