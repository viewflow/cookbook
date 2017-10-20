import { RSAA } from 'redux-api-middleware';
import {
  LOGIN_REQUEST,
  LOGIN_SUCCESS,
  LOGIN_FAILURE
} from '../actionTypes'

export const login = (username, password) => ({
  [RSAA]: {
    endpoint: '/workflow/api/auth/token/',
    method: 'POST',
    body: JSON.stringify({username, password}),
    headers: { 'Content-Type': 'application/json' },
    types: [
      LOGIN_REQUEST, LOGIN_SUCCESS, LOGIN_FAILURE
    ]
  }
})
