/**
 * Token authentification
 *  
 * @param {Object} formData a FormData object with auth credentials
 */
export function login (formData) {
  return fetch('/login/', {
    method: 'POST',
    body: formData
  }).then(response => {
    return response.json().then(
      json => ({ json, response })
    )
  }).catch(response => {
    return Promise.reject({'non_field_errors': response.message})
  }).then(({ json, response }) => {
    if (!response.ok) {
      return Promise.reject(json)
    }
    
    return Promise.resolve(json)
  })
}

/**
 * Authenticated API get request
 *
 * @param {string} url the query path to requet
 */
export function get (url) {
  return fetch(url, {
    method: 'GET',
    headers: {
      'Authorization': 'Token ' + window.localStorage.token
    }
  }).then(response => {
    return response.json().then(
      json => ({ json, response })
    )
  }).catch(response => {
    return Promise.reject({'detail': response.message})
  }).then(({ json, response }) => {
    if (!response.ok) {
      return Promise.reject(json)
    }
    
    return Promise.resolve(json)
  })
}

/**
 * Authenticated API post request
 *
 * @param {string} url the query path to requet
 *
 * @param {Object} formData a FormData to post
 */
export function post (url, formData) {
}
