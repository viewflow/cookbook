import React, { Component, PropTypes } from 'react'

import Paper from 'material-ui/Paper';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import {Card, CardActions, CardTitle, CardText} from 'material-ui/Card';

import auth from '../api/auth'

const styles = {
  overlay: {
    position: 'fixed',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    alignContent: 'center',
    background: '#eee',
    height: '100%',
    width:'100%',
  },
  formField: {
    width: '100%',
  }
}

class Auth extends Component {
  getChildContext() {
    return {'auth': auth};
  }

  renderLoginScreen() {
    return (
      <div style={styles.overlay}>
        <form>
          <Card>
            <CardTitle title="Login" subtitle="Please, input your credentials"/>
            <CardText>
              <TextField floatingLabelText="Username" style={styles.formField}/>
              <TextField floatingLabelText="Password" type="password"  style={styles.formField}/>
            </CardText>
            <CardActions>
              <RaisedButton label="Login" primary={true}  fullWidth={true}/>
            </CardActions>
          </Card>
        </form>
      </div>
    )
  }

  render() {
    return !auth.loggedIn() ? <div>{this.props.children}</div> : this.renderLoginScreen()
  }
}

Auth.childContextTypes = {
  auth: React.PropTypes.object
};

export default Auth;
