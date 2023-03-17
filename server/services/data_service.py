from server.dal.dal_contracts.interface_data_dal import IDataDal
from server.injector.dependency_injector import get_singleton
from server.schemas import regular_expressions

data_dal: IDataDal = get_singleton(IDataDal)


def get_regex_pattern():
    return regular_expressions.RegularExpression()


def get_regex_pattern_by_name(regex_name):
    return {'regex': regular_expressions.RegularExpression().get_child_dict().get(regex_name, None)}


async def get_data_by_id(data_id):
    response = await data_dal.get_data_by_id(data_id)
    if response:
        return response.get("data", None)
    else:
        return None
