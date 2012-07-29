from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()

class Board(Base):
    __tablename__ = 'boards'
    board = Column(Integer(unsigned=True), primary_key=True, autoincrement=True)
    name = Column(String(50))
    shortname = Column(String(5))
    title = Column(String(5))
    
    def addThread(self,session, user, title, text):
        bc = session.query(BoardCounter).filter(BoardCounter.board==self).first()
        if bc == None:
            print 'init'
            bc = BoardCounter(board=self)
            bc.value = 0
            session.add(bc)
        bc.increment()
        post = Post(board=self,postid=bc.value, text=text, username=user, title=title)
        session.add(post)
        session.commit()
        session.flush()
        
    def getThreads(self,session):
        return session.query(Post).filter(Post.board==self).order_by(Post.post.asc()).all()

class BoardCounter(Base):
    __tablename__ = 'boardcounters'
    counter = Column(Integer(unsigned=True), primary_key=True, autoincrement=True)
    board_id = Column('board', Integer(unsigned=True), ForeignKey('boards.board', onupdate="CASCADE", ondelete="RESTRICT"))
    board = relationship('Board', backref='boardcounters')
    value = Column(Integer())
    
    def increment(self):
        self.value += 1
    
class Post(Base):
    __tablename__ = 'posts'
    post = Column(Integer(unsigned=True), primary_key=True, autoincrement=True)
    board_id = Column('board', Integer(unsigned=True), ForeignKey('boards.board', onupdate="CASCADE", ondelete="RESTRICT"))
    board = relationship('Board', backref='boards')
    username = Column(String(50))
    title = Column(String(50))
    text = Column(Text())
    parent = Column('parent', Integer(unsigned=True), ForeignKey('posts.post', onupdate="CASCADE", ondelete="RESTRICT"))
    postid = Column(Integer(unsigned=True))