# -*- coding: utf-8 -*-
# Based on: https://github.com/scholrly/lucene-querybuilder/blob/master/lucenequerybuilder/query.py


class BaseQ(object):
    """
    Q is a query builder for the Neo4j Cypher language backend

    It allows to build filters like
    Q("Artwork title", istartswith="copy", nullable=False)
    Q(property="Artwork title", lookup="istartswith", match="copy")
    """

    matchs = ("exact", "iexact",
              "contains", "icontains",
              "startswith", "istartswith",
              "endswith", "iendswith",
              "regex", "iregex",
              "gt", "gte", "lt", "lte",
              "in", "inrange", "isnull",
              "eq", "equals", "neq", "notequals")

    def __init__(self, property=None, lookup=None, match=None,
                 nullable=None, var=u"n", **kwargs):
        self._and = None
        self._or = None
        self._not = None
        self.property = property
        self.lookup = lookup
        self.match = match
        self.nullable = nullable
        self.var = var
        if property and (not self.lookup or not self.match):
            for m in self.matchs:
                if m in kwargs:
                    self.lookup = m
                    self.match = kwargs[m]
                    break
            else:
                all_matchs = ", ".join(self.matchs)
                raise ValueError("Q objects must have at least a lookup method"
                                 " (%s) and a match case".format(all_matchs))

    def _make_and(q1, q2):
        q = q1.__class__()
        q._and = (q1, q2)
        return q

    def _make_not(q1):
        q = q1.__class__()
        q._not = q1
        return q

    def _make_or(q1, q2):
        q = q1.__class__()
        q._or = (q1, q2)
        return q

    def __and__(self, other):
        return BaseQ._make_and(self, other)

    def __or__(self, other):
        return BaseQ._make_or(self, other)

    def __invert__(self):
        return BaseQ._make_not(self)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.property, self.lookup, self.match,
                     self.nullable))

    def get_query_objects(self, var=None, prefix=None, params=None):
        """
        :return query, params: Query string and a dictionary for lookups
        """
        # return query, params
        raise NotImplementedError("Method has to be implemented")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        query, params = self.get_query_objects()
        return query.format(**params)
