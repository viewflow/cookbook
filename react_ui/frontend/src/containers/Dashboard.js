import DocumentTitle from 'react-document-title'
import React, { Component } from 'react'
import { Route } from 'react-router-dom'
import {
  Card,
  CardBlock,
  CardTitle,
  CardText,
  Button,
  ButtonGroup
} from 'reactstrap';
import { connect } from 'react-redux'
import { Link} from 'react-router-dom'


import FlowGraph from './FlowGraph'
import Start from './flows/hellorest/Start'
import Assign from './flows/hellorest/Assign'
import Approve from './flows/hellorest/Approve'
import { refreshDashboard } from '../actions/dashboard'
import { getCompletedProcesses, getTaskList } from '../reducers'

export class Dashboard extends Component {
  refresh = () => {
    this.props.refreshDashboard('hellorest', [
      'hellorest/flows.HelloRestFlow.approve',
      'hellorest/flows.HelloRestFlow.send'
    ])
  }

  componentDidMount() {
    this.refresh()
    this.updateTimer = setInterval(this.refresh, 1000)
  }

  componentWillUnmount() {
    clearInterval(this.updateTimer)
  }

  renderTaskAction(task, action) {
    if(action.name === 'assign') {
      return (
      <Button
        key={`${task.id}_'${action.name}`}
        to={`/dashboard/hellorest/${task.process.id}/approve/${task.id}/assign/`}
        tag={Link}>
        {action.name}
      </Button>
      )
    } else if(action.name === 'execute') {
      return (
      <Button
        key={`${task.id}_'${action.name}`}
        to={`/dashboard/hellorest/${task.process.id}/approve/${task.id}/`}
        tag={Link}>
        {action.name}
      </Button>
      )
    }
  }

  renderTask(task) {
    return (
      <div key={task.id} className="dashboard__task">
        <Card>
          <CardBlock>
            <CardTitle>#{task.process.id} {task.title}</CardTitle>
            <CardText>
            <div>{task.process_summary}</div>
            <div>{task.summary}</div>
            </CardText>
          </CardBlock>
          <CardBlock className="tasklist__actions">
            <ButtonGroup>
              {task.actions.map(action => this.renderTaskAction(task, action))}
            </ButtonGroup>
          </CardBlock>
        </Card>
      </div>
    )
  }

  renderCompleted(process) {
    return (
      <div className="dashboard__completed" key={process.id}>
        <Card className="dashboard__task">
          <CardBlock>
            <CardTitle>#{process.id} {process.text}</CardTitle>
            <CardText>{process.approved?"Approved":"Rejected"}</CardText>
          </CardBlock>
        </Card>
      </div>
    )
  }

  render() {
    return (
      <div className="dashboard">
        <DocumentTitle title="Dashboard" />
        <Route
          exact
          path='/dashboard/hellorest/start/'
          render={(props) => <Start {...props} onComplete={this.refresh}/> }
        />
        <Route
          exact
          path="/dashboard/hellorest/:process_id/approve/:task_id/assign/"
          render={(props) => <Assign {...props} onComplete={this.refresh}/>}
        />
        <Route
          exact
          path="/dashboard/hellorest/:process_id/approve/:task_id/"
          render={(props) => <Approve {...props} onComplete={this.refresh}/>}
        />
        <div className="dashboard__column">
          <div className="dashboard__title">Start</div>
          <div className="dashboard__content">
            <Card block>
              <CardText>This process demonstrates hello world approval request flow.</CardText>
              <FlowGraph flow_label='hellorest' />
              <Button to="/dashboard/hellorest/start/" tag={Link}>Start</Button>
            </Card>
          </div>
        </div>
        <div className="dashboard__column">
          <div className="dashboard__title">Approve</div>
          <div className="dashboard__content">
          {this.props.approve.map(task => this.renderTask(task))}
          </div>
        </div>
        <div className="dashboard__column">
          <div className="dashboard__title">Send</div>
          <div className="dashboard__content">
          {this.props.send.map(task => this.renderTask(task))}
          </div>
        </div>
        <div className="dashboard__column">
          <div className="dashboard__title">Complete</div>
          <div className="dashboard__content">
          {this.props.completed.slice(0, 6).map(process => this.renderCompleted(process))}
          {this.props.completed.length>6
            ?<div className="tasklist__moretasks">And {this.props.completed.length-6} more</div>
            :""}
          </div>
        </div>
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  approve: getTaskList(state, 'hellorest', 'hellorest/flows.HelloRestFlow.approve'),
  send: getTaskList(state, 'hellorest', 'hellorest/flows.HelloRestFlow.send'),
  completed: getCompletedProcesses(state, 'hellorest'),
})

export default connect(
  mapStateToProps,
  {refreshDashboard}
)(Dashboard)
