# This file is part flower module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import json
import pytz
from trytond.model import ModelView, fields
from trytond.pool import Pool
from trytond.rpc import RPC
from trytond.transaction import Transaction
from .utils import *

__all__ = ['FlowerWorkers', 'FlowerTasks']

_ICONS = {
    'SUCCESS': 'flower-success',
    'ERROR': 'flower-error',
}


class FlowerWorkers(ModelView):
    "Flower Workers"
    __name__ = 'flower.workers'

    name = fields.Char('Name')
    stats = fields.Text('Stats')
    conf = fields.Text('Configuration')

    @classmethod
    def __setup__(cls):
        super(FlowerWorkers, cls).__setup__()
        cls.__rpc__.update({
            'search': RPC(),
            'read': RPC(),
        })

    @classmethod
    def search(cls, domain, offset=0, limit=None, order=None, count=False,
            query=False):
        """Flower Search API workers
        Flower API query parameters:
        refresh: run inspect to get updated list of workers
        workername: get info for workername
        status: only get worker status info
        """
        data = flower_response(WORKERS_API)

        res = []
        for k, _ in data.items():
            res.append(k)

        return res

    @classmethod
    def read(cls, ids, fields_names=None):
        'Flower Read API workers'
        data = flower_response(WORKERS_API)

        # active_queues
        # timestamp
        # registered
        # stats
        # conf

        res = []
        for k, v in data.items():
            v2 = v.copy()
            v2['id'] = k
            v2['name'] = k
            v2['stats'] = json.dumps(v.get('stats'))
            v2['conf'] = json.dumps(v.get('conf'))
            res.append(v2)
        return res


class FlowerTasks(ModelView):
    "Flower Tasks"
    __name__ = 'flower.tasks'
    _rec_name = 'uuid'

    uuid = fields.Char('UUID')
    worker = fields.Char('Worker')
    name = fields.Char('Name')
    state = fields.Char('State')
    args = fields.Char('args')
    kwargs = fields.Char('kwargs')
    result = fields.Char('Result')
    received = fields.DateTime('Received')
    started = fields.DateTime('Started')
    succeeded = fields.DateTime('Succeeded')
    failed = fields.DateTime('Failed')
    retries = fields.Char('Retries')
    runtime = fields.Float('Runtime')
    # clock = fields.Char('Clock')
    traceback = fields.Text('Traceback')

    # Show the icon depending on the state
    state_icon = fields.Function(fields.Char('State Icon'),
        'get_state_icon')

    @classmethod
    def __setup__(cls):
        super(FlowerTasks, cls).__setup__()
        cls.__rpc__.update({
            'search': RPC(),
            'read': RPC(),
        })

    def get_state_icon(self, name):
        return _ICONS.get(self.state, '')

    @classmethod
    def search(cls, domain, offset=0, limit=None, order=None, count=False,
            query=False):
        """Flower Search API tasks
        Flower API query parameters:
        limit: maximum number of tasks
        workername: filter task by workername
        taskname: filter tasks by taskname
        statisinstance(e: filter tasks by state
        """
        # create new list with values from search toolbar and search domain
        conds = []
        for d in domain:
            if isinstance(d[0], list):
                for c in d:
                    if isinstance(c, list):
                        conds.append(c)
            else:
                conds.append(d)

        request_params = []
        for d in conds:
            if not isinstance(d, list):
                continue

            if d and d[0] == 'name':
                request_params.append('taskname=%s' % search_not_like(d[2]))
            if d and d[0] == 'uuid':
                request_params.append('task-id=%s' % search_not_like(d[2]))
            if d and d[0] == 'received':
                if d[1] == '<=':
                    request_params.append('received-end=%s' % flower_json_hour(d[2]))
                else:
                    request_params.append('received-start=%s' % flower_json_hour(d[2]))
            if d and d[0] == 'state':
                request_params.append('state=%s' % search_not_like(d[2]))

        if request_params:
            uri_search = '{}/tasks?{}'.format(API_URI, '&'.join(request_params))
        else:
            uri_search = TASKS_API

        data = flower_response(uri_search)

        res = []
        if data:
            for k, _ in data.items():
                res.append(k)

        return res

    @classmethod
    def read(cls, ids, fields_names=None):
        'Flower Read API task'
        pool = Pool()
        Company = pool.get('company.company')

        timezone = None
        company_id = Transaction().context.get('company')
        if timezone is None and company_id:
            company = Company(company_id)
            if company.timezone:
                timezone = pytz.timezone(company.timezone)

        if len(ids) > 1:
            data = flower_response(TASKS_API) # return {uuid: {}}
            if not data:
                return
        else:
            uuid = ids[0]
            api = '{}/info/{}'.format(TASK_API, uuid)
            val = flower_response(api) # return {}
            if not val:
                return
            data = {uuid: val}

        res = []
        for k, v in data.items():
            v2 = v.copy()
            # copy uuid or task-id to id
            v2['id'] = v['uuid'] if v.get('uuid') else v['task-id']
            v2['uuid'] = v['uuid'] if v.get('uuid') else v['task-id']
            v2['received'] = flower_hour(v['received'], timezone) \
                    if v.get('received') else None
            v2['started'] = flower_hour(v['started'], timezone) \
                    if v.get('started') else None
            v2['succeeded'] = flower_hour(v['succeeded'], timezone) \
                    if v.get('succeeded') else None
            v2['failed'] = flower_hour(v['failed'], timezone) \
                    if v.get('failed') else None
            res.append(v2)

        return res
