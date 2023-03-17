import json
import os

from server.services import scanner_service, resources_service
from server.logger import logger_service
from server.dialogue.dialogue_contracts.dialogue_interface import DialogueInterface


class DialogueImpl(DialogueInterface):

    def __doc__(self):
        intro_str = "Chatbot." + \
                    "\n" + "method:" + \
                    "\n" + "use start method to get congratulate the user and get start" + \
                    "\n" + "use scan(document) method to send a document as response to requirement" \
                           "and get next requirement. " + \
                    "\n" + "in_progress prop is True if the dialogue continues."
        doc_str = "version 3.0"
        return intro_str + '\n' + doc_str

    def __init__(self, remaining_requirements, upload_requirements,files_paths, scholarships_names, upload_attempt):
        """

        :param scholarships_names: the names of all the scholarships (use for identify and get requirements)
        :param upload_requirements: files_requirements- requirements that already uploaded
        :param files_paths: files_paths- all the files paths that already uploaded
        :param remaining_requirements: the remaining requirements
        """

        self._in_progress = True
        self._upload_requirements: [] = upload_requirements
        self._remaining_requirements: [] = remaining_requirements # Array containing all the "id"s of the
        self._files_paths: [] = files_paths
        self._upload_attempt = upload_attempt  # the number of attempted to upload file

        self._scholarships_names = scholarships_names  # scholarships name

    @property
    def in_progress(self):
        """:returns True when dialogue continues"""
        return self._in_progress

    @property
    def remaining_requirements(self):
        """:returns the current remaining requirements """
        return self._remaining_requirements

    @property
    def upload_requirements(self):
        """:returns the current upload requirements """
        return self._upload_requirements

    @property
    def files_paths(self):
        """:returns the current upload requirements files paths"""
        return self._files_paths

    @property
    def scholarships_names(self):
        """:returns the current scholarships names """
        return self._scholarships_names

    @property
    def upload_attempt(self):
        return self._upload_attempt

    @property
    def start(self):
        """
        :returns the start message
        """
        if not self._upload_requirements:
            return GENERAL_RESPONSES['congratulate']
        else:
            return GENERAL_RESPONSES['welcome_back']

    def get_next_requirement(self):
        """:returns next requirement"""

        # check if the conversation end
        if len(self._remaining_requirements) > 0:
            current_requirement = self._remaining_requirements[0]
            if current_requirement in INSTANCES:  # make sure that the current requirement is valid requirement
                retval = INSTANCES[current_requirement]['message']
            else:
                logger_service.error(f"{current_requirement} is invalid requirement")
                self._remaining_requirements.remove(current_requirement)
                retval = self.get_next_requirement()
            self._upload_attempt = 0
        else:
            self._in_progress = False
            retval = GENERAL_RESPONSES['all_done']
        return retval

    def scan(self, file):
        """
        :param file: the file user upload as the desired requirement
        :returns response to document upload
        """
        if len(self._remaining_requirements) > 0:
            requirement = self._remaining_requirements[0]
            current = INSTANCES[requirement]
            file_path = resources_service.save_file_locally(file, requirement)
            document_is_valid = scanner_service.scan(file_path, requirement)

            if document_is_valid:
                self._upload_attempt = 0
                retval = [current['name'] + " " + GENERAL_RESPONSES['success']]
                self._files_paths.append(file_path)
                self._upload_requirements.append(requirement)
                self._remaining_requirements.remove(requirement)
                retval.append(self.get_next_requirement())

            else:  # document is invalid
                resources_service.remove_file_locally(file_path)  # delete document file
                if self._upload_attempt < MAX_ATTEMPT:  # document is invalid and there more attempts
                    self._upload_attempt += 1
                    retval = [GENERAL_RESPONSES['failed']]
                else:  # document is invalid and there no any more attempts
                    self._in_progress = False
                    retval = [GENERAL_RESPONSES['failed']]
        else:  # no more requirements
            retval = self.get_next_requirement()
        return retval


# static variables
pointer = open("server/dialogue/assets/chat_instances.json", 'r', encoding="utf-8")
json_data = json.load(pointer)
INSTANCES = json_data['instances']  # chat messages: all the options for "requirements" (as json)
GENERAL_RESPONSES = json_data['static']  # general responses: all the general  messages
MAX_ATTEMPT = 3  # the max number of attempted to upload file
pointer.close()









