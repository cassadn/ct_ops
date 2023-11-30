import boto3
import pandas as pd
import io

class WonderAWS:
    def __init__(self, service):
        self.session = boto3.Session(profile_name='default')
        self.service = service
    
        
class AWSClientSession(WonderAWS):
    def __init__(self, service):
        super().__init__(service)

    def get_session(self):
        client = self.session.client(service)

    # def 

    
class AWSResourceSession(WonderAWS):
    def __init__(self, service):
        super().__init__(service)
        self.resource = self.session.resource(service)
    
    def s3_parquet_to_df(self, bucket, prefix):
        self.bucket = bucket
        self.prefix = prefix
        bucketobj = self.s3_get_bucketobj()
        prefix_objs = self.s3_get_objects()
        out_df = pd.DataFrame()
        
        for obj in prefix_objs:
            body = obj.get()['Body'].read()
            pq_file = io.BytesIO(body)
            tmp_df = pd.read_parquet(pq_file)
            out_df = pd.concat([out_df, tmp_df])

        return out_df
    
    def s3_get_bucketobj(self):
        self.bucketobj = self.resource.Bucket(self.bucket)

        return self.bucketobj
    
    
    def s3_get_objects(self):
        prefix_objs = self.bucketobj.objects.filter(Prefix=self.prefix)
        
        return prefix_objs


    def read_files_to_df(s3_resource, bucket, prefix):
        prefix_objs = bucket.objects.filter(Prefix=prefix)
        out_df = pd.DataFrame()
        for obj in prefix_objs:
            body = obj.get()['Body'].read()
            pq_file = io.BytesIO(body)
            tmp_df = pd.read_parquet(pq_file)
            out_df = pd.concat([out_df, tmp_df])
    
        return out_df
