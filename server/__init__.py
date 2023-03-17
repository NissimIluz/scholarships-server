from flask import Flask
from flask_login import LoginManager
from server.injector import dependency_injector
from server import configuration


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = configuration.encryption_key
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = configuration.sql_name
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    app.config["MONGO_URI"] = configuration.mangoDB_connection

    # init dal
    ## import dal_services
    from server.dal.dal_contracts.interface_contact_us_dal import IContactUsDal
    from server.dal.dal_contracts.interface_submission import ISubmissionsDal
    from server.dal.infra_dal.interface_database import IDal
    from server.dal.dal_contracts.interface_organizations_dal import IOrganizationsDal
    from server.dal.dal_contracts.interface_scholarships_dal import IScholarshipsDal
    from server.dal.dal_contracts.interface_users_dal import IUsersDal
    from server.dal.dal_contracts.interface_resources_dal import IResourcesDal
    from server.dal.dal_contracts.interface_data_dal import IDataDal
    from server.dal.dal_contracts.interface_helpdesk_dal import IHelpdeskDal

    ## init database
    database: IDal = dependency_injector.get_singleton(IDal)
    dependency_injector.get_singleton(IUsersDal, database)
    dependency_injector.get_singleton(IOrganizationsDal, database)
    dependency_injector.get_singleton(IScholarshipsDal, database)
    dependency_injector.get_singleton(ISubmissionsDal, database)
    dependency_injector.get_singleton(IContactUsDal, database)
    dependency_injector.get_singleton(IResourcesDal, database)
    dependency_injector.get_singleton(IDataDal, database)
    dependency_injector.get_singleton(IHelpdeskDal, database)

    # load controllers
    ## import to controllers
    from .controllers.chatbot_controller import chatbot_controller
    from .controllers.candidates_controller import candidates_controller
    from .controllers.scholarship_controller import scholarships_controller
    from .controllers.organizations_controller import organizations_controller
    from .controllers.submissions_controller import submissions_controller
    from .controllers.contact_us_controller import contact_us_controller
    from .controllers.data_controller import data_controller
    from .controllers.helpdesk_controller import helpdesk_controller

    ## register controllers
    app.register_blueprint(chatbot_controller, url_prefix='/chat')
    app.register_blueprint(candidates_controller, url_prefix='/candidates')
    app.register_blueprint(scholarships_controller, url_prefix='/scholarships')
    app.register_blueprint(organizations_controller, url_prefix='/organization')
    app.register_blueprint(submissions_controller, url_prefix='/submissions')
    app.register_blueprint(contact_us_controller, url_prefix='/contactUs')
    app.register_blueprint(data_controller, url_prefix='/data')
    app.register_blueprint(helpdesk_controller, url_prefix='/helpdesk')
    return app