'''
import json
import os

from server.services.scanner_service import scan
from server.dialogue.dialogue_contracts.dialogue_interface import DialogueInterface
from datetime import datetime
from server.dal.dal_contracts.dal_service_interface import DalServiceInterface


class DialogueImpl(DialogueInterface):

    def __doc__(self):
        intro_str = "Chatbot." + \
                    "\n" + "method:" + \
                    "\n" + "use start method to get congratulate the user and get start" + \
                    "\n" + "use scan(document) method to send a document as response to requirement" \
                           "and get next requirement. " + \
                    "\n" + "in_progress prop is True if the dialogue continues."
        doc_str = "version 3.0"
        return intro_str + '\n' + doc_str

    def __init__(self, user_identifier, scholarships_names, dal_service, files_requirements,files_paths,submit_id):
        """

        :param user_identifier: the user identifier. user for correct saving the file
        :param scholarships_names: the names of all the scholarships (use for identify and get requirements)
        :param dal_service: dal_service
        :param files_requirements: files_requirements- requirements that already uploaded
        :param files_paths: files_paths- all the files paths that already uploaded
        :param submit_id: the id of this submit
        """

        self.dal_service:DalServiceInterface = dal_service
        self._user_identifier = user_identifier
        self._scholarships_names = scholarships_names  # scholarships name
        self._requirements = self._get_requirements(scholarships_names)  # Array containing all the "id"s of the
        # requirements
        if len(files_requirements) > 1:
            # remove all requirements that already uploaded from all the requirements
            self._requirements = [requirement for requirement in self._requirements if requirement not in files_requirements]
        self._current_requirement_index = 0   # the current requirement index in the array _requirements
        self._num_of_requirements = len(self._requirements)  # the number of requirements
        self._upload_attempt = 0  # the number of attempted to upload file
        self._in_progress = True  # //chatbot status
        self._uploads = files_paths  # array of paths of the uploads requirements

    @property
    def user_identifier(self):
        return self._user_identifier

    @property
    def in_progress(self):
        """:returns True when dialogue continues"""
        return self._in_progress

    @property
    def requirements(self):
        """:returns the current requirement """
        return self._requirements


    @property
    def uploads_documents(self):
        """:returns the scholarship name """
        return self._uploads

    def start(self):
        """
        :returns the start message
        """
        return GENERAL_RESPONSES['congratulate']

    def welcome_back(self):
        """
        :returns welcome back message
        """
        return GENERAL_RESPONSES['welcome_back']

    def get_next_requirement(self):
        """:returns next requirement"""

        # check if the conversation end
        if self._current_requirement_index < self._num_of_requirements:
            current_requirement = self._requirements[self._current_requirement_index]
            if current_requirement in INSTANCES:  # make sure that the current requirement is valid requirement
                retval = INSTANCES[current_requirement]['message']
            else:
                print(f"{current_requirement} is invalid requirement")
                self._current_requirement_index += 1
                retval =  self.get_next_requirement()
            self._upload_attempt = 0
        else:
            self._in_progress = False
            retval = GENERAL_RESPONSES['all_done']
        return retval

    def scan(self, file):
        """
        :param file: the file user upload as the desired requirement
        :returns response to document upload
        """
        requirement = self.requirements[self._current_requirement_index]
        current = INSTANCES[requirement]
        file_path = _save_file_locally(file, self._user_identifier, requirement)
        document_is_valid = scan(file_path, requirement)

        if document_is_valid:
            self._upload_attempt = 0
            retval = [current['name'] + " " + GENERAL_RESPONSES['success']]

            if self._save_upload(file_path):
                self._current_requirement_index += 1 # move to next requirement
                retval.append(self.get_next_requirement())
            else:
                raise TypeError(f"cannot save document {file_path} in DB")
                retval = GENERAL_RESPONSES["error_message"]

        else:  # document is invalid
            os.remove(file_path)  # delete document file
            if self._upload_attempt < MAX_ATTEMPT:  # document is invalid and there more attempts
                self._upload_attempt += 1
                retval = [GENERAL_RESPONSES['failed']]
            else:  # document is invalid and there no any more attempts
                """
                    add some code...
                    for this moment nothing happened here
                """
                retval = [GENERAL_RESPONSES['failed']]

        return retval


    def _save_upload(self, file_path):
        """
        save the valid uploads
        :param file_path: the documents location
        :return:
        """
        resp = self.dal_service.add_file(self.user_identifier, file_path)
        if not resp["status"]:
            print(f"Add file to db failed. user identifier: {self.user_identifier}, file_path: {file_path}. "
                  f"db response {resp['status']}.")
        self._uploads.append(file_path)

        return True

    def _get_requirements(self, scholarships_names):
        """
        :param scholarships_names: array of the names of the requested scholarships
        :return: all the requirements for scholarship
        """
        # asdsdf = self.dal_service.get_requirements(scholarships_names)
        # return self.dal_service.get_requirements(scholarships_names)

        return ["candidate_id", "candidate_current_account",
                "father_vehicle_licence"]

# def _save_file_locally(file, user_id, requirement):
#     """
#     :param file: the document who will scan / the documents the user sent
#     :param user_id: the id of the user
#     :param requirement: the current requirement / the requirement of this document
#     :return: the path who the file saved at
#     """
#
#     dt_string = datetime.now().strftime("%d_%m_%Y %H_%M_%S")
#
#     file_path = f"{requirement} {dt_string}.{file.content_type[file.content_type.index('/') + 1:]}"
#     print(os.path.abspath(file_path))
#     file.save(file_path)
#
#     return file_path

def _save_file_locally(file, user_id, requirement):
    """
    :param file: the document who will scan / the documents the user sent
    :param user_id: the id of the user
    :param requirement: the current requirement / the requirement of this document
    :return: the path who the file saved at
    """
    file_type = constant.Accepted_type = f".{file.content_type[file.content_type.index('/') + 1:]}"
    relative_path: str = "Uploaded files"  # The directory in which the files will be stored
    dt_string = datetime.now().strftime("%d_%m_%Y %H_%M_%S")
    folder = relative_path + "//" + str(user_id)
    file_path = f"{folder}/{requirement} {dt_string}{file_type}"
    file_path = os.path.abspath(file_path)

    print("please make sure that this path exist on your computer:")
    print(os.path.abspath(relative_path))
    print("The file will be saved in folder: " ,os.path.abspath(folder))

    if not os.path.exists(os.path.abspath(folder)):
        os.mkdir(folder)
    file.save(file_path)
    # file_path = os.path.abspath(file_path)
    return file_path


# static variables
pointer = open('server\\assets\\chat_instances.json', 'r', encoding="utf-8")
json_data = json.load(pointer)
INSTANCES = json_data['instances']  # chat messages: all the options for "requirements" (as json)
GENERAL_RESPONSES = json_data['static']  # general responses: all the general  messages
MAX_ATTEMPT = 3  # the max number of attempted to upload file
pointer.close()

'''