import { compose, createStore, applyMiddleware } from 'redux'
import { persistStore } from 'redux-persist'
import thunk from 'redux-thunk'

import { API_URL } from './config'
import rootReducer from '../reducers'

const buildStoreEnhancer = (middlewares = []) => {
  const enhancers = []

  const useDevTools = typeof window !== 'undefined' && window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__
  if (useDevTools) {
    const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__
    return composeEnhancers(...enhancers, applyMiddleware(...middlewares))
  }
  return compose(
    ...enhancers,
    applyMiddleware(...middlewares)
  )
}

export const configureStore = (initialState = {}) => {
  const middlewares = [thunk.withExtraArgument({ rootUrl: API_URL })]

  const storeEnhancer = buildStoreEnhancer(middlewares)

  const store = createStore(rootReducer, initialState, storeEnhancer)

  const persistor = persistStore(store)

  return { persistor, store }
}

export default configureStore
