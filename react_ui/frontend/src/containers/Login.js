import DocumentTitle from 'react-document-title'
import React from 'react'
import ui from 'redux-ui';
import { Redirect } from 'react-router'
import { connect } from 'react-redux'

import LoginForm from '../components/LoginForm'
import { isAuthenticated } from '../reducers'
import { apiErrorReducer } from '../reducers/ui/api'
import { login } from  '../actions/auth'

export const Login = ({ui, ...props}) => {
  if (props.isAuthenticated) {
    return <Redirect to='/' />
  }

  return (
    <div className="login-page">
      <DocumentTitle title="Login" />
      <LoginForm {...props} {...ui} />
    </div>
  )
}

export default connect(
  (state) => ({
    isAuthenticated: isAuthenticated(state)
  }),
  { onSubmit: login }
)(ui({
  key: 'auth',
  reducer: apiErrorReducer,
  state: {errors: []}
})(Login))
