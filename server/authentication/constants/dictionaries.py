from server.authentication.enums.authorization_level import AuthorizationLevel
from server.constants.database_constants.objnames import ObjNames
from server.models.users.authorized_user import AuthorizedUser
from server.models.users.candidates_user import CandidatesUser
from server.models.users.helpdesk_user import HelpDeskUser
from server.models.users.organizations_user import OrganizationsUser

collection_names_dictionary = {
    AuthorizationLevel.registered_candidate: ObjNames.Candidates,
    AuthorizationLevel.organizations: ObjNames.Contact,
    AuthorizationLevel.signed_up: ObjNames.SignedUp,
    AuthorizationLevel.help_desk_user: ObjNames.HelpDeskUser
}

usr_model_dictionary = {
        AuthorizationLevel.registered_candidate: CandidatesUser,
        AuthorizationLevel.organizations: OrganizationsUser,
        AuthorizationLevel.authorized: AuthorizedUser,
        AuthorizationLevel.candidates: AuthorizedUser,
        AuthorizationLevel.signed_up: AuthorizedUser,
        AuthorizationLevel.help_desk_user: HelpDeskUser
    }