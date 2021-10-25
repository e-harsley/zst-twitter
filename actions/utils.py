import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from actions.models import Actions


def create_action(user, verb, target=None):
    # check for any similar action made in the last minute
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    print("dkdkddkdkkd",user.id, verb, last_minute)
    similar_actions = Actions.objects.filter(user_id=user.id,
                                       verb= verb,
                                       created__gte=last_minute)
    print(similar_actions, target)
    if target:
        target_ct = ContentType.objects.get_for_model(target)

        print('ddddd',target_ct)
        similar_actions = similar_actions.filter(target_ct=target_ct,
                                                 target_id=target.id)
    if not similar_actions:
        print("i am suooise to be heree")
        # no existing actions found
        action = Actions(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
