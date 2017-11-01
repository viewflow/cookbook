import React, { Component } from 'react'
import DocumentTitle from 'react-document-title'
import {
  Card,
  CardBlock,
  Button,
  ButtonGroup,
  CardTitle,
  CardText,
} from 'reactstrap';
import { Route, Link } from 'react-router-dom'
import { connect } from 'react-redux'

import Approve from './flows/hellorest/Approve'
import Assign from './flows/hellorest/Assign'
import { fetchInbox, fetchQueue, fetchArchive } from '../actions/tasks'
import { getInbox, getQueue, getArchive } from '../reducers'

export default class TaskList extends Component {
  refresh = () => {
    this.props.fetch()
  }

  componentDidMount() {
   this.refresh()
  }

  renderTaskAction(task, action) {
    if(action.name === 'assign') {
      return (
      <Button
        key={`${task.id}_'${action.name}`}
        to={`${this.props.location}${task.process.id}/approve/${task.id}/assign/`}
        tag={Link}>
        {action.name}
      </Button>
      )
    } else if(action.name === 'execute') {
      return (
      <Button
        key={`${task.id}_'${action.name}`}
        to={`${this.props.location}${task.process.id}/approve/${task.id}/`}
        tag={Link}>
        {action.name}
      </Button>
      )
    }
  }

  renderTask(task) {
    return (
      <div className="tasklist__task" key={task.id}>
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

  render() {
    return (
      <div className="tasklist">
        {this.props.tasks.length === 0 ? <h1>{this.props.name} are empty</h1> : ""}
        <DocumentTitle title={this.props.name} />
        <Route
          exact
          path={`${this.props.location}:process_id/approve/:task_id/assign/`}
          render={(props) => <Assign {...props} onComplete={this.refresh}/>}
        />
        <Route
          exact
          path={`${this.props.location}:process_id/approve/:task_id/`}
          render={(props) => <Approve {...props} onComplete={this.refresh}/>}
        />
        {this.props.tasks.map(task => this.renderTask(task))}
      </div>
    )
  }
}

export const Inbox = connect(
  (state) => ({
    name: 'Inbox',
    location: '/tasks/inbox/',
    tasks: getInbox(state),
  }),
  { fetch: fetchInbox }
)(TaskList)

export const Queue = connect(
  (state) => ({
    name: 'Queue',
    location: '/tasks/queue/',
    tasks: getQueue(state),
  }),
  { fetch: fetchQueue }
)(TaskList)

export const Archive = connect(
  (state) => ({
    name: 'Archive',
    tasks: getArchive(state),
  }),
  { fetch: fetchArchive }
)(TaskList)
