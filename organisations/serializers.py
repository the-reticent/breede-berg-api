from rest_framework import serializers
from .models import Organisation, OrganisationMembership


class OrganisationSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Organisation
        fields = '__all__'

    def get_member_count(self, obj):
        return obj.memberships.count()


class OrganisationMembershipSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    organisation_name = serializers.CharField(source='organisation.name', read_only=True)

    class Meta:
        model = OrganisationMembership
        fields = '__all__'