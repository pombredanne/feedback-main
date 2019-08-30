import PropTypes from 'prop-types'
import React, { Component, Fragment } from 'react'
import { Form } from 'react-final-form'
import { getCanSubmit, parseSubmitErrors } from 'react-final-form-utils'
import { requestData } from 'redux-saga-data'

import ArticleItemContainer from '../Articles/ArticleItem/ArticleItemContainer'
import FormFieldsContainer from './FormFields/FormFieldsContainer'
import FormFooterContainer from './FormFooter/FormFooterContainer'
import Footer from '../../layout/Footer'
import { Icon } from '../../layout/Icon'
import HeaderContainer from '../../layout/Header/HeaderContainer'
import MainContainer from '../../layout/Main/MainContainer'
import scrapDecorator from './decorators/scrapDecorator'
import getFormParams from '../../../utils/getFormParams'
import { articleNormalizer } from '../../../utils/normalizers'

class Article extends Component {
  constructor() {
    super()
    this.state = { isFormLoading: false }
  }

  componentDidMount() {
    this.handleRequestData()
  }

  getArticleFormParams = () => getFormParams('article', this.props)

  handleRequestData = () => {
    const { dispatch } = this.props
    const { id, isCreatedEntity } = this.getArticleFormParams()

    if (isCreatedEntity) {
      return
    }

    dispatch(
      requestData({
        apiPath: `/articles/${id}`,
        normalizer: articleNormalizer,
      })
    )
  }

  handleRequestFail = formResolver => (state, action) => {
    const { payload } = action
    const nextState = { isFormLoading: false }
    const errors = parseSubmitErrors(payload.errors)

    this.setState(nextState, () => formResolver(errors))
  }

  handleRequestSuccess = formResolver => (state, action) => {
    const { payload: { datum } } = action
    const { history } = this.props
    const nextState = { isFormLoading: false }

    this.setState(nextState, () => {
      formResolver()
      const nextUrl = `/articles/${datum.id}`
      history.push(nextUrl)
    })
  }

  onFormSubmit = formValues => {
    const { article, dispatch } = this.props
    const { method } = this.getArticleFormParams()
    const { id } = (article || {})

    const apiPath = `/articles/${id || ''}`
    this.setState({ isFormLoading: true })
    const formSubmitPromise = new Promise(resolve => {
      dispatch(requestData({
        apiPath,
        body: { ...formValues },
        handleFail: this.handleRequestFail(resolve),
        handleSuccess: this.handleRequestSuccess(resolve),
        method
      }))
    })
    return formSubmitPromise
  }

  render() {
    const { article, canCreateArticle, history } = this.props
    const { creationUrl, isCreatedEntity } = this.getArticleFormParams()
    const { id } = (article || {})
    const { isFormLoading } = this.state

    return (
      <Fragment>
        <HeaderContainer />
        <MainContainer name="article">
          <section className="section hero is-relative">
            <h1 className="title">
              {isCreatedEntity ? 'New Article' : 'Article'}
            </h1>
            {!isCreatedEntity && (
              <div className="is-absolute b12 r8">
                {canCreateArticle && (
                  <button
                    className="button is-primary"
                    onClick={() => history.push(creationUrl)}
                    type="button"
                  >
                    New article
                  </button>
                )}
              </div>
            )}
          </section>

          {id && (
            <section className="section">
              <ArticleItemContainer article={article} />
            </section>
          )}

          <section className="section">
            <h2 className="subtitle flex-columns items-center">
              <Icon className="icon mr12" svg="ico-newspaper" />
              DETAILS
            </h2>
            <Form
              decorators={[
                scrapDecorator
              ]}
              initialValues={article || false}
              key={id}
              onSubmit={this.onFormSubmit}
              render={formProps => {
                const {
                  form: { reset: resetForm },
                  handleSubmit,
                  validating
                }= formProps
                const canSubmit = getCanSubmit(
                  Object.assign({ isLoading: isFormLoading }, formProps))
                return (
                  <form
                    autoComplete="off"
                    className="form"
                    disabled={isFormLoading}
                    noValidate
                    onSubmit={handleSubmit}
                  >
                    <FormFieldsContainer validating={validating} />
                    <FormFooterContainer
                      canSubmit={canSubmit}
                      isLoading={isFormLoading}
                      resetForm={resetForm}
                    />
                  </form>
                )
              }}
            />
          </section>
        </MainContainer>
        <Footer />
      </Fragment>
    )
  }
}

Article.defaultProps = {
  article: null,
  canCreateArticle: false,
}

Article.propTypes = {
  article: PropTypes.object,
  canCreateArticle: PropTypes.bool,
  dispatch: PropTypes.func.isRequired,
  history: PropTypes.shape({
    push: PropTypes.func.isRequired
  }).isRequired
}

export default Article
