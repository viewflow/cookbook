import React, {Component} from 'react'
import { Redirect } from 'react-router-dom'
import { Alert, Jumbotron, Button, Form, Progress } from 'reactstrap';


import TextInput from '../components/TextInput'
import * as API from '../api'

export default class Login extends Component {
  constructor (props) {
    super(props)

    this.handleSubmit = this.handleSubmit.bind(this)

    this.state = {
      done: false,
      inProgress: false,
      errors: {}
    }
  }

  handleSubmit(event) {
    event.preventDefault()
    this.setState({inProgress: true})
    
    const formData = new window.FormData(event.target)
    API.login(formData).then(response => {
      window.localStorage.userToken = response.token
      this.setState({inProgress: false, done: true, errors: []})
    }).catch(
      response => {
        this.setState({inProgress: false, errors: response})
      }
    )
  }

  render() {
    const { from } = this.props.location.state || { from: { pathname: '/' } }
 
    if(!!window.localStorage.userToken) {
      return (
        <div>
          <Redirect to={from} />
        </div>
      )
    }

    return (
      <div className="login-page"> 
      <div className="container">
        <Jumbotron>
          <h2>Please log in</h2>
          {this.state.errors.non_field_errors? <Alert color="danger">{this.state.errors.non_field_errors}</Alert>:""}
          <Form onSubmit={this.handleSubmit} >
            <TextInput id="id_username" name="username" label="Username" error={this.state.errors.username} getRef={input => input && input.focus()}/>
            <TextInput id="id_password" name="password" label="Password" error={this.state.errors.password} type="password"/>
            <Button type="submit" color="primary" size="lg" disabled={this.state.inProgress}>Log In</Button>
          </Form>
        </Jumbotron>
        {this.state.inProgress?<Progress animated value="100" className="progress--top"/>:""}
      </div>
      </div>
    )
  }
}
