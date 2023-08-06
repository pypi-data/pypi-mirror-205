import os
import uuid
from typing import Optional

import click
from click import style

from dnastack.alpha.cli.workbench.utils import _get_ewes_client
from dnastack.alpha.client.ewes.models import ExtendedRunListOptions, ExtendedRunRequest, BatchRunRequest, \
    MinimalExtendedRunWithOutputs, MinimalExtendedRunWithInputs
from dnastack.alpha.client.ewes.models import LogType, Log
from dnastack.cli.helpers.command.decorator import command
from dnastack.cli.helpers.command.spec import ArgumentSpec
from dnastack.cli.helpers.exporter import to_json, normalize
from dnastack.cli.helpers.iterator_printer import show_iterator, OutputFormat
from dnastack.common.json_argument_parser import *
from dnastack.http.session import ClientError


@click.group('runs')
def alpha_runs_command_group():
    """ EWES Runs API """

@command(alpha_runs_command_group,
         'list',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='max_results',
                 arg_names=['--max-results'],
                 help='An optional flag to limit the total number of results.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='page',
                 arg_names=['--page'],
                 help='An optional flag to set the offset page number. '
                      'This allows for jumping into an arbitrary page of results. Zero-based.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='page_size',
                 arg_names=['--page-size'],
                 help='An optional flag to set the page size returned by the server.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='order',
                 arg_names=['--order'],
                 help='An optional flag to define the ordering of the results. '
                      'The value should return to the attribute name to order the results by. '
                      'By default, results are returned in descending order. '
                      'To change the direction of ordering include the "ASC" or "DESC" string after the column. '
                      'e.g.: --O "end_time", --O "end_time ASC"',

                 as_option=True
             ),
             ArgumentSpec(
                 name='states',
                 arg_names=['--state'],
                 help='An optional flag to filter the results by their state. '
                      'This flag can be defined multiple times, with the result being any of the states.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='submitted_since',
                 arg_names=['--submitted-since'],
                 help='An optional flag to filter the results with their start_time '
                      'greater or equal to the since timestamp. '
                      'The timestamp can be in iso date, or datetime format. '
                      'e.g.: -f "2022-11-23", -f "2022-11-23T00:00:00.000Z"',
                 as_option=True
             ),
             ArgumentSpec(
                 name='submitted_until',
                 arg_names=['--submitted-until'],
                 help='An optional flag to filter the results with their start_time '
                      'strictly less than the since timestamp. '
                      'The timestamp can be in iso date, or datetime format. '
                      'e.g.: -t "2022-11-23", -t "2022-11-23T23:59:59.999Z"',
                 as_option=True
             ),
             ArgumentSpec(
                 name='engine',
                 arg_names=['--engine'],
                 help='An optional flag to filter the results to runs with the given engine ID',
                 as_option=True
             ),
             ArgumentSpec(
                 name='search',
                 arg_names=['--search'],
                 help='An optional flag to perform a full text search across various fields using the search value',
                 as_option=True
             ),
         ])
def list_runs(context: Optional[str],
              endpoint_id: Optional[str],
              namespace: Optional[str],
              max_results: Optional[int],
              page: Optional[int],
              page_size: Optional[int],
              order: Optional[str],
              submitted_since: Optional[str],
              submitted_until: Optional[str],
              engine: Optional[str],
              search: Optional[str],
              states: List[str] = None):
    """ List workflow runs """

    def parse_to_datetime_iso_format(date: str, start_of_day: bool = False, end_of_day: bool = False) -> str:
        if (date is not None) and ("T" not in date):
            if start_of_day:
                return f'{date}T00:00:00.000Z'
            if end_of_day:
                return f'{date}T23:59:59.999Z'
        return date

    order_direction = None
    if order:
        order_and_direction = order.split()
        if len(order_and_direction) > 1:
            order = order_and_direction[0]
            order_direction = order_and_direction[1]

    client = _get_ewes_client(context_name=context, endpoint_id=endpoint_id, namespace=namespace)
    list_options: ExtendedRunListOptions = ExtendedRunListOptions(
        page=page,
        page_size=page_size,
        order=order,
        direction=order_direction,
        state=states,
        since=parse_to_datetime_iso_format(date=submitted_since, start_of_day=True),
        until=parse_to_datetime_iso_format(date=submitted_until, end_of_day=True),
        engineId=engine,
        search=search,
    )
    show_iterator(output_format=OutputFormat.JSON, iterator=client.list_runs(list_options, max_results))


