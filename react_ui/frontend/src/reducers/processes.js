import { COMPLETED_PROCESSES_RECEIVED } from '../actionTypes'


const initialState = {
  completed: []
}

export default (state=initialState, action) => {
  switch(action.type) {
    case COMPLETED_PROCESSES_RECEIVED:
      return {
        ...state,
        completed: action.payload
      }
    default:
      return state
  }
}

export function getCompletedProcesses(state, flow_label) {
  return state.completed
}
