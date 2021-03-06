from sqlalchemy.sql.base import _generative
from sqlalchemy.sql.expression import Executable, ClauseElement


class BaseMatchClause(ClauseElement):
    def __init__(self, then, by="target", and_=None):
        if by not in {"target", "source"}:
            raise ValueError("by must be one of [source|target]")

        self.then = then
        self.and_ = MergeSearchConditionClause(and_)
        self.by = by


class WhenNotMatchedClause(BaseMatchClause):
    __visit_name__ = "when_not_matched"


class WhenMatchedClause(BaseMatchClause):
    __visit_name__ = "when_matched"


class MergeSearchConditionClause(ClauseElement):
    __visit_name__ = "merge_search_condition"

    def __init__(self, binary_expression):
        self.binary_expression = binary_expression


class Merge(Executable, ClauseElement):
    __visit_name__ = "merge"
    _returning = None

    def __init__(self, source, target, condition):
        self.target = target
        self.source = source
        self.merge_condition = condition
        self.when_clauses = tuple()

    @_generative
    def when_matched(self, *args, **kw):
        self.when_clauses += (WhenMatchedClause(*args, **kw), )

    @_generative
    def when_not_matched(self, *args, **kw):
        self.when_clauses += (WhenNotMatchedClause(*args, **kw), )


class MergeInsertClause(ClauseElement):
    __visit_name__ = "merge_insert"

    def __init__(self, values):
        self.values = values


class MergeUpdateClause(ClauseElement):
    __visit_name__ = "merge_update"

    def __init__(self, values):
        self.values = values


class MergeDeleteClause(ClauseElement):
    __visit_name__ = "merge_delete"
    pass


def clause_factory(cls):
    """
        Allow clauses to be imported similar to other SQLAlchemy DML clauses (i.e., `from sqlalchemy.sql import insert`)
    """
    def factory(*args, **kwargs):
        return cls(*args, **kwargs)
    return factory


merge = clause_factory(Merge)
merge_insert = clause_factory(MergeInsertClause)
merge_update = clause_factory(MergeUpdateClause)
merge_delete = clause_factory(MergeDeleteClause)
