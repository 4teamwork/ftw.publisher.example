from Acquisition import aq_parent, aq_inner, aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.statusmessages.interfaces import IStatusMessage
from ftw.publisher.example import _
from ftw.publisher.example import config


def is_temporary(obj, checkId=True):
    """Checks, whether an object is a temporary object (means it's in the
    `portal_factory`) or has no acquisition chain set up.
    Source: http://svn.plone.org/svn/collective/collective.indexing/trunk/collective/indexing/subscribers.py
    """
    parent = aq_parent(aq_inner(obj))
    if parent is None:
        return True
    if checkId and getattr(obj, 'getId', None):
        if getattr(aq_base(parent), obj.getId(), None) is None:
            return True
    isTemporary = getattr(obj, 'isTemporary', None)
    if isTemporary is not None:
        try:
            if obj.isTemporary():
                return True
        except TypeError:
            return True # `isTemporary` on the `FactoryTool` expects 2 args
    return False


def get_workflow_name(obj):
    """Returns the first configured workflow id for the object or None.
    """
    wftool = getToolByName(obj, 'portal_workflow')
    workflows = wftool.getWorkflowsFor(obj)
    if len(workflows)>0:
        return workflows[0].id
    else:
        return None


def is_published(obj):
    """Checks whether an object is in a workflow state which indicates that it
    is published. If the object has no workflow (policy configuration), it inherits
    the permission configuration from it's parent - so the state of the parent(s)
    is checked.
    """
    # when the plone site is reached, we have no workflows defined for the object
    # or any of it's parents.
    if IPloneSiteRoot.providedBy(obj):
        return False

    workflow = get_workflow_name(obj)

    if not workflow:
        # no workflow defined for this object - check the workflow of the parent
        return is_published(aq_parent(aq_inner(obj)))

    wf_tool = getToolByName(obj, 'portal_workflow')
    wf_state = wf_tool.getInfoFor(obj, 'review_state', None)

    return (workflow, wf_state) in config.PUBLISHED_STATES


def is_action_possible(obj, action, show_warnings=False, show_errors=False):
    """Checks whether it's possible to execute a certain publishing action
    on the object in it's current state.
    """
    # the plone site should never be published.
    if IPloneSiteRoot.providedBy(obj):
        return False

    errors = []
    warnings = []
    parent = aq_parent(aq_inner(obj))
    request = obj.REQUEST

    # parent should be published
    if action == 'push' and not is_published(parent) and \
            not IPloneSiteRoot.providedBy(parent):
        errors.append(_(u'error_parent_not_published',
                        default=u'Could not publish object: parent object ' +\
                            'must be published first!'))

    if action == 'submit' and not is_published(parent):
        warnings.append(_(u'warning_parent_not_published',
                          default=u'Parent object is not published: it ' +\
                              'must be published first.'))

    # check for referenced objects
    if action in ('submit', 'push'):
        try:
            references = obj.getReferences()
        except AttributeError:
            pass
        else:
            for refobj in references:
                if not is_published(refobj):
                    warnings.append(
                        _(u'warning_reference_not_published',
                          default=u'The referenced object ${Title} is not ' +\
                              'published yet. Maybe you should publish it too.',
                          mapping={'Title': refobj.pretty_title_or_id().decode(
                                    'utf-8')}))

    # referenced object still published
    if action in ('delete', 'retract', 'reject'):
        try:
            references = obj.getReferences()
        except AttributeError:
            pass
        else:
            for refobj in references:
                if is_published(refobj):
                    warnings.append(
                        _(u'warning_referenced_objects_still_published',
                          default=u'The referenced object ${Title} is still ' + \
                              'published.',
                          mapping={'Title': refobj.pretty_title_or_id().decode(
                                    'utf-8')}))

    if show_warnings:
        for msg in warnings:
            IStatusMessage(request).addStatusMessage(msg, type='warning')

    if show_errors:
        for msg in errors:
            IStatusMessage(request).addStatusMessage(msg, type='error')

    return len(errors)==0
