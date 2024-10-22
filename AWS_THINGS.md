## Cognito user pool
- https://us-east-2.console.aws.amazon.com/cognito/v2/idp/user-pools/us-east-2_P2utY5LE6/users?region=us-east-2

## IAM Permissions
- https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-2#/users/details/water-treatment-dev-user?section=permissions


## s3
- Set up a bucket
  - Almost ALL default settings
  - GET, HEAD is fine if all you're doing is serving files
  - Domain config might change for custom domain
- Set up cloudfront
  - Cloudfront is useful because it can be set up for URL signing with long-term access
  - Also, it's a CDN, so it will reduce latency with image sourcing
- Set up IAM users
  - One for dev and one for prod
  - Give them permissions