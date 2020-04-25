from sqlalchemy import BigInteger,\
                       Column,\
                       ForeignKey,\
                       Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy_api_handler import ApiHandler
from sqlalchemy_api_handler.mixins.soft_deletable_mixin import SoftDeletableMixin

from models.utils.db import get_model_with_table_name, Model
from models.mixins import HasScienceFeedbackMixin, \
                          HasRatingMixin


class Review(ApiHandler,
             Model,
             HasScienceFeedbackMixin, 
             HasRatingMixin,
             SoftDeletableMixin):

    articleId = Column(BigInteger(),
                       ForeignKey('article.id'),
                       nullable=False,
                       index=True)

    article = relationship('Article',
                           foreign_keys=[articleId],
                           backref='reviews')

    comment = Column(Text(), nullable=True)

    evaluationId = Column(BigInteger(),
                          ForeignKey('evaluation.id'),
                          index=True)

    evaluation = relationship('Evaluation',
                              foreign_keys=[evaluationId],
                              backref='reviews')

    userId = Column(BigInteger(),
                    ForeignKey('user.id'),
                    nullable=False,
                    index=True)

    user = relationship('User',
                        foreign_keys=[userId],
                        backref='reviews')

    @property
    def verdicts(self):
        Verdict = get_model_with_table_name('verdict')
        VerdictUser = get_model_with_table_name('verdict_user')
        verdict_users = VerdictUser.query.filter_by(userId=self.userId)
        verdict_ids = [verdict_user.verdict.id for verdict_user in verdict_users]
        verdicts = Verdict.query.filter(Verdict.id.in_(verdict_ids)).all()
        return InstrumentedList(verdicts)
