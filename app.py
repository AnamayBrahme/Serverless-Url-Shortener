#!/usr/bin/env python3

import aws_cdk as cdk

from sample_app1.sample_app1_stack import SampleApp1Stack


app = cdk.App()
SampleApp1Stack(app, "SampleApp1Stack")

app.synth()
