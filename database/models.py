import os
import pymysql
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Text

USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')
DATABASE = os.getenv('DATABASE')

Base = declarative_base()

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    def __repr__(self):
        return f'<Project(name={self.name})>'


class UserStory(Base):
    __tablename__ = 'user_stories'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    user_story_count = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return f'<UserStory(id={self.id}, project_id={self.project_id})>'


class SchemaDesign(Base):
    __tablename__ = 'schema_designs'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    version = Column(Integer, nullable=False)
    script = Column(Text, nullable=True)

    def __repr__(self):
        return f'<SchemaDesign(id={self.project_id}, project_id={self.user_story_count})>'


class ModelClass(Base):
    __tablename__ = 'model_classes'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    script = Column(Text, nullable=True)
    code = Column(Text, nullable=True)

    def __repr__(self):
        return f'<Model(project_id={self.project_id}, id={self.id})>'


class APIEndpointSchemas(Base):
    __tablename__ = 'api_endpoint_schemas'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    user_story_count = Column(Integer, nullable=False)
    json_schema_design = Column(Text)

    def __repr__(self):
        return f'<APIEndpointsSchema(project_id={self.project_id}, user_story_count={self.user_story_count}>, id={self.id})>'


class APIEndpointCode(Base):
    __tablename__ = 'api_endpoint_codes'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    user_story_count = Column(Integer, nullable=False)
    api_endpoint_schema_id = Column(Integer, ForeignKey('api_endpoint_schemas.id'), nullable=False)
    code = Column(Text)

    def __repr__(self):
        return f'<APIEndpointCode(project_id={self.project_id}, user_story_count={self.user_story_count}>, id={self.id})>'


class FrontendPage(Base):
    __tablename__ = 'frontend_pages'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    name = Column(String(255), nullable=False)
    purpose = Column(Text, nullable=False)
    html_code = Column(Text, nullable=True)
    css_code = Column(Text, nullable=True)
    js_code = Column(Text, nullable=True)

    def __repr__(self):
        return f'<FrontendPage(project_id={self.project_id}, id={self.id}, name={self.name})>'


class ApplicationRequirements(Base):
    __tablename__ = 'application_requirements'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    requirements = Column(Text, nullable=True)

    def __repr__(self):
        return f'<ApplicationRequirements(project_id={self.project_id}, id={self.id})>'


def initiate_database():
    if DATABASE == 'mysql':
        # Create database if not exists
        conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, port=int(PORT))
        cursor = conn.cursor()
        create_database_sql = "CREATE DATABASE IF NOT EXISTS `flask-ai`"
        cursor.execute(create_database_sql)
        cursor.close()
        conn.close()

        # Create all tables in the database
        engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/flask-ai')
        Base.metadata.create_all(engine)
    elif DATABASE == 'sqlite':
        if not os.path.exists(os.path.join(DIR_PATH, 'sqlite_db')):
            os.makedirs(os.path.join(DIR_PATH, 'sqlite_db'))

        engine = create_engine(f'sqlite:///{DIR_PATH}/sqlite_db/flask-ai.db')
        Base.metadata.create_all(engine)
    else:
        raise Exception(f'Database "{DATABASE}" not yet supported. Please use "mysql" or "sqlite".')


def get_session():
    initiate_database()

    if DATABASE == 'mysql':
        engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/flask-ai')
        Session = sessionmaker(bind=engine)
    else:
        engine = create_engine(f'sqlite:///{DIR_PATH}/sqlite_db/flask-ai.db')
        Session = sessionmaker(bind=engine)

    return Session()
