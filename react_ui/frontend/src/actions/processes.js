import { RSAA } from 'redux-api-middleware';

import {
  COMPLETED_PROCESSES_REQUEST,
  COMPLETED_PROCESSES_RECEIVED,
  COMPLETED_PROCESSES_FAILURE
} from '../actionTypes'
import { withAuth } from '../auth'

export const fetchCompleted = (flow_label) => ({
  [RSAA] : {
    endpoint: `/workflow/api/processes/${flow_label}/?status=DONE`,
    method: 'GET',
    headers: withAuth(),
    types: [
      COMPLETED_PROCESSES_REQUEST,
      COMPLETED_PROCESSES_RECEIVED,
      COMPLETED_PROCESSES_FAILURE
    ]
  }
})
