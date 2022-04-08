# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging
import click
import json

import grpc
from gRPC import hpo_pb2_grpc, hpo_pb2
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import Parse, ParseDict


@click.group()
def main():
    """A HPO command line tool to allow interaction with HPO service"""
    logging.basicConfig()
    pass

@main.command()
def count():
    """Return a count of experiments currently running"""
    empty = hpo_pb2.NumberExperimentsReply()
    fun = lambda stub : stub.NumberExperiments(empty)
    response = run(fun)
    click.echo(" Number of running experiments: {}".format(response.count))

@main.command()
def list():
    """List names of all experiments currently running"""
    empty = hpo_pb2.NumberExperimentsReply()
    fun = lambda stub : stub.ExperimentsList(empty)
    experiments: hpo_pb2.ExperimentsListReply = run(fun)
    print("Running Experiments:")
    for experiment in experiments.experiment:
        click.echo(" %s" % experiment)

@main.command()
@click.option("--name", prompt=" Experiment name", type=str)
def show(name):
    """Show details of running experiment"""
    expr: hpo_pb2.ExperimentNameParams = hpo_pb2.ExperimentNameParams()
    expr.experiment_name = name
    fun = lambda stub : stub.GetExperimentDetails(expr)
    experiment: hpo_pb2.ExperimentDetails = run(fun)
    json_obj = MessageToJson(experiment)
    click.echo("Experiment Details:")
    click.echo(json_obj)

@main.command()
@click.option("--file", prompt=" Experiment configuration file path", type=str)
def new(file):
    """Create a new experiment"""
    # TODO: validate file path
    with open(file, 'r') as json_file:
        data = json.load(json_file)
        # data = file.read().replace('\n', '')
        message: hpo_pb2.ExperimentDetails = ParseDict(data, hpo_pb2.ExperimentDetails())
    click.echo(" Adding new experiment: {}".format(message.experiment_name))
    fun = lambda stub : stub.NewExperiment(message)
    response: hpo_pb2.NewExperimentsReply = run(fun)
    click.echo("Trial Number: {}".format(response.trial_number))

@main.command()
@click.option("--name", prompt=" Experiment name", type=str)
@click.option("--trial", prompt=" Trial number", type=int)
def config(name, trial):
    """Obtain a configuration set for a particular experiment trail"""
    expr: hpo_pb2.ExperimentTrial = hpo_pb2.ExperimentTrial()
    expr.experiment_name = name
    expr.trial = trial
    fun = lambda stub : stub.GetTrialConfig(expr)
    trial_config: hpo_pb2.TrialConfig = run(fun)
    json_obj = MessageToJson(trial_config)
    click.echo("Trial Config:")
    click.echo(json_obj)

@main.command()
@click.option("--name", prompt=" Enter name", type=str)
@click.option("--trial", prompt=" Enter trial number", type=int)
@click.option("--result", prompt=" Enter trial result", type=str)
@click.option("--value_type", prompt=" Enter result type", type=str)
@click.option("--value", prompt=" Enter result value", type=float)
def result(name, trial, result, value_type, value):
    """Update results for a particular experiment trail"""
    trialResult: hpo_pb2.ExperimentTrialResult = hpo_pb2.ExperimentTrialResult()
    trialResult.experiment_id = name
    trialResult.trial = trial
    trialResult.result = hpo_pb2._EXPERIMENTTRIALRESULT_RESULT.values_by_name[result].number
    trialResult.value_type = value_type
    trialResult.value = value
    fun = lambda stub : stub.UpdateTrialResult(trialResult)
    hpo_pb2.TrialConfig = run(fun)
    click.echo("Updated Trial Result")

@main.command()
@click.option("--name", prompt=" Enter name", type=str)
def next(name):
    """Generate next configuration set for running experiment"""
    experiment: hpo_pb2.ExperimentNameParams = hpo_pb2.ExperimentNameParams()
    experiment.experiment_name = name
    fun = lambda stub : stub.GenerateNextConfig(experiment)
    reply: hpo_pb2.NewExperimentsReply = run(fun)
    click.echo("Next Trial: {}".format(reply.trial_number))

def run(func):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = hpo_pb2_grpc.HpoServiceStub(channel)
        return func(stub)

def NewExperiment(stub, **args):
    empty = hpo_pb2.NumberExperimentsReply()
    response = stub.NumberExperiments(empty)
    print("HpoService client received: %s" % response.count)


if __name__ == "__main__":
    main()