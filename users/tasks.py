import logging
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from recipe.models import RecipeLike

User = get_user_model()

logger = logging.getLogger(__name__)


@shared_task
def send_daily_likes_notification():
    """
    Send daily notifications to authors about likes received on their recipes.
    """
    try:
        logger.debug("Enter send_daily_likes_notification")
        today = timezone.now().date()
        users = User.objects.all()
        for user in users:
            # Get the likes received by the user's recipes today
            liked_recipes = RecipeLike.objects.filter(
                recipe__author=user, created__date=today
            )

            if liked_recipes.exists():
                subject = "Daily Likes Notification"
                context = {
                    "user": user,
                    "liked_recipes": liked_recipes,
                }
                email_html_message = render_to_string(
                    "users/daily_likes_notification.html", context
                )
                email_plaintext_message = render_to_string(
                    "users/daily_likes_notification.txt", context
                )
                msg = EmailMultiAlternatives(
                    # title:
                    subject,
                    # message:
                    email_plaintext_message,
                    # from:
                    "noreply@somehost.local",
                    # to:
                    [user.email],
                )
                msg.attach_alternative(email_html_message, "text/html")
                msg.send()
        logger.debug("Exit send_daily_likes_notification: success")
    except Exception as e:
        logger.error(f"Error send_daily_likes_notification: {e}", exc_info=True)
