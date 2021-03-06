from rest_framework import serializers
from Donate.models import Donate


class DonateSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_account')
    title = serializers.SerializerMethodField('get_post_title_from_post')

    def get_username_from_account(self, donate):
        username = donate.account_id_from.username
        return username

    def get_post_title_from_post(self, donate):
        pt = donate.post_id_to.title
        return pt

    class Meta:
        model = Donate
        fields = ['pk', 'account_id_from', 'username', 'post_id_to', 'title', 'amount', 'is_recurring', 'start_date', 'occurence', 'times_donated']

class DonateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donate
        fields = ['account_id_from', 'post_id_to', 'amount', 'is_recurring', 'start_date', 'occurence', 'times_donated']

    def save(self):
        try:
            account_id_from = self.validated_data['account_id_from']
            post_id_to = self.validated_data['post_id_to']
            amount = self.validated_data['amount']
            is_recurring = self.validated_data['is_recurring']
            
            if ('occurence' in self.validated_data):
                occurence = self.validated_data['occurence']
            else:
                occurence = None
            
        
            donate = Donate(
                account_id_from = account_id_from,
                post_id_to = post_id_to,
                amount = amount,
                is_recurring = is_recurring,
                occurence = occurence,
            )

            donate.save()
            return donate
            
        except KeyError:
            raise serializers.ValidationError({"response": "You must have an account_id_from, post_id_to, amount and is_recurring"}) 


class DonateUpdateSerializer(serializers.ModelSerializer):
     class Meta:
        model = Donate
        fields = ['amount', 'is_recurring', 'occurence']   

     def validate(self, donate):
        try:
            amount = donate['amount']
            occurence = donate['occurence']
            is_recurring = donate['is_recurring']
        except KeyError:
            pass
        return donate 