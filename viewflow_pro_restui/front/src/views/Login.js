import React, {Component} from 'react'

import TextField from 'material-ui/TextField'
import RaisedButton from 'material-ui/RaisedButton'
import {Card, CardActions, CardTitle, CardText} from 'material-ui/Card'

import {login} from '../api/base'
import LoadIndicator from '../components/LoadIndicator'


const styles = {
  overlay: {
    position: 'fixed',
    height: '100%',
    width:'100%',
    
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',

    background: '#eee',
  },
  form: {
    position: "absolute",
  },
  formField: {
    width: '100%',
  }
}


class Login extends Component {
  constructor (props) {
    super(props)

    this.handleSubmit = this.handleSubmit.bind(this)
    
    this.state = {
      inProgress: false,
      errors: {}
    }    
  }

  login(token) {
    window.localStorage.token = token
  }

  redirectBack() {
    const { location } = this.props
    if (location.state && location.state.nextPathname) {
      this.context.router.replace(location.state.nextPathname)
    } else {
      this.context.router.replace('/')
    }
  }
  
  handleSubmit() {
    this.setState({inProgress: true})

    const formData = new FormData(this.refs.loginForm)

    login(formData).then(response => {
      this.setState({inProgress: false, errors: []})
      this.login(response.token)
      this.redirectBack()
    }).catch(      
      response => this.setState({inProgress: false, errors: response})
    )
  }

  render() {
    const errors = this.state.errors

    const subtitle = errors.non_field_errors || "Please, input your credentials"
    const subtitleColor = errors.non_field_errors ? "red" : ""
    
    return (
      <div style={styles.overlay}>
        <form ref="loginForm" style={styles.form}>
          <Card>
            <CardTitle title="Login" subtitle={subtitle} subtitleColor={subtitleColor} />
            <LoadIndicator inProgress={this.state.inProgress} />
            <CardText>
              <TextField name="username" floatingLabelText="Username" style={styles.formField} errorText={errors.username}/>
              <TextField name="password" floatingLabelText="Password" type="password"  style={styles.formField}  errorText={errors.password}/>
            </CardText>
          <CardActions>
            <RaisedButton label="Login" primary={true}  fullWidth={true} onClick={this.handleSubmit} />
          </CardActions>
          </Card>
        </form>
      </div>
    )
  }
}


Login.contextTypes = {
  router: React.PropTypes.object.isRequired
}

export default Login
