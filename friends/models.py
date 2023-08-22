from django.db import models
from products.models import Reservation
from users.models import User
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_friend_list(sender, instance, created, **kwargs):
    if created:
        FriendList.objects.create(user=instance)


class FriendList(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(User, blank=True, related_name="friends")

    def __str__(self):
        return self.user.surname

    def add_friend(self, account):
        """
        Add a new friend
        """
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self, account):
        """
        Remove a friend
        """
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()

    def unfriend(self, removee):
        """
        Initiate the action of unfriend someone
        """
        remover_friends_list = self
        remover_friends_list.remove_friend(removee)

        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(remover_friends_list.user)

    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
    """
    A friend request consists of two main parts:
        1: SENDER - person sending the friend request
        2: RECEIVER - person receiving the friend request
    """

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.surname

    def accept(self):
        """
        Accept a friend request.
        Update both SENDER and RECEIVER friend lists.
        """
        receiver_friend_list, _ = FriendList.objects.get_or_create(user=self.receiver)
        receiver_friend_list.add_friend(self.sender)

        sender_friend_list, _ = FriendList.objects.get_or_create(user=self.sender)
        sender_friend_list.add_friend(self.receiver)

        self.delete()

    def decline(self):
        """
        Decline a friend request.
        """
        self.delete()

    def cancel(self):
        """
        Cancel a friend request.
        This is only different with respect to "declining" through the notification that is generated.
        """
        self.delete()


class Notification(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True, blank=True, )
    friend_request = models.ForeignKey(FriendRequest, on_delete=models.CASCADE, null=True, blank=True, )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.user} - {self.content}"
