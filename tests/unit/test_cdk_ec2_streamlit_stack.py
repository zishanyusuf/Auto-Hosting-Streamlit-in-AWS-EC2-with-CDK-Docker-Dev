import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_ec2_streamlit.cdk_ec2_streamlit_stack import CdkEc2StreamlitStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_ec2_streamlit/cdk_ec2_streamlit_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkEc2StreamlitStack(app, "cdk-ec2-streamlit")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
