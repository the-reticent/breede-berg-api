from rest_framework import serializers
from .models import Organisation, OrganisationMembership
    
class OrganisationSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    sites_remaining = serializers.SerializerMethodField()
    users_remaining = serializers.SerializerMethodField()
    plan_limits = serializers.SerializerMethodField()

    class Meta:
        model = Organisation
        fields = '__all__'

    def get_member_count(self, obj):
        return obj.memberships.count()

    def get_sites_remaining(self, obj):
        return obj.sites_remaining()

    def get_users_remaining(self, obj):
        return obj.users_remaining()

    def get_plan_limits(self, obj):
        return obj.get_limits()


class OrganisationMembershipSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    organisation_name = serializers.CharField(source='organisation.name', read_only=True)

    class Meta:
        model = OrganisationMembership
        fields = '__all__'