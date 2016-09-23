import React, { Component, PropTypes } from 'react'

import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';

import auth from '../api/auth'


class Auth extends Component {
  getChildContext() {
    return {'auth': auth};
  }

  renderLoginScreen() {
    return (
      <div>
        <form>
          <TextField floatingLabelText="Username" />
          <TextField floatingLabelText="Password" type="password" />
          <RaisedButton label="Login" primary={true} />
        </form>
      </div>
    )
  }

  render() {
    return auth.loggedIn() ? <div>{this.props.children}</div> : this.renderLoginScreen()
  }
}

Auth.childContextTypes = {
  auth: React.PropTypes.object
};

export default Auth;
