import {get, post} from './base'


/**
 * List of flows
 */
export function flows() {
    return get('/flows/')
}


/**
 * Inbox tasks
 */
export function inbox() {
  return get('/tasks/?task_list=INBOX')
}


/**
 * Unassigned tasks queue
 */
export function queue() {
  return get('/tasks/?task_list=QUEUE')
}


/**
 * Completed tasks list
 */
export function archive() {
  return get('/tasks/?task_list=ARCHIVE')
}


/**
 * Generic task detail
 */
export function task_detail(task_detail_url) {
  return get(task_detail_url)
}


/**
 * Generic task action.

 * Assumes that action requires no parameters, just a POST request to
 * complete
 */
export function perform_action(action_url) {
  return post(action_url)
}
