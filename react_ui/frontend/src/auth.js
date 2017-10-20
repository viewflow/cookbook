import { getToken } from './reducers'

export function withAuth(headers={}) {
  return (state) => ({
    ...headers,
    'Authorization': `Token ${getToken(state)}`
  })
}
