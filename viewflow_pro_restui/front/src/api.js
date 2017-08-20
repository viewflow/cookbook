function _handleResponse(promise) {
  return promise.then(response => {
    if (response.status === 401) {
      window.localStorage.removeItem('userToken')
      window.location = '/login'
      return Promise.reject('Not authenticated')
    } else if (response.status === 403)  {
      return response.json().then(
        json => {
          throw Error(json.detail)
        }
      )
    } else if (response.status === 500)  {
      return response.text().then(
        text => {
          throw Error(text)
        }
      )
    } else {
      return response.json().then(
        json => ({ json, response })
      )
    }
  }).catch(response => {
    return Promise.reject({'non_field_errors': response.message})
  }).then(({ json, response }) => {
    if (!response.ok) {
      return Promise.reject(json)
    }
    return Promise.resolve(json)
  })
}

export function login (formData) {
  return _handleResponse(
    window.fetch('/api/login/', {
      method: 'POST',
      body: formData
    }))
}


export function flowGraph(url) {
  return _handleResponse(
    window.fetch(url, {
      'method': 'GET',
      headers: {
        'Authorization': 'Token ' + window.localStorage.userToken,
        'Accept': 'application/json'
      }
    })
  )
}

export function inbox() {
  return _handleResponse(
    window.fetch('/api/tasks/?task_list=INBOX', {
      'method': 'GET',
      headers: {
        'Authorization': 'Token ' + window.localStorage.userToken,
      }
    })
  )
}

export function queue() {
  return _handleResponse(
    window.fetch('/api/tasks/?task_list=QUEUE', {
      'method': 'GET',
      headers: {
        'Authorization': 'Token ' + window.localStorage.userToken,
      }
    })
  )
}

export function archive() {
  return _handleResponse(
    window.fetch('/api/tasks/?task_list=ARCHIVE', {
      'method': 'GET',
      headers: {
        'Authorization': 'Token ' + window.localStorage.userToken,
      }
    })
  )
}

export function hellorest_start(text) {
  return _handleResponse(
    window.fetch('/api/tasks/hellorest/start/', {
      method: 'POST',
      headers: {
        'Authorization': 'Token ' + window.localStorage.userToken,
        'Content-type': 'application/json'
      },
      body: JSON.stringify({text: text})
    })
  )
}
