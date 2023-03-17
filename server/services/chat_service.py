from flask_login import current_user
from . import submissions_service
from server.injector.dependency_injector import get_transient, get_singleton
from server.dialogue.dialogue_contracts.dialogue_interface import DialogueInterface
from ..base_services.base_controller import ok, custom_error_resp
from server.constants.fields_name.dialogue_fields import DialogueFields
from ..constants.error_constants import ErrorConstant
from ..dal.dal_contracts.interface_users_dal import IUsersDal

user_dal: IUsersDal = get_singleton(IUsersDal)


async def start_scholarship_submission_chat(scholarships_names):
    """
    :param scholarships_names: the name of the requested scholarship
    :return: json with the fields 'inProgress' and 'messages'
    """
    dialogue_obj = await _get_dialogue_obj()
    if dialogue_obj is None:
        requirements = submissions_service.get_requirements(scholarships_names)
        dialogue_instance = get_transient(DialogueInterface, requirements, [], [], scholarships_names, 0)
        await _update_chat_instance(dialogue_instance, is_update=False, is_active=dialogue_instance.in_progress)
    else:
        dialogue_instance = get_transient(DialogueInterface, dialogue_obj[DialogueFields.remaining_requirements],
                                          dialogue_obj[DialogueFields.upload_requirements],
                                          dialogue_obj[DialogueFields.files_paths],
                                          dialogue_obj[DialogueFields.scholarships_names],
                                          dialogue_obj[DialogueFields.upload_attempt])

    messages = [dialogue_instance.start, dialogue_instance.get_next_requirement()]
    return ok(inProgress=dialogue_instance.in_progress, messages=messages)


async def scholarship_submission_chat_scan_and_next(file):
    """"
        :param file: the file that uploaded for scanning to the server.
        :return: json with the fields 'inProgress' and 'messages'
    """
    dialogue_obj = await _get_dialogue_obj()
    if dialogue_obj is not None:
        dialogue_instance = get_transient(DialogueInterface, dialogue_obj[DialogueFields.remaining_requirements],
                                          dialogue_obj[DialogueFields.upload_requirements],
                                          dialogue_obj[DialogueFields.files_paths],
                                          dialogue_obj[DialogueFields.scholarships_names],
                                          dialogue_obj[DialogueFields.upload_attempt])
        messages = dialogue_instance.scan(file)
        in_progress = dialogue_instance.in_progress
        if not in_progress:
            res = await submissions_service.send_submission(dialogue_instance.scholarships_names,
                                                                       dialogue_instance.files_paths)
            if res is None:
                await _update_chat_instance(dialogue_instance, is_update=True, is_active=True)
                return custom_error_resp(400, inProgress=in_progress, messages=[ErrorConstant.SubmitError.value])
            messages.append(res)
        await _update_chat_instance(dialogue_instance, is_update=True, is_active=in_progress)
        return ok(inProgress=in_progress, messages=messages)

    else:
        error_message = f"{ErrorConstant.NoOpenChat.value} {current_user.get_id()}"
        print(error_message)
        return custom_error_resp(400, inProgress=False, messages=[error_message])


async def close_scholarship_submission_chat():
    await user_dal.update_dialogue_obj(is_active=False)


def _get_dialogue_obj():
    return user_dal.get_dialogue_obj()


async def _update_chat_instance(dialogue_instance: DialogueInterface, is_update, is_active):
    await user_dal.update_dialogue_obj(remaining_requirements=dialogue_instance.remaining_requirements,
                                       upload_requirements=dialogue_instance.upload_requirements,
                                       files_paths=dialogue_instance.files_paths,
                                       upload_attempt=dialogue_instance.upload_attempt,
                                       scholarships_names=dialogue_instance.scholarships_names,
                                       is_update=is_update, is_active=is_active)
