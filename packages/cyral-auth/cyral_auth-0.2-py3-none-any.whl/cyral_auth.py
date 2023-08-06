def sso(username, token, user_account=None):
    from pyspark import SparkContext

    scs = SparkContext.getOrCreate()

    key = f"{username}:{token}"
    if user_account is not None:
        key = f"{key}:{user_account}"

    scs._jsc.hadoopConfiguration().set('fs.s3a.access.key', key)
    scs._jsc.hadoopConfiguration().set('fs.s3a.secret.key', 'none')
    scs._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider",
                                       "org.apache.hadoop.fs.s3a.BasicAWSCredentialsProvider")
