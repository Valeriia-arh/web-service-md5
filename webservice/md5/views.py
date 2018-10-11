from rest_framework.response import Response
from celery.result import AsyncResult
from celery import uuid

@api_view(['GET'])
def request_get(request, task_uuid):
    """
    This function takes name of text in url.
    :return: 200 status code if everything is fine, otherwise 400
    if task wasn't completed return 409
    """
    result = AsyncResult(task_uuid)
    if result.state == 'FAILURE':
        try:
            res = result.get()
        except Exception as exc:
            answer = {'state' : result.state, 'caused by' : str(exc)}
        return Response(answer, status=status.HTTP_400_BAD_REQUEST)
    elif result.state == 'SUCCESS':
        try:
            answer = {'state' : result.state}
        except Exception:
            return Response(data='Something went wrong!')
        return Response(answer, status=status.HTTP_200_OK)
    else:
        answer = {'state' : result.state}
        return Response(answer, data="Task wasn't completed", status=status.HTTP_409_CONFLICT)


@api_view(['POST'])
def request_post(request):
    task_ud = uuid()



    def post(self, request, pipeline_id):
        pipeline = self.get_pipeline(self.request, pipeline_id)
        if pipeline is None:
            return response.Response(data={}, status=status.HTTP_404_NOT_FOUND)
        elif pipeline.status in pipeline.waiting_statuses() + pipeline.running_statuses():
            self.pipeline_service.terminate_pipeline(pipeline_id)
            return response.Response(data={}, status=status.HTTP_202_ACCEPTED)
        else:
            return response.Response(
                data={'error': 'pipeline {} has status {}'.format(pipeline_id, pipeline['status'])},
                status=status.HTTP_409_CONFLICT
            )

from django.contrib.auth.models import User, Group
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from quickstart.serializers import UserSerializer, GroupSerializer





from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from celery.result import AsyncResult
from celery import uuid, chain

from api import tasks
import logging

logger = logging.getLogger(__name__)


class HashViewSet(viewsets.ViewSet):
    """
    API endpoint that allow to start document hashing or to get result from it.
    """
    def retrieve(self, request, pk=None):
        res = AsyncResult(pk)
        if res.state == 'SUCCESS':
            content = {'state': res.state, 'result': res.get()}
            return Response(content, status=status.HTTP_200_OK)
        elif res.state == 'FAILURE':
            try:
                res.get()
            except Exception as e:
                content = {'state': res.state, 'cause': str(e)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {'state': res.state}
            return Response(content, status=status.HTTP_409_CONFLICT)

    def create(self, request):
        if 'url' in request.POST:
            url = request.POST['url']
            logger.debug(url)
            filename = uuid()

            ch = chain(tasks.download.s(url, filename), tasks.hash.s())
            async = ch.apply_async()
            logger.debug("Chain to export: {}".format(async))
            content = {'GUID': async.id}
            return Response(content, status=status.HTTP_202_ACCEPTED)
        else:
return Response(status=status.HTTP_400_BAD_REQUEST)