@command(alpha_runs_command_group,
         'describe',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='status',
                 arg_names=['--status'],
                 help='Output a minimal response, only showing the status id, current state, start and stop times.',
                 as_option=True,
                 default=False
             ),
             ArgumentSpec(
                 name='inputs',
                 arg_names=['--inputs'],
                 help='Display only the run\'s inputs as json.',
                 as_option=True,
                 default=False
             ),
             ArgumentSpec(
                 name='outputs',
                 arg_names=['--outputs'],
                 help='Display only the run\'s outputs as json.',
                 as_option=True,
                 default=False
             ),
             ArgumentSpec(
                 name='include_tasks',
                 arg_names=['--include-tasks'],
                 help='Include the tasks in the output.',
                 as_option=True,
                 default=False
             ),
         ])
def describe_runs(context: Optional[str],
                  endpoint_id: Optional[str],
                  namespace: Optional[str],
                  runs: List[str],
                  status: Optional[bool],
                  inputs: Optional[bool],
                  outputs: Optional[bool],
                  include_tasks: Optional[bool]):
    """ Describe workflow run """
    client = _get_ewes_client(context_name=context, endpoint_id=endpoint_id, namespace=namespace)
    if status:
        described_runs = [client.get_status(run_id=run) for run in runs]
    else:
        described_runs = [client.get_run(run_id=run, include_tasks=include_tasks) for run in runs]

        if inputs:
            described_runs = [MinimalExtendedRunWithInputs(
                run_id=described_run.run_id,
                inputs=described_run.request.workflow_params,
            ) for described_run in described_runs]
        elif outputs:
            described_runs = [MinimalExtendedRunWithOutputs(
                run_id=described_run.run_id,
                outputs=described_run.outputs
            ) for described_run in described_runs]
    click.echo(to_json(normalize(described_runs)))


@command(alpha_runs_command_group,
         'cancel',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
         ])
def cancel_runs(context: Optional[str],
                endpoint_id: Optional[str],
                namespace: Optional[str],
                runs: List[str] = None):
    """Cancel one or more workflow runs"""
    client = _get_ewes_client(context_name=context, endpoint_id=endpoint_id, namespace=namespace)
    result = client.cancel_runs(runs)
    click.echo(to_json(normalize(result)))


@command(alpha_runs_command_group,
         'delete',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='force',
                 arg_names=['--force'],
                 help='Force the deletion without prompting for confirmation.',
                 as_option=True,
                 default=False
             )
         ])
def delete_runs(context: Optional[str],
                endpoint_id: Optional[str],
                namespace: Optional[str],
                force: Optional[bool] = False,
                runs: List[str] = None):
    """Delete one or more workflow runs"""
    client = _get_ewes_client(context_name=context, endpoint_id=endpoint_id, namespace=namespace)
    if not force and not click.confirm('Do you want to proceed?'):
        return
    result = client.delete_runs(runs)
    click.echo(to_json(normalize(result)))


@command(alpha_runs_command_group,
         'logs',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='log_type',
                 arg_names=['--log-type'],
                 help='Print only stderr or stdout to the current console.',
                 as_option=True,
                 default=LogType.stdout
             ),
             ArgumentSpec(
                 name='task_name',
                 arg_names=['--task-name'],
                 help='Retrieve logs associated with the given task in the run.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='max_bytes',
                 arg_names=['--max-bytes'],
                 help='Limit number of bytes to retrieve from the log stream.',
                 as_option=True,
             ),
             ArgumentSpec(
                 name='output',
                 arg_names=['--output'],
                 help="Save the output to the defined path, if it does not exist",
                 as_option=True
             )
         ])
def get_run_logs(context: Optional[str],
                 endpoint_id: Optional[str],
                 namespace: Optional[str],
                 run_id_or_log_url: str,
                 output: Optional[str],
                 log_type: Optional[LogType] = LogType.stdout,
                 task_name: Optional[str] = None,
                 max_bytes: Optional[int] = None):
    """Get logs of a single workflow run"""

    def get_writer(output_path: Optional[str]):
        if not output_path:
            return click.echo
        if os.path.exists(output_path):
            click.echo(style(f"{output_path} already exists, command will not overwrite", fg="red"), color=True)
            exit(0)

        output_file = open(output_path, "w")

        def write(binary_content: bytes):
            output_file.write(binary_content.decode("utf-8"))

        return write

    def is_valid_uuid(val: str):
        try:
            uuid.UUID(val, version=4)
            return True
        except ValueError:
            return False

    def print_logs_by_url(log_url: str, writer):
        for logs_chunk in client.stream_run_logs(log_url=log_url, max_bytes=max_bytes):
            if logs_chunk:
                writer(logs_chunk)

    def print_logs(log: Log, writer):
        if log:
            print_logs_by_url(log.stderr if log_type == LogType.stderr else log.stdout, writer=writer)

    client = _get_ewes_client(context_name=context, endpoint_id=endpoint_id, namespace=namespace)
    output_writer = get_writer(output)

    if not is_valid_uuid(run_id_or_log_url):
        print_logs_by_url(log_url=run_id_or_log_url, writer=output_writer)
        return

    described_run = client.get_run(run_id=run_id_or_log_url, include_tasks=True)
    if not task_name:
        try:
            print_logs(log=described_run.run_log, writer=output_writer)
        except ClientError as e:
            if e.response.status_code == 404:
                return
    else:
        if described_run.task_logs:
            task = next(
                (run_task for run_task in described_run.task_logs if
                 run_task.name.lower() == task_name.strip().lower()),
                None
            )
            if task:
                print_logs(log=task, writer=output_writer)


