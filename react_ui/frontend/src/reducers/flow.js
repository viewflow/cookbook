import { FLOWGRAPH_RECEIVED } from '../actionTypes'

const initialState = {

}

export default (state=initialState, action) => {
  switch(action.type) {
    case FLOWGRAPH_RECEIVED:
      const flow_label = action.meta.flow_label,
            flow_data = state[flow_label] || {}

      return {
        ...state,
        [flow_label]: {
          ...flow_data,
          svg: action.payload.svg
        }
      }
    default:
      return state
  }
}

export function getFlowGraph(state, flow_label) {
  const flow_data = state[flow_label]

  if(flow_data) {
    return flow_data.svg
  }
}
