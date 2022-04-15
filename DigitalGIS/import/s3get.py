import os
import psycopg2, subprocess
import geopandas as gpd
from minio import Minio
from minio.error import S3Error
from urllib.request import urlopen
from sqlalchemy import create_engine

class DGSMinio(Minio):

    def define_bucket(self, bucket_name):
        # Define bucket
        found = self.bucket_exists(bucket_name)
        if not found:
            self.make_bucket(bucket_name)
        else:
            print(f"Bucket '{bucket_name}' already exists")

        self.bucket_name = bucket_name

    def get_from_url(self, url, object_name):

        if hasattr(self, 'bucket_name'):
            found = self.bucket_exists(self.bucket_name)
            if not found:
                raise AttributeError('Please, define bucket: obj.make_bucket()')
            pass
        else:
            raise AttributeError('Please, define bucket: obj.make_bucket()')

        try:
            self.stat_object(self.bucket_name, object_name)
        except Exception as e:
            self.put_object(
                self.bucket_name, object_name, urlopen(url), length=-1, part_size=500*1024*1024
            )
            print(
                f"'{url}' is successfully uploaded as object '{object_name}' to bucket '{self.bucket_name}'."
            )
            pass
        else:
            print(f"Object {object_name} already exists in the bucket {self.bucket_name}")


class DGSMasks(object):


    conn_str = "postgresql://postgres:rbH%6lsr@digitalgis_db_1:5432/digitalgis"
    engine = create_engine(conn_str)

    def __init__(self, geojson_url):
        label_df = gpd.read_file(geojson_url)
        label_df = label_df[label_df['geometry'].isna() != True] # remove empty rows
        print("Object count: ", len(label_df))
        label_df.condition = label_df.condition.fillna('N')
        self.label_df = label_df

    def to_postgis(self):
        # Save masks to PostGIS
        self.engine.execute('TRUNCATE TABLE markers_mask')
        self.label_df[['condition','geometry']].to_postgis('markers_mask', self.engine, schema='public', if_exists='append')


def load_into_PostGIS(file):

    os.environ['PGPASSWORD'] = os.getenv('POSTGRES_PASSWORD')
    os.environ['PGUSER'] = os.getenv('POSTGRES_USER')
    os.environ['PGDATABASE'] = os.getenv('POSTGRES_DB')
    os.environ['PGHOST'] = os.getenv('POSTGRES_HOST')
    cmds = 'raster2pgsql -s 3857 -C -F -Y -t 256x256 /srv/html/app/import/geo-znz.tif public.myrasters | psql'
           #'psql -U {} -d {} -h {} -p 5432'.format(os.getenv('POSTGRES_USER'), os.getenv('POSTGRES_DB'), os.getenv('POSTGRES_HOST'))

    subprocess.call(cmds, shell=True)


def main():
    # Define storage
    client = DGSMinio(
        "minio1:9000",
        access_key="Q3AM3UQ867SPQQA43P2A",
        secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TA",
        secure=False,
    )

    # Define bucket
    bucket_name = "geo-znz"
    client.define_bucket(bucket_name)

    # Get image
    tif_url = 'http://oin-hotosm.s3.amazonaws.com/5afeda152b6a08001185f11a/0/5afeda152b6a08001185f11b.tif'
    tif_name = "geo-znz.tif"
    client.get_from_url(tif_url, tif_name)

    # Get masks
    geojson_url = 'https://www.dropbox.com/sh/ct3s1x2a846x3yl/AAARCAOqhcRdoU7ULOb9GJl9a/grid_001.geojson?dl=1'
    geojson_name = "geo-znz.geojson"
    client.get_from_url(geojson_url, geojson_name)

    #masks = DGSMasks(geojson_url)
    #masks.to_postgis()

    #file = client.get_object(bucket_name, tif_name)
    load_into_PostGIS('import/geo-znz.tif')

if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)


