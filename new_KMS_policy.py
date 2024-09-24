import boto3
import json

client = boto3.client('kms')

# policy={
#   "Version": "2012-10-17",
#   "Id": "key-consolepolicy-3",
#   "Statement": [
#     {
#       "Sid": "Enable IAM User Permissions",
#       "Effect": "Allow",
#       "Principal": {
#         "AWS": "arn:aws:iam::523265914192:root"
#       },
#       "Action": "kms:*",
#       "Resource": "*"
#     },
#     {
#       "Sid": "Allow access for Key Administrators",
#       "Effect": "Allow",
#       "Principal": {
#         "AWS": "arn:aws:iam::523265914192:user/22676427@student.uwa.edu.au"
#       },
#       "Action": [
#         "kms:Create*",
#         "kms:Describe*",
#         "kms:Enable*",
#         "kms:List*",
#         "kms:Put*",
#         "kms:Update*",
#         "kms:Revoke*",
#         "kms:Disable*",
#         "kms:Get*",
#         "kms:Delete*",
#         "kms:TagResource",
#         "kms:UntagResource",
#         "kms:ScheduleKeyDeletion",
#         "kms:CancelKeyDeletion"
#       ],
#       "Resource": "*"
#     },
#     {
#       "Sid": "Allow use of the key",
#       "Effect": "Allow",
#       "Principal": {
#         "AWS": "arn:aws:iam::523265914192:user/22676427@student.uwa.edu.au"
#       },
#       "Action": [
#         "kms:Encrypt",
#         "kms:Decrypt",
#         "kms:ReEncrypt*",
#         "kms:GenerateDataKey*",
#         "kms:DescribeKey"
#       ],
#       "Resource": "*"
#     },
#     {
#       "Sid": "Allow attachment of persistent resources",
#       "Effect": "Allow",
#       "Principal": {
#         "AWS": "arn:aws:iam::523265914192:user/22676427@student.uwa.edu.au"
#       },
#       "Action": [
#         "kms:CreateGrant",
#         "kms:ListGrants",
#         "kms:RevokeGrant"
#       ],
#       "Resource": "*",
#       "Condition": {
#         "Bool": {
#           "kms:GrantIsForAWSResource": "true"
#         }
#       }
#     }
#   ]
# }

# client.put_key_policy(
#     KeyId='1dd28fd9-1beb-44ba-8998-8819ab4c33b4',
#     PolicyName='Create_KMS_Policy',
#     Policy=json.dumps(policy)
# )


response = client.get_key_policy(
    KeyId = 'ab447b7c-fc9a-40b0-a1eb-8956223ec0cd',
    PolicyName = 'default'
)

print(response)

