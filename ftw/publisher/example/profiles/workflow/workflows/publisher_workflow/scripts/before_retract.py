## Script (Python) "before_retract"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=state_change
##title=
##
obj = state_change.object

try:
    view = obj.restrictedTraverse('@@publisher-workflow-controller')
except KeyError, AttributeError:
    return state_change
else:
    return view.check_retract_allowed(state_change)
