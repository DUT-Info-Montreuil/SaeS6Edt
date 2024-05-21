from database.config import db
from models.WeekComment import WeekComment

class WeekCommentService:

    @staticmethod
    def create_comment(data):
        commentExist = WeekComment.query.filter_by(week_number=data['week_number'], year=data['year'], id_promo=data['id_promo']).first()
        if (commentExist):
            return WeekCommentService.update_comment(commentExist.id, **data)

        comment = WeekComment(**data)
        db.session.add(comment)
        db.session.commit()
        return comment
    
    def get_comment_by_id(id):
        return WeekComment.query.get(id)
    
    @staticmethod
    def get_all_comments():
        comments = WeekComment.query.all()
        return comments
    

    
    @staticmethod
    def delete_comment(id):
        comment = WeekComment.query.get(id)
        db.session.delete(comment)
        db.session.commit()
        return comment
    
    @staticmethod
    def update_comment(id, content, **kwargs):
        comment = WeekComment.query.get(id)

        if (content == ""):
            return WeekCommentService.delete_comment(id)

        comment.content = content
        db.session.commit()
        return comment
