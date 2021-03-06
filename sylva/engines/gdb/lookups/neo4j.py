# -*- coding: utf-8 -*-
from engines.gdb.lookups import BaseQ


class Q(BaseQ):
    # matchs = ("exact", "iexact",
    #           "contains", "icontains",
    #           "startswith", "istartswith",
    #           "endswith", "iendswith",
    #           "regex", "iregex",
    #           "gt", "gte", "lt", "lte",
    #           "in", "inrange", "isnull",
    #           "eq", "equals", "neq", "notequals")

    def _escape(self, s):
        # if isinstance(s, basestring):
        #     query = ''
        #     specialchars = self.specialchars.translate(None,'*?')\
        #             if self.allow_wildcard else self.specialchars
        #     for c in s:
        #         if c in specialchars:
        #             query += '\\' + c
        #         else:
        #             query += c
        #     return query
        # match = unicode(lookup["match"]).replace(u"'", u"\\'")
        return s

    def _get_lookup_and_match(self):
        if self.lookup == "exact":
            lookup = u"="
            match = u"'{0}'".format(self.match)
        elif self.lookup == "iexact":
            lookup = u"=~"
            match = u"'(?i){0}'".format(self.match)
        elif self.lookup == "contains":
            lookup = u"=~"
            match = u"'.*{0}.*'".format(self.match)
        elif self.lookup == "icontains":
            lookup = u"=~"
            match = u"'(?i).*{0}.*'".format(self.match)
        elif self.lookup == "startswith":
            lookup = u"=~"
            match = u"'{0}.*'".format(self.match)
        elif self.lookup == "istartswith":
            lookup = u"=~"
            match = u"'(?i){0}.*'".format(self.match)
        elif self.lookup == "endswith":
            lookup = u"=~"
            match = u"'.*{0}'".format(self.match)
        elif self.lookup == "iendswith":
            lookup = u"=~"
            match = u"'(?i).*{0}'".format(self.match)
        elif self.lookup == "regex":
            lookup = u"=~"
            match = u"'{0}'".format(self.match)
        elif self.lookup == "iregex":
            lookup = u"=~"
            match = u"'(?i){0}'".format(self.match)
        elif self.lookup == "gt":
            lookup = u">"
            match = u"{0}".format(self.match)
        elif self.lookup == "gte":
            lookup = u">"
            match = u"{0}".format(self.match)
        elif self.lookup == "lt":
            lookup = u"<"
            match = u"{0}".format(self.match)
        elif self.lookup == "lte":
            lookup = u"<"
            match = u"{0}".format(self.match)
        elif self.lookup in ["in", "inrange"]:
            lookup = u"IN"
            match = u"['{0}']".format(u"', '".join([self._escape(m)
                                      for m in self.match]))
        elif self.lookup == "isnull":
            if self.match:
                lookup = u"="
            else:
                lookup = u"<>"
            match = u"null"
        elif self.lookup in ["eq", "equals"]:
            lookup = u"="
            match = u"'{0}'".format(self._escape(self.match))
        elif self.lookup in ["neq", "notequals"]:
            lookup = u"<>"
            match = u"'{0}'".format(self._escape(self.match))
        else:
            lookup = self.lookup
            match = u""
        return lookup, match

    def get_query_objects(self, var=None, prefix=None, params=None):
        if var:
            self.var = var
        if not params:
            params = {}
        if not prefix:
            prefix = u""
        else:
            params.update(params)
        if self._and is not None:
            left_and = self._and[0].get_query_objects(params=params)
            params.update(left_and[1])
            right_and = self._and[1].get_query_objects(params=params)
            params.update(right_and[1])
            query = u"( {0} AND {1} )".format(left_and[0], right_and[0])
        elif self._not is not None:
            op_not = self._not.get_query_objects(params=params)
            params.update(op_not[1])
            query = u"NOT ( {0} )".format(op_not[0])
        elif self._or is not None:
            left_or = self._or[0].get_query_objects(params=params)
            params.update(left_or[1])
            right_or = self._or[1].get_query_objects(params=params)
            params.update(right_or[1])
            query = u"( {0} OR {1} )".format(left_or[0], right_or[0])
        else:
            query = u""
            lookup, match = self._get_lookup_and_match()
        if self.property is not None and self.var is not None:
            key = u"{0}p{1}".format(prefix, len(params))
            property = unicode(self.property).replace(u"`", u"\\`")
            if self.nullable is True:
                nullable = u"?"
            elif self.nullable is False:
                nullable = u"!"
            else:
                nullable = u""
            params[key] = match
            try:
                query_format = u"{0}.`{1}`{2} {3} {{{4}}}"
                query = query_format.format(self.var, property, nullable,
                                            lookup, key)
            except AttributeError:
                query = u"%s.`%s`%s %s {%s}" % (self.var, property, nullable,
                                                lookup, key)
        return query, params
