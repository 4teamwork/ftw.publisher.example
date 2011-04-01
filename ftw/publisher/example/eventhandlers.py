from ftw.publisher.example import config
from ftw.publisher.example.utils import get_workflow_name
from ftw.publisher.example.utils import is_temporary, is_action_possible
from plone.app.linkintegrity.interfaces import ILinkIntegrityInfo


_marker = '_publisher_event_already_handled'


def publish_after_transition(obj, event):
    """ This event handler is executed after each transition and
    publishes the object with ftw.publisher on certain transitions.

    Also when retracting an object, the object will be published,
    since we should not delete anything unless it's delete from the
    sender instance too. This is necessary for preventing
    inconsistency, which could occur when deleting a folder which
    contains published objects on the reciever site.
    """

    # the event handler will be run multiple times, so we need to
    # remember which event we've already handled.
    if getattr(event, _marker, False):
        return
    else:
        setattr(event, _marker, True)

    # when there is no transition for the state change, we do nothing
    if not event.transition:
        return

    # do nothing with temprorary objects
    if is_temporary(obj):
        return

    # check if we should handle this transaction
    wf_transition = (event.workflow.__name__, event.transition.__name__)
    if wf_transition in config.PUSH_TRANSITIONS:
        action = 'push'
    elif wf_transition in config.DELETE_TRANSITIONS:
        action = 'delete'
    else:
        return

    if is_action_possible(obj, action):
        if action == 'push':
            obj.restrictedTraverse('publisher.publish')()
        elif action == 'delete':
            obj.restrictedTraverse('publisher.delete')()


def handle_remove_event(obj, event):
    """If an object will be removed on the senders instance, we need to create a
    publisher delete job.
    """
    # the event is notified for every subobject, but we only want to check
    # the top object which the users tries to delete
    if obj is not event.object:
        return

    workflow = get_workflow_name(obj)
    if not workflow or workflow not in config.PUBLISHING_WORKFLOWS:
        # we don't have a workflow or the workflow does not publish ever - so we
        # don't need to delete anything on the receiver.
        return

    # the event handler is fired twice (once from link integrity check), but
    # we just want to do our stuff once. And we should only do it if the user
    # already did confirm.
    do_delete = False
    request = getattr(obj, 'REQUEST', None)
    if request is None:
        do_delete = True
    else:
        info = ILinkIntegrityInfo(request)
        if not info.integrityCheckingEnabled():
            do_delete = True
        elif info.isConfirmedItem(obj):
            do_delete = True

    if request.URL.endswith('/sl_delete_object'):
        do_delete = True
    if request.has_key('form.submitted') and \
            request.URL.endswith('/delete_confirmation'):
        do_delete = True
    if request.URL.endswith('/folder_delete'):
        do_delete = True
    if request.has_key('form.button.Cancel'):
        do_delete = True

    # register the job
    if do_delete:
        obj.restrictedTraverse('@@publisher.delete')()
