import logging.handlers
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stripeTestTask.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    rotating_handler = logging.handlers.RotatingFileHandler('logs/stripe_app.log',
                                                            backupCount=5,
                                                            maxBytes=512 * 1024)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(lineno)d - %(message)s')
    rotating_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(lineno)d - %(message)s')
    logging.getLogger('').addHandler(rotating_handler)

    main()
