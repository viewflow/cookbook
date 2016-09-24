import React from 'react'
import { IndexRoute, Route }  from 'react-router'

import App from './App'
import InboxView from './views/Inbox'
import QueueView from './views/Queue'
import ArchiveView from './views/Archive'
import LoginView from './views/Login'
import LogoutView from './views/Logout'


function requireAuth(nextState, transition) {
  if(!localStorage.token) {
    transition({
      pathname: '/login',
      state: { nextPathname: nextState.location.pathname }
    })
  }
}


export default (
  <Route>
    <Route path='login' component={LoginView} />    
    <Route path='logout' component={LogoutView} />    
    <Route path='/' component={App} onEnter={requireAuth}>
      <IndexRoute component={InboxView} />
      <Route path='queue' component={QueueView} />
      <Route path='archive' component={ArchiveView} />
      <Route path='logout' component={LogoutView} />
    </Route>
  </Route>
)
