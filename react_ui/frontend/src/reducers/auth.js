import {
  LOGIN_SUCCESS,
  LOGIN_FAILURE
} from '../actionTypes'

const initialState = {
  token: undefined,
}

export default (state=initialState, action) => {
  switch(action.type) {
    case LOGIN_SUCCESS:
      return {
        token: action.payload.token,
      }
    case LOGIN_FAILURE:
      return {
        token: undefined,
      }
    default:
      return state
  }
}

export function isAuthenticated(state) {
  return !!state.token
}

export function getToken(state) {
  return state.token
}
