import { RSAA } from 'redux-api-middleware';
import qs from 'qs'

import * as types from '../actionTypes'
import { withAuth } from '../auth'

export const fetchInbox = () => ({
  [RSAA] : {
    endpoint: `/workflow/api/tasks/?task_list=INBOX`,
    method: 'GET',
    headers: withAuth(),
    types: [
      types.INBOX_REQUEST, types.INBOX_RECEIVED, types.INBOX_FAILURE
    ]
  }
})

export const fetchQueue = () => ({
  [RSAA] : {
    endpoint: `/workflow/api/tasks/?task_list=QUEUE`,
    method: 'GET',
    headers: withAuth(),
    types: [
      types.QUEUE_REQUEST, types.QUEUE_RECEIVED, types.QUEUE_FAILURE
    ]
  }
})

export const fetchArchive = () => ({
  [RSAA] : {
    endpoint: `/workflow/api/tasks/?task_list=ARCHIVE`,
    method: 'GET',
    headers: withAuth(),
    types: [
      types.ARCHIVE_REQUEST, types.ARCHIVE_RECEIVED, types.ARCHIVE_FAILURE
    ]
  }
})

export const fetchTasks = (flow_label, task_label) => {
  const query = qs.stringify({ flow_task: task_label, task_list: 'ACTIVE' })
  return {
    [RSAA]: {
      endpoint: `/workflow/api/tasks/${flow_label}/?${query}`,
      method: 'GET',
      headers: withAuth(),
      types: [
        types.TASKS_REQUEST,
        {
          type: types.TASKS_RECEIVED,
          meta: { flow_label, task_label }
        },
        types.TASKS_FAILURE
      ]
    }
  }
}
