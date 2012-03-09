# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from django.db import models

from base.fields import AutoSlugField


class Schema(models.Model):
    # graph = models.OneToOneField(Graph, verbose_name=_('graph'))
    options = models.TextField(_('options'), null=True, blank=True)

    class Meta:
        permissions = (
            ('view_schema', _('View schema')),
        )

    def __unicode__(self):
        try:
            return _(u"Schema for \"%s\"") % (self.graph.name)
        except ObjectDoesNotExist:
            return _(u"Schema \"%s\"") % (self.id)

    def export(self):
        schema_dict = {}
        schema_dict["node_types"] = []
        for node_type in self.nodetype_set.all():
            schema_dict["node_types"].append(node_type)
        schema_dict["relationship_types"] = []
        for r_type in self.relationshiptype_set.all():
            schema_dict["relationship_types"].append(r_type)
        return schema_dict

    @models.permalink
    def get_absolute_url(self):
        return ('schemas.views.edit', [str(self.id)])


class BaseType(models.Model):
    name = models.CharField(_('name'), max_length=150)
    slug = AutoSlugField(populate_from=['name'], max_length=200,
                         editable=False)
    plural_name = models.CharField(_('plural name'), max_length=175,
                                   null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)
    schema = models.ForeignKey(Schema)
    order = models.IntegerField(_('order'), null=True, blank=True)
    total = models.IntegerField(_("total objects"), default=0)
    validation = models.TextField(_('validation'), blank=True, null=True)

    class Meta:
        unique = ("slug", )
        abstract = True
        ordering = ("order", "name")


class NodeType(BaseType):
    inheritance = models.ForeignKey('self', null=True, blank=True,
                                    verbose_name=_("inheritance"),
                                    help_text=_("Choose the type which " \
                                                "properties will be " \
                                                "inherited from"))

    def __unicode__(self):
        return "%s" % (self.name)

    def get_incoming_relationships(self):
        return RelationshipType.objects.filter(target=self)

    def get_outgoing_relationships(self):
        return RelationshipType.objects.filter(source=self)

    def all(self):
        if self.id:
            return self.schema.graph.nodes.filter(label=self.id)
        else:
            return []


class RelationshipType(BaseType):
    inverse = models.CharField(_('inverse name'), max_length=150,
                               null=True, blank=True,
                               help_text=_("For example, " \
                                           "if name is \"writes\", inverse " \
                                           "is \"written by\""))
    plural_inverse = models.CharField(_('plural inverse name'), max_length=175,
                                      null=True, blank=True)
    inheritance = models.ForeignKey('self', null=True, blank=True,
                                    verbose_name=_("inheritance"),
                                    help_text=_("Choose the type which " \
                                                "properties will be " \
                                                "inherited from"))
    source = models.ForeignKey(NodeType, related_name='outgoing_relationships',
                               verbose_name=_("source"),
                               help_text=_("Source type of the " \
                                           "allowed relationship"))
    target = models.ForeignKey(NodeType, related_name='incoming_relationships',
                               verbose_name=_("target"),
                               help_text=_("Target type of the " \
                                           "allowed relationship"))
    arity_source = models.IntegerField(_('Source arity'), default=0, blank=True,
                                help_text=_("Leave blank for infinite arity,"
                                            "or type with format min:max."))
    arity_target = models.IntegerField(_('Target arity'), default=0, blank=True,
                                help_text=_("Leave blank for infinite arity,"
                                            "or type with format min:max."))

    def save(self, *args, **kwargs):
        if not self.arity_source or self.arity_source < 1:
            self.arity_source = 0
        if not self.arity_target or self.arity_target < 1:
            self.arity_target = 0
        super(RelationshipType, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s %s %s' % (self.source.name, self.name, self.target.name)


class BaseProperty(models.Model):
    key = models.CharField(_('key'), max_length=50)
    slug = AutoSlugField(populate_from=['key'], max_length=750,
                         editable=False)
    default = models.CharField(_('default value'), max_length=255,
                               blank=True, null=True)
    value = models.CharField(_('value'), max_length=255, blank=True)
    DATATYPE_CHOICES = (
        (u'u', _(u'Default')),
        (u'n', _(u'Number')),
        (u's', _(u'String')),
        (u'b', _(u'Boolean')),
        (u'd', _(u'Date')),
        (u't', _(u'Time')),
        (u'o', _(u'Options')),
    )
    datatype = models.CharField(_('data type'),
                                max_length=1, choices=DATATYPE_CHOICES,
                                default=u"u")
    required = models.BooleanField(_('is required?'), default=False)
    display = models.BooleanField(_('is required?'), default=False)
    description = models.TextField(_('description'), blank=True, null=True)
    validation = models.TextField(_('validation'), blank=True, null=True)
    order = models.IntegerField(_('order'), blank=True, null=True)

    class Meta:
        unique = ("slug", )
        abstract = True
        ordering = ("order", )

    def __unicode__(self):
        return "%s: %s" % (self.key, self.value)

    def get_datatype_dict(self):
        return dict([(v.lower(), u) for (u, v) in self.DATATYPE_CHOICES])

    def get_datatype(self):
        datatype_dict = dict(self.DATATYPE_CHOICES)
        return datatype_dict.get(self.datatype)


class NodeProperty(BaseProperty):
    node = models.ForeignKey(NodeType, verbose_name=_('node'),
                             related_name="properties")

    class Meta:
        verbose_name_plural = _("Node properties")


class RelationshipProperty(BaseProperty):
    relationship = models.ForeignKey(RelationshipType,
                                     verbose_name=_('relationship'),
                                     related_name="properties")

    class Meta:
        verbose_name_plural = _("Relationship properties")
