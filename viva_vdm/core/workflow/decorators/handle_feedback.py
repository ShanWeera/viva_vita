import functools

from viva_vdm.core.models import JobDBModel
from viva_vdm.core.models.models import JobStatuses, LoggerFlags, LoggerMessageMap


def handle_feedback(context: str):
    def _(fn):
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            try:
                JobDBModel.objects.update_log(
                    instance=self.job_instance,
                    context=context,
                    flag=LoggerFlags.info,
                    msg=LoggerMessageMap.running[context],
                )

                fn(self, *args, **kwargs)

                JobDBModel.objects.update_log(
                    instance=self.job_instance,
                    context=context,
                    flag=LoggerFlags.info,
                    msg=LoggerMessageMap.completed[context],
                )
            except Exception as ex:
                JobDBModel.objects.update_log(
                    instance=self.job_instance,
                    context=context,
                    flag=LoggerFlags.error,
                    msg=LoggerMessageMap.error[context],
                )
                JobDBModel.objects.update_status(instance=self.job_instance, status=JobStatuses.error)

                raise ex

        return wrapper

    return _
