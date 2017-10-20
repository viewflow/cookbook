import { combineReducers } from 'redux'
import { routerReducer } from 'react-router-redux'
import { reducer as uiReducer } from 'redux-ui'

import auth, * as fromAuth from './auth.js'
import flow, * as fromFlow from './flow.js'
import tasks, * as fromTasks from './tasks.js'
import processes, * as fromProcesses from './processes.js'

export default combineReducers({
  auth,
  flow,
  tasks,
  processes,
  router: routerReducer,
  ui: uiReducer
})

export const isAuthenticated = state => fromAuth.isAuthenticated(state.auth)
export const getToken = state => fromAuth.getToken(state.auth)

export const getInbox = state => fromTasks.getInbox(state.tasks);
export const getQueue = state => fromTasks.getQueue(state.tasks);
export const getArchive = state => fromTasks.getArchive(state.tasks);
export const getTaskList = (state, flow_label, task_label) =>
  fromTasks.getTaskList(state.tasks, flow_label, task_label);

export const getFlowGraph = (state, flow_label) =>
  fromFlow.getFlowGraph(state.flow, flow_label);

export const getCompletedProcesses = (state, flow_label) =>
  fromProcesses.getCompletedProcesses(state.processes, flow_label);
