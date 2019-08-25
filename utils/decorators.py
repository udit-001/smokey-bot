from utils.timer import feedback_msg
import config


def feedback_timer(input_function):
    def wrapper(bot, update, user_data, job_queue):
        input_function(bot, update, user_data, job_queue)
        for item in job_queue.queue.queue:
            item[1].schedule_removal()
        job_queue.run_once(feedback_msg, config.timer_duration, context=update)
    return wrapper


def feedback_timer_search(input_function):
    def wrapper(bot, update, args, user_data, job_queue):
        input_function(bot, update, args, user_data, job_queue)
        for item in job_queue.queue.queue:
            item[1].schedule_removal()
        job_queue.run_once(feedback_msg, config.timer_duration, context=update)
    return wrapper
