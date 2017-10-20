import { INBOX_RECEIVED, QUEUE_RECEIVED, ARCHIVE_RECEIVED, TASKS_RECEIVED } from '../actionTypes'

const initialState = {
  inbox: [],
  queue: [],
  archive: [],
  task_lists: {}
}

export default (state=initialState, action) => {
  switch(action.type) {
    case INBOX_RECEIVED:
      return {
        ...state,
        inbox: action.payload
      }
    case QUEUE_RECEIVED:
      return {
        ...state,
        queue: action.payload
      }
    case ARCHIVE_RECEIVED:
      return {
        ...state,
        archive: action.payload
      }
    case TASKS_RECEIVED:
      const flow_label = action.meta.flow_label,
            task_label = action.meta.task_label,
            task_list = state.task_lists[flow_label] || {}

      return {
          ...state,
          task_lists: {
            [flow_label]: {
              ...task_list,
              [task_label]: action.payload
            }
          }
        }
    default:
      return state
  }
}

export function getInbox(state) {
  return state.inbox
}

export function getQueue(state) {
  return state.queue
}

export function getArchive(state) {
  return state.archive
}

export function getTaskList(state, flow_label, task_label) {
  const task_list = state.task_lists[flow_label] || {}
  return  task_list[task_label] || []
}
