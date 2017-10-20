import { RSAA } from 'redux-api-middleware';

import * as types from '../actionTypes'
import { withAuth } from '../auth'

export const start = (message) => ({
  [RSAA] : {
    endpoint: `/workflow/api/tasks/hellorest/start/`,
    method: 'POST',
    body: JSON.stringify({text: message}),
    headers: withAuth({ 'Content-type': 'application/json' }),
    types: [
      types.HELLOREST_START_REQUEST,
      types.HELLOREST_START_SUCCEED,
      types.HELLOREST_START_FAILURE
    ]
  }
})

export const approve = (process_id, task_id, approved) => ({
  [RSAA] : {
    endpoint: `/workflow/api/tasks/hellorest/${process_id}/approve/${task_id}/`,
    method: 'POST',
    body: JSON.stringify({approved: approved}),
    headers: withAuth({ 'Content-type': 'application/json' }),
    types: [
      types.HELLOREST_APPROVE_REQUEST,
      types.HELLOREST_APPROVE_SUCCEED,
      types.HELLOREST_APPROVE_FAILURE
    ]
  }
})

export const approveAssign = (process_id, task_id) => ({
  [RSAA] : {
    endpoint: `/workflow/api/tasks/hellorest/${process_id}/approve/${task_id}/assign/`,
    method: 'POST',
    headers: withAuth({ 'Content-type': 'application/json' }),
    types: [
      types.HELLOREST_APPROVE_ASSIGN_REQUEST,
      types.HELLOREST_APPROVE_ASSIGN_SUCCEED,
      types.HELLOREST_APPROVE_ASSIGN_FAILURE
    ]
  }
})
