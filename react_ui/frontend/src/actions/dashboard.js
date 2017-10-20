import { fetchTasks } from './tasks.js'
import { fetchCompleted } from './processes.js'


export const refreshDashboard = (flow_label, task_labels) => {
  return (dispatch) => {
    const tasks_promises = task_labels.map(
      (task_label) => dispatch(fetchTasks(flow_label, task_label))
    )

    return Promise.all([
      ...tasks_promises,
      dispatch(fetchCompleted(flow_label))
    ])
  }
}
