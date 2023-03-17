from server.dal.dal_contracts.interface_helpdesk_dal import IHelpdeskDal
from server.injector.dependency_injector import get_singleton

helpdesk_dal: IHelpdeskDal = get_singleton(IHelpdeskDal)


def get_students(skip, take, s_phone_number, s_email, s_first_name, s_last_name, s_id, s_phrase, only_active,
                 order_by, order_direction):
    return helpdesk_dal.get_students(skip, take, s_phone_number, s_email, s_first_name, s_id, s_last_name,
                                     s_phrase, only_active, order_by, order_direction)


