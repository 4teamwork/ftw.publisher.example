# List of transactions which triger a publisher "push" job.
# Tuple of workflow-id and transaction-id for each transaction.
PUSH_TRANSITIONS = (
    ('publisher_workflow', 'publish'),
    ('publisher_workflow', 'retract'),
    )


# List of transactions which triger a publisher "delete" job.
# Be careful, usually it's not good to delete objects on workflow
# state changes!
# See: https://github.com/4teamwork/ftw.publisher.sender/wiki/Integration
DELETE_TRANSITIONS = (
    )


# List of workflow states, on which objects are visible to anonymous users.
PUBLISHED_STATES = (
    ('publisher_workflow', 'published'),
    ('publisher_workflow', 'revision'),
    )


# List of workflows, for which publishing is configured.
PUBLISHING_WORKFLOWS = dict(
    list(PUSH_TRANSITIONS) +
    list(DELETE_TRANSITIONS) +
    list(PUBLISHED_STATES)
    ).keys()
