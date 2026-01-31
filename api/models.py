from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from . import db

""" Database Models
    TODO: 
    - add uniqueness constraint on Song for title + artist
"""

class Artist(db.Model):
    __tablename__ = 'artists'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    
    # relationships
    songs: Mapped[list['Song']] = relationship('Song', back_populates='artist', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id, 
            'name': self.name,
            'songs': [song.title for song in self.songs] if self.songs else []
            }

class Song(db.Model):
    __tablename__ = 'songs'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    artist_id: Mapped[int] = mapped_column(ForeignKey('artists.id'), nullable=False)
    
    # relationships
    artist: Mapped['Artist'] = relationship('Artist', back_populates='songs')
    dance: Mapped['Dance'] = relationship('Dance', back_populates='song', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist.name,
            'artist_id': self.artist_id,
            'status': self.dance.status if self.dance else None
        }
    
class Dance(db.Model):
    __tablename__ = 'dances'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    song_id: Mapped[int] = mapped_column(ForeignKey('songs.id'), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default='to do')

    # TODO: change status to enum and enforce at db level
    # class StatusEnum(str, Enum):
    #     TO_DO = 'to do'
    #     IN_PROGRESS = 'in progress'
    #     DONE = 'done'
    #
    # status: Mapped[StatusEnum] = mapped_column(String(50), default=StatusEnum.TO_DO)
    
    # relationships
    song: Mapped['Song'] = relationship('Song', back_populates='dance')

    def to_dict(self):
        return {
            'id': self.id,
            'song_id': self.song_id,
            'song': self.song.title,
            'status': self.status
        }