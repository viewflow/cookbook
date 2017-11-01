import {
  LOGIN_SUCCESS,
  LOGIN_FAILURE
} from '../actionTypes'

const initialState = {
  token: undefined,
}

export default (state=initialState, action) => {
  if(action.error === true &&
     action.payload &&
     action.payload.name === "ApiError" &&
     action.payload.status === 401) {
       return {
         token: undefined
       }
  }

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
