import storage from 'redux-persist/lib/storage'
import thunk from 'redux-thunk';
import { apiMiddleware } from 'redux-api-middleware';
import { applyMiddleware, createStore } from 'redux'
import { createFilter   } from 'redux-persist-transform-filter';
import { persistReducer } from 'redux-persist'
import { routerMiddleware } from 'react-router-redux'
import rootReducer from './reducers'

export default (history) => {
  const persistedFilter = createFilter('auth', ['token']);

  const reducer = persistReducer(
    {
      key: 'root',
      storage: storage,
      whitelist: ['auth'],
      transforms: [persistedFilter]
    },
    rootReducer)

  const store = createStore(
    reducer, {},
    applyMiddleware(
      thunk,
      apiMiddleware,
      routerMiddleware(history))
  )

  return store
}
