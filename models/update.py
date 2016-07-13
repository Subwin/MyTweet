from . import db

class Update(object):
    def update(self, form):
        new_content = form['content'] if form['content'] != '' else self.content
        self.content = new_content

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()