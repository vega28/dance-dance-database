from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import db

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
    # TODO: make status an enum
    status: Mapped[str] = mapped_column(String(50), default='to do')
    
    # relationships
    artist: Mapped['Artist'] = relationship('Artist', back_populates='songs')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist.name,
            'artist_id': self.artist_id,
            'status': self.status
        }