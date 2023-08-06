from cProfile import label
import imp
from django import forms
from django.conf import settings

from django.utils.translation import gettext as _

from dcim.models import Device, Site, Region, DeviceRole, Location, Rack

from django import forms
from dcim.choices import DeviceStatusChoices
from tenancy.models import TenantGroup, Tenant
from tenancy.forms import TenancyFilterForm
from django.conf import settings
from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelForm
from utilities.forms.fields import (
    TagFilterField,
    DynamicModelMultipleChoiceField,
    MultipleChoiceField
)


from .models import IndividualOptions

class DeviceFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = Device
    fieldsets = (
        (
            None,
            (
                "q",
                "filter_id",
                "save_coords",
                "show_unconnected",
                "show_cables",
                "show_circuit",
                "show_logical_connections",
                "show_single_cable_logical_conns",
                "show_power",
                "show_wireless",
            ),
        ),
        (
            None,
            (
                "tenant_group_id",
                "tenant_id",
            ),
        ),
        (None, ("region_id", "site_id", "location_id", "rack_id")),
        (
            None,
            (
                "device_role_id",
                "id",
                "status",
            ),
        ),
        (None, ("tag",)),
    )

    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(), required=False, label=_("Region")
    )
    device_role_id = DynamicModelMultipleChoiceField(
        queryset=DeviceRole.objects.all(), required=False, label=_("Device Role")
    )
    id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label=_("Device"),
        query_params={
            "location_id": "$location_id",
            "region_id": "$region_id",
            "site_id": "$site_id",
            "role_id": "$device_role_id",
        },
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            "region_id": "$region_id",
        },
        label=_("Site"),
    )
    location_id = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        query_params={
            "region_id": "$region_id",
            "site_id": "$site_id",
        },
        label=_("Location"),
    )
    rack_id = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        query_params={
            "region_id": "$region_id",
            "site_id": "$site_id",
            "location_id": "$location_id",
        },
        label=_("Rack"),
    )
    status = MultipleChoiceField(
        choices=DeviceStatusChoices, required=False, label=_("Device Status")
    )
    tag = TagFilterField(model)

    # options
    save_coords = forms.BooleanField(
        label=_("Save Coordinates"),
        required=False,
        disabled=(not settings.PLUGINS_CONFIG["netbox_topology_views"]["allow_coordinates_saving"] or settings.PLUGINS_CONFIG["netbox_topology_views"]["always_save_coordinates"]),
        initial=(settings.PLUGINS_CONFIG["netbox_topology_views"]["always_save_coordinates"])
    )
    show_unconnected = forms.BooleanField(
        label=_("Show Unconnected"), required=False, initial=False
    )
    show_logical_connections = forms.BooleanField(
        label =_("Show Logical Connections"), required=False, initial=False
    )
    show_single_cable_logical_conns = forms.BooleanField(
        label =_("Show redundant Cable and Locigal Connection"), required=False, initial=False
    )
    show_cables = forms.BooleanField(
        label =_("Show Cables"), required=False, initial=False
    )
    show_wireless = forms.BooleanField(
        label =_("Show Wireless Links"), required=False, initial=False
    )
    show_circuit = forms.BooleanField(
        label=_("Show Circuit Terminations"), required=False, initial=False
    )
    show_power = forms.BooleanField(
        label=_("Show Power Feeds"), required=False, initial=False
    )

class IndividualOptionsForm(NetBoxModelForm):
    fieldsets = (
        (
            None,
            (
                "user_id",
                "ignore_cable_type",
                "preselected_device_roles",
                "preselected_tags",
                "show_unconnected",
                "show_cables",
                "show_circuit",
                "show_logical_connections",
                "show_single_cable_logical_conns",
                "show_power",
                "show_wireless",
                "draw_default_layout",
            ),
        ),
    )

    user_id = forms.CharField(widget=forms.HiddenInput())

    ignore_cable_type = MultipleChoiceField(
        label=_("Ignore Termination Types"), 
        required=False, 
        choices=IndividualOptions.CHOICES,
        help_text=_("Choose Termination Types that you want to be ignored. "
            "If any ignored Termination Type is part of a connection, the "
            "cable is not displayed.")
    )
    preselected_device_roles = DynamicModelMultipleChoiceField(
        label=_("Preselected Device Role"),
        queryset=DeviceRole.objects.all(),
        required=False,
        help_text=_("Select Device Roles that you want to have "
            "preselected in the filter tab.")
    )
    preselected_tags = forms.ModelMultipleChoiceField(
        label=_("Preselected Tags"),
        queryset=Device.tags.all(),
        required=False,
        help_text=_("Select Tags that you want to have "
            "preselected in the filter tab.")
    )
    show_unconnected = forms.BooleanField(
        label=_("Show Unconnected"), 
        required=False, 
        initial=False,
        help_text=_("Draws devices that have no connections or for which no "
            "connection is displayed. This option depends on other parameters "
            "like 'Show Cables' and 'Show Logical Connections'.")
    )
    show_cables = forms.BooleanField(
        label =_("Show Cables"), 
        required=False, 
        initial=False,
        help_text=_("Displays connections between interfaces that are connected "
            "with one or more cables. These connections are displayed as solid "
            "lines in the color of the cable.")
    )
    show_logical_connections = forms.BooleanField(
        label =_("Show Logical Connections"), 
        required=False, 
        initial=False,
        help_text=_("Displays connections between devices that are not "
            "directly connected (e.g. via patch panels). These connections "
            "are displayed as yellow dotted lines.")
    )
    show_single_cable_logical_conns = forms.BooleanField(
        label = ("Show redundant Cable and Locigal Connection"),
        required = False,
        initial=False,
        help_text=_("Shows a logical connection (in addition to a cable), "
            "even if a cable is directly connected. Leaving this option "
            "disabled prevents that redundant display. This option only "
            "has an effect if 'Show Logical Connections' is activated.")
    )
    show_circuit = forms.BooleanField(
        label=_("Show Circuit Terminations"), 
        required=False, 
        initial=False,
        help_text=_("Displays connections between circuit terminations. "
            "These connections are displayed as blue dashed lines.")
    )
    show_power = forms.BooleanField(
        label=_("Show Power Feeds"), 
        required=False, 
        initial=False,
        help_text=_("Displays connections between power outlets and power "
            "ports. These connections are displayed as solid lines in the "
            "color of the cable. This option depends on 'Show Cables'.")
    )
    show_wireless = forms.BooleanField(
        label =_("Show Wireless Links"), 
        required=False, 
        initial=False,
        help_text=_("Displays wireless connections. These connections are "
            "displayed as blue dotted lines.")
    )
    draw_default_layout = forms.BooleanField(
        label = ("Draw Default Layout"),
        required=False,
        initial=False,
        help_text=_("Enable this option if you want to draw the topology on "
            "the initial load (when you go to the topology plugin page).")
    )

    class Meta:
        model = IndividualOptions
        fields = [
            'user_id', 'ignore_cable_type', 'preselected_device_roles', 'preselected_tags', 'show_unconnected', 'show_cables', 'show_logical_connections', 'show_single_cable_logical_conns', 'show_circuit', 'show_power', 'show_wireless', 'draw_default_layout'
        ]