@command(alpha_runs_command_group,
         'submit',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='workflow_url',
                 arg_names=['--url'],
                 help='The URL to the workflow file (*.wdl). Only urls from workflow-service are '
                      'currently supported.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='engine_id',
                 arg_names=['--engine'],
                 help='Use the given engine id for execution of runs. If this value is not defined then it is assumed '
                      'that the default engine will be used.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='default_workflow_engine_parameters',
                 arg_names=['--engine-params'],
                 help='Set the global engine parameters for all runs that are to be submitted. '
                      'Engine params can be specified as a KV pair, inlined JSON, or as a json file preceded by the "@"'
                      'symbol.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='default_workflow_params',
                 arg_names=['--default-params'],
                 help='Specify the global default inputs as a json file or as inlined json to use when submitting '
                      'multiple runs. Default inputs have the lowest level of precedence and will be overridden '
                      'by any run input or override.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='workflow_params',
                 arg_names=['--workflow-params'],
                 help='Optional flag to specify the workflow params for a given run. The workflow params can be any'
                      'JSON-like value, such as inline JSON, command separated key value pairs or a json file referenced'
                      'preceded by the "@" symbol. This field may be repeated, with each repetition specifying '
                      'a separate run request that will be submitted.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='tags',
                 arg_names=['--tags'],
                 help='Set the global tags for all runs that are to be submitted. '
                      'Tags can be any JSON-like value, such as inline JSON, command separated key value pairs or'
                      'a json file referenced preceded by the "@" symbol.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='run_request',
                 arg_names=['--run-request'],
                 help='Supply a single run configuration in the form of a JSON run request. Values can be defined '
                      'through key value inputs, a json file or inlined json. This approach allows the user to have '
                      'more control over not just the inputs but the engine params and tags that are submitted as part '
                      'of a single run. A single “request” flag will result in a single run '
                      '(similar to the –inputs flag). The value may be repeated multiple times with each repetition '
                      'corresponding to a unique run.',
                 as_option=True
             )
         ])
def submit_batch(context: Optional[str],
                 endpoint_id: Optional[str],
                 namespace: Optional[str],
                 workflow_url: str,
                 engine_id: Optional[str],
                 default_workflow_engine_parameters: Optional[str],
                 default_workflow_params: Optional[str],
                 tags: Optional[str],
                 workflow_params: List[str] = None,
                 run_request: Optional[str] = None,
                 overrides: List[str] = None):
    """
    Submit one or more workflows for execution

    """

    ewes_client = _get_ewes_client(context_name=context, endpoint_id=endpoint_id, namespace=namespace)

    batch_request: BatchRunRequest = BatchRunRequest(
        workflow_url=workflow_url,
        workflow_type="WDL",
        engine_id=engine_id,
        default_workflow_engine_parameters=parse_argument(default_workflow_engine_parameters),
        default_workflow_params=parse_argument(default_workflow_params),
        default_tags=parse_argument(tags),
        run_requests=[run_request] if run_request else []
    )

    for workflow_param in workflow_params:
        run_request = ExtendedRunRequest(
            workflow_params=parse_argument(workflow_param)
        )
        batch_request.run_requests.append(run_request)

    override_data = parse_and_merge_arguments(overrides)
    if override_data:
        if not batch_request.default_workflow_params:
            batch_request.default_workflow_params = dict()
        merge(batch_request.default_workflow_params, override_data)

        for run_request in batch_request.run_requests:
            if not run_request.workflow_params:
                run_request.workflow_params = dict()
            merge(run_request.workflow_params, override_data)

    minimal_batch = ewes_client.submit_batch(batch_request)
    click.echo(to_json(normalize(minimal_batch)))
