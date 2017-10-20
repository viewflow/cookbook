const initialState = {
  errors: []
}

export const apiErrorReducer = (state=initialState, action) => {
  if(action.error === true && action.payload && action.payload.name === "ApiError") {
    return state.set(
      'errors',
      action.payload.response || {'non_field_errors': action.payload.statusText}
    )
  }
  return state
}
