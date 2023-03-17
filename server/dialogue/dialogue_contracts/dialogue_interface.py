from abc import ABC, abstractmethod


class DialogueInterface(ABC):

    @abstractmethod
    def __doc__(self):
        intro_str = "Chatbot." + \
                    "\n" + "method:" + \
                    "\n" + "use start method to get congratulate the user and get start" + \
                    "\n" + "use scan(document) method to send a document as response to requirement" \
                           "and get next requirement. " + \
                    "\n" + "in_progress prop is True if the dialogue continues."
        return intro_str

    def __init__(self, remaining_requirements, upload_requirements, files_paths, scholarships_names, upload_attempt):
        """
        :param scholarships_names: the names of all the scholarships (use for identify and get requirements)
        :param upload_requirements: files_requirements- requirements that already uploaded
        :param files_paths: files_paths- all the files paths that already uploaded
        :param remaining_requirements: the remaining requirements
        """
        pass

    @property
    def in_progress(self):
        """:returns True when dialogue continues"""
        pass

    @property
    def remaining_requirements(self):
        """:returns the current remaining requirements """
        pass

    @property
    def upload_requirements(self):
        """:returns the current upload requirements """
        pass

    @property
    def files_paths(self):
        """:returns the current upload requirements files paths"""
        pass

    @property
    def scholarships_names(self):
        """:returns the current scholarshipsnames """
        pass

    @property
    def upload_attempt(self):
        pass

    @property
    def start(self):
        """
        :returns the start message
        """
        pass

    def get_next_requirement(self):
        """:returns next requirement"""

        pass

    def scan(self, file):
        """
        :param file: the file user upload as the desired requirement
        :returns response to document upload
        """
        pass
'''
    @abstractmethod
    def __init__(self, user_identifier, scholarships_names, dal_service, files_requirements, files_paths, submit_id):
        """

        :param user_identifier: the user identifier. user for correct saving the file
        :param scholarships_names: the names of all the scholarships (use for identify and get requirements)
        :param dal_service: dal_service
        :param files_requirements: files_requirements- requirements that already uploaded
        :param files_paths: files_paths- all the files paths that already uploaded
        :param submit_id: the id of this submit
        """
        pass

    @property
    def user_identifier(self):
        pass

    @property
    def in_progress(self):
        """ :returns True when dialogue continues"""
        pass


    @property
    def requirements(self):
        """:returns the current requirement """
        pass

    @property
    def uploads_documents(self):
        """:returns the scholarship name """
        pass

    @abstractmethod
    def start(self):
        """:returns the start message """
        pass

    @abstractmethod
    def welcome_back(self):
        """
        :returns welcome back message
        """
        pass
    @abstractmethod
    def get_next_requirement(self):
        """:returns next requirement"""
        pass

    @abstractmethod
    def scan(self, file_path):
        """:returns response to document upload  """
        pass

'''