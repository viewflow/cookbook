import {post} from './base'


/**
 * Flow - Start
 */
export function start(action_url, formData) {
  return post(action_url, formData)
}


/**
 * Flow - Approve
 */
export function approve(action_url, formData) {
  return post(action_url, formData)
}
