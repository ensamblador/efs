import aws_cdk as core
import aws_cdk.assertions as assertions

from elastic_file_system.elastic_file_system_stack import ElasticFileSystemStack

# example tests. To run these tests, uncomment this file along with the example
# resource in elastic_file_system/elastic_file_system_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ElasticFileSystemStack(app, "elastic-file-system")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
