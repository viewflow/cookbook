import { RSAA } from 'redux-api-middleware';

import {
  FLOWGRAPH_REQUEST, FLOWGRAPH_RECEIVED, FLOWGRAPH_FAILURE
} from '../actionTypes'
import { withAuth } from '../auth'

export const fetchChart = (flow_label) => ({
  [RSAA] : {
    endpoint: `/workflow/api/flows/${flow_label}/chart/`,
    method: 'GET',
    headers: withAuth({ 'Accept': 'application/json' }),
    types: [
      FLOWGRAPH_REQUEST,
      {
        type: FLOWGRAPH_RECEIVED,
        meta: { flow_label }
      },
      FLOWGRAPH_FAILURE
    ]
  }
})
