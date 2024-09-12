from dataclasses import dataclass


from worker.celery import send_email_task


@dataclass
class MailClient:

    def send_welcome_email(self, to: str) -> None:
        return send_email_task.delay(f"Welcome email", f'Welcome to our platform, {to}. Enjoy your stay!', to)
    
