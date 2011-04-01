from Products.Five.browser import BrowserView
from ftw.publisher.example.interfaces import IPublisherWorkflowController
from ftw.publisher.example.utils import is_action_possible
from zExceptions import Redirect
from zope.interface import implements


class PublisherWorkflowControllerView(BrowserView):
    """The "@@publisher-workflow-controller" view checks whether certain workflow
    transitions are allowed to execute
    """

    implements(IPublisherWorkflowController)


    def check_publish_allowed(self, state_change):
        if not is_action_possible(self.context, 'push',
                                  show_warnings=True, show_errors=True):
            raise Redirect(self.request.get('HTTP_REFERER'))
        else:
            return state_change

    def check_reject_allowed(self, state_change):
        if not is_action_possible(self.context, 'reject',
                                  show_warnings=True, show_errors=True):
            raise Redirect(self.request.get('HTTP_REFERER'))
        else:
            return state_change

    def check_retract_allowed(self, state_change):
        if not is_action_possible(self.context, 'retract',
                                  show_warnings=True, show_errors=True):
            raise Redirect(self.request.get('HTTP_REFERER'))
        else:
            return state_change

    def check_revise_allowed(self, state_change):
        if not is_action_possible(self.context, 'revise',
                                  show_warnings=True, show_errors=True):
            raise Redirect(self.request.get('HTTP_REFERER'))
        else:
            return state_change

    def check_submit_allowed(self, state_change):
        if not is_action_possible(self.context, 'submit',
                                  show_warnings=True, show_errors=True):
            raise Redirect(self.request.get('HTTP_REFERER'))
        else:
            return state_change
