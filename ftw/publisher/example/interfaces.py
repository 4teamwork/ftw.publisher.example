from zope.interface import Interface


class IPublisherWorkflowController(Interface):
    """Interface for allowing attribute traversal on the
    "@@publisher-workflow-controller" view.
    """

    def check_publish_allowed(self):
        pass

    def check_reject_allowed(self):
        pass

    def check_retract_allowed(self):
        pass

    def check_revise_allowed(self):
        pass

    def check_submit_allowed(self):
        pass
