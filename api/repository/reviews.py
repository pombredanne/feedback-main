from domain.keywords import create_filter_matching_all_keywords_in_any_model, \
                            create_get_filter_matching_ts_query_in_any_model
from models.manager import Manager
from models.review import Review
from models.review_tag import ReviewTag
from models.tag import Tag
from models.user import User
from utils.human_ids import dehumanize

review_ts_filter = create_get_filter_matching_ts_query_in_any_model(
    Review,
    Tag,
    User
)

def save_tags(review, tag_ids):
    review_tags = []
    for tag_id in tag_ids:
        tag = Tag.query.get(dehumanize(tag_id))
        review_tag = ReviewTag.query.filter_by(tag=tag, review=review).first()
        if review_tag is None:
            review_tag = ReviewTag()
            review_tag.review = review
            review_tag.tag = tag
        review_tags.append(review_tag)
    Manager.check_and_save(*review_tags)

def filter_reviews_with_article_id(query, article_id):
    query = query.filter_by(articleId=dehumanize(article_id))
    return query

def get_reviews_join_query(query):
    query = query.outerjoin(ReviewTag) \
                 .outerjoin(Tag) \
                 .join(User)
    return query

def get_reviews_query_with_keywords(query, keywords):
    keywords_filter = create_filter_matching_all_keywords_in_any_model(
        review_ts_filter,
        keywords
    )
    query = query.filter(keywords_filter)
    return query