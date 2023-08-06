from django.contrib.postgres.fields import ArrayField
from django.db import models
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet

class SubnetAllocations(NetBoxModel):
    node_id = models.PositiveIntegerField(
        primary_key = True
    )
    prefix = models.ForeignKey(
        to='ipam.Prefix',
        on_delete=models.PROTECT,
        related_name='+',
        blank=False,
        null=False
    )
    cidr = models.PositiveIntegerField(
        validators=[MinValueValidator(8), MaxValueValidator(31)]
    )
    supernet = models.ForeignKey(
        to='ipam.Prefix',
        on_delete=models.PROTECT,
        related_name='+',
        blank=False,
        null=False
    )
    parent = models.ForeignKey(
        to='self',
        on_delete=models.PROTECT,
        related_name='+',
        blank=False,
        null=False
    )
    children = ArrayField(
        base_field = models.PositiveIntegerField(),
        size=2,
        null=True,
        blank=True
    )
    allocated = models.BooleanField(
        default=False
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )
    created_by = models.ForeignKey(
        to='users.Tokens', 
        on_delete=models.PROTECT,
        related_name='+',
        blank=False,
        null=False)

    class Meta:
        ordering = ('supernet','cidr')

    def __str__(self):
        return self.prefix

    